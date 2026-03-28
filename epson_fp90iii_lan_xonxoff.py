#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
EPSON FP-90III RT - Protocollo XON-XOFF Rev 6.3 via LAN (TCP 9100)

Per ogni iterazione:
  1) Vendita 10,00€ su REPARTO N  -> 1000H{N}R
  2) Pagamento CONTANTI           -> 1T
  3) Chiusura giornaliera (Z)     -> 1F

Comandi / esempi nel protocollo:
- Vendita a reparto: 1000H1R (10,00€ su reparto 1)  :contentReference[oaicite:5]{index=5}
- Pagamento contanti: 1T                             
- Rapporto Z (chiusura fiscale con azzeramento): 1F   :contentReference[oaicite:7]{index=7}
- Footer opzionale (SET 14/42): STXgg-mm-aaaa hh:mm nnnnKKETX :contentReference[oaicite:8]{index=8}

Nota: XON/XOFF è monodirezionale; lo script gestisce eventuali XOFF/XON ricevuti.
"""

from __future__ import annotations

import argparse
import select
import socket
import time
from dataclasses import dataclass
from typing import Optional

XON  = b"\x11"  # DC1
XOFF = b"\x13"  # DC3
STX  = b"\x02"
ETX  = b"\x03"


@dataclass
class Footer:
    raw: bytes
    date_time: Optional[str] = None
    doc_no: Optional[str] = None
    checksum: Optional[str] = None


class EpsonLanXonXoff:
    def __init__(self, host: str, port: int = 9100, timeout: float = 2.0):
        self.sock = socket.create_connection((host, port), timeout=timeout)
        self.sock.settimeout(timeout)
        self.paused = False  # se riceviamo XOFF

    def close(self) -> None:
        try:
            self.sock.close()
        except Exception:
            pass

    def _recv_nonblocking(self, max_bytes: int = 4096, wait: float = 0.0) -> bytes:
        """Legge quel che c'è disponibile (senza bloccare oltre 'wait')."""
        r, _, _ = select.select([self.sock], [], [], wait)
        if not r:
            return b""
        try:
            return self.sock.recv(max_bytes)
        except socket.timeout:
            return b""

    def _pump_flow_chars(self) -> None:
        """Aggiorna stato paused leggendo eventuali XON/XOFF arrivati."""
        data = self._recv_nonblocking(wait=0.0)
        if not data:
            return
        if XOFF in data:
            self.paused = True
        if XON in data:
            self.paused = False
        # se nel buffer ci fossero anche altri dati (es. footer), NON li consumiamo qui:
        # per semplicità, la lettura footer usa un metodo dedicato (read_footer) con wait.

    def _wait_if_paused(self, timeout: float = 10.0) -> None:
        if not self.paused:
            return
        deadline = time.time() + timeout
        while time.time() < deadline:
            data = self._recv_nonblocking(wait=0.2)
            if not data:
                continue
            if XON in data:
                self.paused = False
                return
            if XOFF in data:
                self.paused = True
        raise TimeoutError("Timeout: stampante in XOFF (buffer pieno)")

    def send_cmd(self, cmd: str, add_crlf: bool = False) -> None:
        """
        Invia un comando ASCII. CR/LF sono tipicamente ignorati, ma possono essere utili in debug.
        """
        self._pump_flow_chars()
        self._wait_if_paused()

        payload = cmd.encode("ascii", errors="replace")
        if add_crlf:
            payload += b"\r\n"
        self.sock.sendall(payload)

    def read_footer(self, timeout: float = 2.0) -> Optional[Footer]:
        """
        Legge il footer STX ... ETX se SET 14/42 è attivo.
        Se non arriva nulla entro timeout, ritorna None.
        """
        deadline = time.time() + timeout
        buf = bytearray()

        # cerca STX
        while time.time() < deadline:
            data = self._recv_nonblocking(wait=0.2)
            if not data:
                continue

            # aggiorna flow control
            if XOFF in data:
                self.paused = True
            if XON in data:
                self.paused = False

            buf += data
            stx_pos = buf.find(STX)
            if stx_pos != -1:
                buf = buf[stx_pos:]  # taglia tutto prima dello STX
                break
        else:
            return None

        # leggi fino a ETX
        while time.time() < deadline:
            etx_pos = buf.find(ETX)
            if etx_pos != -1:
                raw = bytes(buf[: etx_pos + 1])
                return self._parse_footer(raw)

            data = self._recv_nonblocking(wait=0.2)
            if not data:
                continue
            buf += data

        return None

    @staticmethod
    def _parse_footer(raw: bytes) -> Footer:
        """
        Formato: STXgg-mm-aaaa hh:mm nnnnKKETX  :contentReference[oaicite:9]{index=9}
        Parsing best-effort (il calcolo checksum KK non è implementato qui).
        """
        f = Footer(raw=raw)
        try:
            mid = raw[1:-1].decode("ascii", errors="replace").strip()
            # esempio: "18-12-2023 12:30 0001AB"
            #          0........9 11..15 17..20 21..22
            if len(mid) >= 16:
                f.date_time = mid[0:16].strip()
            # prova a estrarre doc e checksum guardando la parte finale
            tail = mid[16:].strip()
            # spesso è: "0001KK"
            if len(tail) >= 6 and tail[:4].isdigit():
                f.doc_no = tail[:4]
                f.checksum = tail[4:6]
        except Exception:
            pass
        return f


def cmd_sale(amount_cents: int, reparto: int) -> str:
    # 10,00€ -> 1000 centesimi; vendita reparto: {amount}H{rep}R :contentReference[oaicite:10]{index=10}
    return f"{amount_cents}H{reparto}R"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", required=True, help="IP o hostname RT (LAN)")
    ap.add_argument("--port", type=int, default=9100, help="porta TCP (default 9100)")
    ap.add_argument("--loops", type=int, default=1000, help="numero iterazioni (default 1000)")
    ap.add_argument("--reparto", type=int, default=1, help="reparto vendita (default 1)")
    ap.add_argument("--amount-cents", type=int, default=1000, help="importo vendita in centesimi (default 1000=10,00€)")
    ap.add_argument("--sleep", type=float, default=0.1, help="pausa tra iterazioni (default 0.1s)")
    ap.add_argument("--crlf", action="store_true", help="aggiunge CRLF dopo ogni comando (debug)")
    ap.add_argument("--try-footer", action="store_true",
                    help="prova a leggere footer STX..ETX (funziona solo se SET 14/42=SI)")
    ap.add_argument("--footer-timeout", type=float, default=1.5, help="timeout lettura footer (s)")
    args = ap.parse_args()

    cli = EpsonLanXonXoff(args.host, args.port)

    try:
        for i in range(1, args.loops + 1):
            print(f"== ITER {i}/{args.loops} ==")

            # 1) vendita
            cli.send_cmd(cmd_sale(args.amount_cents, args.reparto), add_crlf=args.crlf)

            # 2) pagamento contanti (chiude il documento commerciale)
            cli.send_cmd("1T", add_crlf=args.crlf)  # 

            if args.try_footer:
                f = cli.read_footer(timeout=args.footer_timeout)
                if f:
                    print(f"Footer doc: date_time={f.date_time} doc={f.doc_no} kk={f.checksum} raw={f.raw!r}")
                else:
                    print("Footer doc: (nessuna risposta - probabile SET 14/42=NO)")

            # 3) chiusura giornaliera Z
            cli.send_cmd("1F", add_crlf=args.crlf)  # :contentReference[oaicite:12]{index=12}

            if args.try_footer:
                f = cli.read_footer(timeout=args.footer_timeout)
                if f:
                    print(f"Footer Z: date_time={f.date_time} doc={f.doc_no} kk={f.checksum} raw={f.raw!r}")
                else:
                    print("Footer Z: (nessuna risposta - probabile SET 14/42=NO)")

            if args.sleep:
                time.sleep(args.sleep)

        return 0
    finally:
        cli.close()


if __name__ == "__main__":
    raise SystemExit(main())

#python3 epson_fp90iii_lan_xonxoff.py --host 192.168.1.50 --loops 1000

#python3 epson_fp90iii_lan_xonxoff.py --host 192.168.1.50 --loops 1000 --try-footer --footer-timeout 2
