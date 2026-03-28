#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RT-Server (EPSON Fiscal Security Communication Protocol rev.19) - Loop:
- createReceipt: vendita 10,00€ + pagamento contanti
- createDailyClosure
- (opzionale) printZReport via fpmate.cgi

Riferimenti protocollo:
- URL fpserver.cgi: https://{ip}/cgi-bin/fpserver.cgi  :contentReference[oaicite:6]{index=6}
- Auth: HTTP authentication (Digest)                   :contentReference[oaicite:7]{index=7}
- createToken / token format                           :contentReference[oaicite:8]{index=8}
- createReceipt + esempio XML                           :contentReference[oaicite:9]{index=9}
- createDailyClosure                                    :contentReference[oaicite:10]{index=10}
- fpmate.cgi printZReport                                :contentReference[oaicite:11]{index=11}
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import sys
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple

# Dipendenze: pip install requests
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth


SOAP_ENV_NS = "http://schemas.xmlsoap.org/soap/envelope/"
SOAPENV = f"{{{SOAP_ENV_NS}}}"


def soap_envelope(body_xml: str) -> str:
    return (
        '<?xml version="1.0" encoding="utf-8"?>'
        f'<soapenv:Envelope xmlns:soapenv="{SOAP_ENV_NS}">'
        f"<soapenv:Body>{body_xml}</soapenv:Body>"
        "</soapenv:Envelope>"
    )


def local_name(tag: str) -> str:
    # "{ns}name" -> "name"
    if "}" in tag:
        return tag.split("}", 1)[1]
    return tag


@dataclass
class SoapResponse:
    success: bool
    code: str
    status: str
    addinfo: Dict[str, str]
    raw_xml: str


@dataclass
class TokenInfo:
    token: str
    server_serial: str
    till_id: str
    random_number: str
    server_date: str  # YYYYMMDD
    zrep_number: str  # 4 digits
    next_doc_number: str  # 4 digits
    daily_amount_cents: int  # 9 numeric, last 2 decimals implied


def parse_token(token: str) -> TokenInfo:
    # Token fields (len): serverSN(11) + tillId(8) + rnd(5) + date(8) + zrep(4) + doc(4) + daily(9) :contentReference[oaicite:12]{index=12}
    # Totale 49. Se il vendor aggiunge altro, qui facciamo best-effort prendendo le code note dal fondo.
    if len(token) < 49:
        raise ValueError(f"Token troppo corto ({len(token)}): {token!r}")

    daily = token[-9:]
    doc = token[-13:-9]
    zrep = token[-17:-13]
    date = token[-25:-17]
    rnd = token[-30:-25]
    till = token[-38:-30]
    srv = token[-49:-38]

    if not daily.isdigit() or not doc.isdigit() or not zrep.isdigit() or not date.isdigit():
        # Se non combacia, restituiamo comunque (ma segnaliamo)
        raise ValueError(f"Token non parsabile in modo affidabile: {token!r}")

    return TokenInfo(
        token=token,
        server_serial=srv,
        till_id=till,
        random_number=rnd,
        server_date=date,
        zrep_number=zrep,
        next_doc_number=doc,
        daily_amount_cents=int(daily),
    )


class RTServerClient:
    def __init__(
        self,
        host: str,
        scheme: str,
        user: str,
        password: str,
        verify_tls: bool,
        timeout: float,
        auth_mode: str = "digest",
    ):
        self.host = host
        self.scheme = scheme
        self.verify_tls = verify_tls
        self.timeout = timeout

        self.fpserver_url = f"{scheme}://{host}/cgi-bin/fpserver.cgi"  # :contentReference[oaicite:13]{index=13}
        self.fpmate_url = f"{scheme}://{host}/cgi-bin/fpmate.cgi"      # :contentReference[oaicite:14]{index=14}

        self.s = requests.Session()
        if auth_mode == "basic":
            self.s.auth = HTTPBasicAuth(user, password)
        else:
            self.s.auth = HTTPDigestAuth(user, password)  # :contentReference[oaicite:15]{index=15}

        # Riduce warning se verify_tls=False (self-signed)
        if not verify_tls:
            try:
                requests.packages.urllib3.disable_warnings()  # type: ignore[attr-defined]
            except Exception:
                pass

    def _post_soap(self, url: str, body_xml: str) -> SoapResponse:
        payload = soap_envelope(body_xml)
        headers = {"Content-Type": "application/soap+xml; charset=utf-8"}  # :contentReference[oaicite:16]{index=16}

        r = self.s.post(url, data=payload.encode("utf-8"), headers=headers,
                        verify=self.verify_tls, timeout=self.timeout)

        # Fallback: se digest fallisce in certi setup LAN, prova basic
        if r.status_code == 401 and isinstance(self.s.auth, HTTPDigestAuth):
            # riprova basic una volta
            basic = HTTPBasicAuth(self.s.auth.username, self.s.auth.password)  # type: ignore[arg-type]
            r = self.s.post(url, data=payload.encode("utf-8"), headers=headers,
                            verify=self.verify_tls, timeout=self.timeout, auth=basic)

        r.raise_for_status()
        raw = r.text

        # Parse XML (SOAP envelope)
        root = ET.fromstring(raw)
        resp_el = None
        for el in root.iter():
            if local_name(el.tag) == "response":
                resp_el = el
                break
        if resp_el is None:
            raise ValueError(f"Risposta senza <response>: {raw}")

        success = resp_el.attrib.get("success", "false").lower() == "true"
        code = resp_el.attrib.get("code", "")
        status = resp_el.attrib.get("status", "")

        addinfo: Dict[str, str] = {}
        for el in resp_el.iter():
            if local_name(el.tag) == "addInfo":
                for child in list(el):
                    # elementList, token, fingerPrint, fiscalReceiptNumber, zRepNumber, ecc. :contentReference[oaicite:17]{index=17}
                    addinfo[local_name(child.tag)] = (child.text or "").strip()
                break

        return SoapResponse(success=success, code=code, status=status, addinfo=addinfo, raw_xml=raw)

    # ---- fpserver.cgi ----

    def create_token(self, till_id: str) -> SoapResponse:
        body = f'<createToken><till tillId="{till_id}" /></createToken>'  # :contentReference[oaicite:18]{index=18}
        return self._post_soap(self.fpserver_url, body)

    def create_receipt(self, body_xml: str) -> SoapResponse:
        return self._post_soap(self.fpserver_url, body_xml)  # :contentReference[oaicite:19]{index=19}

    def create_daily_closure(self, till_id: str) -> SoapResponse:
        body = f'<createDailyClosure><till tillId="{till_id}" /></createDailyClosure>'  # :contentReference[oaicite:20]{index=20}
        return self._post_soap(self.fpserver_url, body)

    # ---- fpmate.cgi ----

    def print_z_report(self, manager_user: str, manager_pass: str) -> SoapResponse:
        # Richiede manager user. :contentReference[oaicite:21]{index=21}
        body = "<printerFiscalReport><printZReport/></printerFiscalReport>"  # :contentReference[oaicite:22]{index=22}
        # forza auth manager per questa chiamata
        auth = HTTPDigestAuth(manager_user, manager_pass)
        payload = soap_envelope(body)
        headers = {"Content-Type": "application/soap+xml; charset=utf-8"}

        r = self.s.post(self.fpmate_url, data=payload.encode("utf-8"), headers=headers,
                        verify=self.verify_tls, timeout=self.timeout, auth=auth)
        if r.status_code == 401:
            # fallback basic
            r = self.s.post(self.fpmate_url, data=payload.encode("utf-8"), headers=headers,
                            verify=self.verify_tls, timeout=self.timeout, auth=HTTPBasicAuth(manager_user, manager_pass))
        r.raise_for_status()

        raw = r.text
        root = ET.fromstring(raw)
        resp_el = None
        for el in root.iter():
            if local_name(el.tag) == "response":
                resp_el = el
                break
        if resp_el is None:
            raise ValueError(f"Risposta senza <response>: {raw}")

        success = resp_el.attrib.get("success", "false").lower() == "true"
        code = resp_el.attrib.get("code", "")
        status = resp_el.attrib.get("status", "")

        addinfo: Dict[str, str] = {}
        for el in resp_el.iter():
            if local_name(el.tag) == "addInfo":
                for child in list(el):
                    addinfo[local_name(child.tag)] = (child.text or "").strip()
                break

        return SoapResponse(success=success, code=code, status=status, addinfo=addinfo, raw_xml=raw)


def fmt_4(n: int) -> str:
    return f"{n:04d}"


def now_fiscal_datetime() -> str:
    # esempio nel doc: 20170708T201900 (YYYYMMDDTHHMMSS) :contentReference[oaicite:23]{index=23}
    return dt.datetime.now().strftime("%Y%m%dT%H%M%S")


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def build_printer_fiscal_receipt_xml(
    till_id: str,
    zrep_number: str,
    rec_number: str,
    daily_amount_cents_after: int,
    sale_cents: int,
    vat_id: str,
    item_desc: str,
    rec_vat_str: str,
) -> str:
    # NOTA: il contenuto dettagliato di printerFiscalReceipt rimanda a ePOS.fiscal.xml :contentReference[oaicite:24]{index=24}
    # Qui costruiamo un payload minimale e coerente con l’esempio createReceipt. :contentReference[oaicite:25]{index=25}
    dt_str = now_fiscal_datetime()
    daily_9 = f"{daily_amount_cents_after:09d}"

    # amount fields: nel token/dailyAmount sono numerici con 2 decimali impliciti (ultime 2 cifre) :contentReference[oaicite:26]{index=26}
    sale_str = str(sale_cents)

    return (
        "<printerFiscalReceipt>"
        "<beginFiscalReceipt />"
        f'<printRecItem vatID="{vat_id}" quantity="1" description="{item_desc}" unitPrice="{sale_str}"/>'
        f'<printRecTotal payment="{sale_str}" index="0" description="Cash" paymentType="0"/>'
        f'<fiscalInformation '
        f'dailyAmount="{daily_9}" '
        f'tillId="{till_id}" '
        f'zRepNumber="{zrep_number}" '
        f'recNumber="{rec_number}" '
        f'dateTime="{dt_str}" '
        f'recAmount="{sale_str}" '
        f'recVAT="{rec_vat_str}" '
        f'doctype="0" '              # 0 = Sales :contentReference[oaicite:27]{index=27}
        f'cashAmount="{sale_str}" '
        f'ePayAmount="0" '
        f'noPayAmount="0" '
        f'changeAmount="0" '
        f'paidAmount="{sale_str}"'
        "/>"
        "<endFiscalReceipt />"
        "</printerFiscalReceipt>"
    )


def build_create_receipt_xml(section_a: str, printer_fiscal_receipt_xml: str, ccdc_hex: str) -> str:
    # Struttura come nell’esempio createReceipt. :contentReference[oaicite:28]{index=28}
    return (
        "<createReceipt>"
        "<receipt>"
        f'<hash fingerPrint="{section_a}"/>'
        f"{printer_fiscal_receipt_xml}"
        "</receipt>"
        "<receiptSecurity>"
        f'<hash fingerPrint="{ccdc_hex}"/>'
        "</receiptSecurity>"
        "</createReceipt>"
    )


def compute_ccdc(section_a: str, section_b_xml: str) -> str:
    # CCDC = SHA-256( SectionA + SectionB ) :contentReference[oaicite:29]{index=29}
    return sha256_hex(section_a.encode("utf-8") + section_b_xml.encode("utf-8"))


def compute_vat_from_gross(gross_cents: int, vat_rate_percent: float) -> str:
    # VAT su lordo: vat = gross * rate/(100+rate)
    gross = gross_cents / 100.0
    vat = gross * (vat_rate_percent / (100.0 + vat_rate_percent))
    # rev.7: separatore decimale punto (usiamo ".") :contentReference[oaicite:30]{index=30}
    return f"{vat:.2f}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", required=True, help="IP/host RT-Server (LAN)")
    ap.add_argument("--scheme", default="https", choices=["https", "http"], help="default https")
    ap.add_argument("--user", default="epson", help="TILL user (default epson)")
    ap.add_argument("--password", default="epson", help="TILL password (default epson)")
    ap.add_argument("--auth", default="digest", choices=["digest", "basic"], help="auth mode (default digest)")
    ap.add_argument("--verify-tls", action="store_true", help="verifica TLS (default: NO, utile con certificati self-signed)")
    ap.add_argument("--timeout", type=float, default=10.0)
    ap.add_argument("--till-id", required=True, help='TillId (8 chars, es "AAAA0001") :contentReference[oaicite:31]{index=31}')

    ap.add_argument("--loops", type=int, default=1000)
    ap.add_argument("--sleep", type=float, default=0.1)

    ap.add_argument("--sale-cents", type=int, default=1000, help="vendita in centesimi (default 1000=10,00€)")
    ap.add_argument("--vat-id", default="1", help="vatID per printRecItem (default 1)")
    ap.add_argument("--vat-rate", type=float, default=22.0, help="aliquota per calcolo recVAT (default 22.0)")
    ap.add_argument("--item-desc", default="VENDITA 10 EURO", help="descrizione riga")

    ap.add_argument("--do-server-z", action="store_true",
                    help="dopo createDailyClosure chiama anche printZReport su fpmate.cgi (richiede credenziali manager)")
    ap.add_argument("--manager-user", default="", help="manager user (solo se --do-server-z)")
    ap.add_argument("--manager-pass", default="", help="manager pass (solo se --do-server-z)")

    args = ap.parse_args()

    cli = RTServerClient(
        host=args.host,
        scheme=args.scheme,
        user=args.user,
        password=args.password,
        verify_tls=args.verify_tls,
        timeout=args.timeout,
        auth_mode=args.auth,
    )

    # 1) createToken (necessario per inizializzare sectionA) :contentReference[oaicite:32]{index=32}
    r = cli.create_token(args.till_id)
    if not r.success:
        print(f"[FATAL] createToken KO code={r.code} status={r.status}")
        return 2

    token = r.addinfo.get("token", "")
    if not token:
        print("[FATAL] createToken OK ma token non presente in addInfo")
        return 2

    try:
        tinfo = parse_token(token)
    except Exception as e:
        print(f"[WARN] Token ricevuto ma parsing non affidabile: {e}")
        # Continuiamo comunque: useremo il token come sectionA e gestiremo numeri “locali”
        tinfo = TokenInfo(
            token=token,
            server_serial="",
            till_id=args.till_id,
            random_number="",
            server_date=dt.datetime.now().strftime("%Y%m%d"),
            zrep_number="0001",
            next_doc_number="0001",
            daily_amount_cents=0,
        )

    # Stato corrente per loop
    prev_ccdc_or_token = token  # SectionA: prima volta Token, poi Previous CCDC :contentReference[oaicite:33]{index=33}
    zrep_number = tinfo.zrep_number
    rec_number_int = int(tinfo.next_doc_number) if tinfo.next_doc_number.isdigit() else 1
    daily_amount_cents = tinfo.daily_amount_cents

    for i in range(1, args.loops + 1):
        print(f"\n=== ITER {i}/{args.loops} ===")

        # prepara numeri e importi
        rec_number = fmt_4(rec_number_int)
        daily_amount_cents += args.sale_cents  # daily amount “sales only” :contentReference[oaicite:34]{index=34}

        rec_vat = compute_vat_from_gross(args.sale_cents, args.vat_rate)

        section_b = build_printer_fiscal_receipt_xml(
            till_id=args.till_id,
            zrep_number=zrep_number,
            rec_number=rec_number,
            daily_amount_cents_after=daily_amount_cents,
            sale_cents=args.sale_cents,
            vat_id=args.vat_id,
            item_desc=args.item_desc,
            rec_vat_str=rec_vat,
        )

        ccdc = compute_ccdc(prev_ccdc_or_token, section_b)
        create_receipt_xml = build_create_receipt_xml(prev_ccdc_or_token, section_b, ccdc)

        # 2) createReceipt :contentReference[oaicite:35]{index=35}
        rr = cli.create_receipt(create_receipt_xml)
        if not rr.success:
            print(f"[ERR] createReceipt KO code={rr.code} status={rr.status}")

            # Se errore blockchain/hash, richiedi nuovo token (il doc dice di richiederlo in caso di errori security). :contentReference[oaicite:36]{index=36}
            if rr.code in ("-21", "-22"):  # Blockchain / Hash error :contentReference[oaicite:37]{index=37}
                print("[INFO] Richiedo nuovo token e riprovo una volta...")
                rtok = cli.create_token(args.till_id)
                if rtok.success and rtok.addinfo.get("token"):
                    prev_ccdc_or_token = rtok.addinfo["token"]
                    # ricalcolo e riprovo
                    ccdc = compute_ccdc(prev_ccdc_or_token, section_b)
                    create_receipt_xml = build_create_receipt_xml(prev_ccdc_or_token, section_b, ccdc)
                    rr = cli.create_receipt(create_receipt_xml)

            if not rr.success:
                print(f"[ERR] createReceipt fallito (definitivo) code={rr.code} status={rr.status}")
                # non incrementiamo rec_number_int in caso di fallimento
                time.sleep(args.sleep)
                continue

        # Se il server ritorna fingerPrint (CCDC) in addInfo, usalo come SectionA successiva :contentReference[oaicite:38]{index=38}
        fp = rr.addinfo.get("fingerPrint") or rr.addinfo.get("hash")
        if fp:
            prev_ccdc_or_token = fp

        frn = rr.addinfo.get("fiscalReceiptNumber", "").strip()
        zrn = rr.addinfo.get("zRepNumber", "").strip()
        fda = rr.addinfo.get("fiscalDailyAmount", "").strip()
        print(f"[OK] Receipt sent. serverReceipt={frn or rec_number} serverZ={zrn or zrep_number} daily={fda or daily_amount_cents}")

        rec_number_int += 1
        if rec_number_int > 9999:
            rec_number_int = 1

        if args.sleep:
            time.sleep(args.sleep)

        # 3) createDailyClosure (chiusura giornata per quel till) :contentReference[oaicite:39]{index=39}
        dc = cli.create_daily_closure(args.till_id)
        if not dc.success:
            print(f"[ERR] createDailyClosure KO code={dc.code} status={dc.status}")
        else:
            print("[OK] createDailyClosure OK")

        if args.sleep:
            time.sleep(args.sleep)

        # 4) opzionale printZReport su fpmate.cgi (Server Zreport) :contentReference[oaicite:40]{index=40}
        if args.do_server_z:
            if not args.manager_user or not args.manager_pass:
                print("[WARN] --do-server-z attivo ma mancano --manager-user/--manager-pass (skip)")
            else:
                try:
                    zz = cli.print_z_report(args.manager_user, args.manager_pass)
                    if zz.success:
                        print("[OK] printZReport OK")
                    else:
                        print(f"[ERR] printZReport KO code={zz.code} status={zz.status}")
                except Exception as e:
                    print(f"[ERR] printZReport exception: {e}")

        if args.sleep:
            time.sleep(args.sleep)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())


#
#python3 rtserver_rev19_loop.py --host 192.168.1.50 --till-id AAAA0001 --loops 1000   --do-server-z --manager-user NOME --manager-pass PASS
#
