#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Epson FP-90III RT - esempio invio comandi:
- Documento commerciale: vendita 10,00€ pagata in contanti
- Chiusura giornaliera: Z report
- Loop 1..1000

Protocollo PDU:
STX CNT IDEN A.PDU CKS ETX, checksum = somma ASCII di CNT+IDEN+A.PDU mod 100
e A.PDU.ERR = "ERR" + OP(2) + N(2) (codice errore). 
"""

from __future__ import annotations

import argparse
import random
import socket
import sys
import time
from dataclasses import dataclass
from typing import Optional, Protocol


STX = b"\x02"
ETX = b"\x03"
ACK = b"\x06"


class Transport(Protocol):
    def write(self, data: bytes) -> None: ...
    def read(self, n: int) -> bytes: ...
    def close(self) -> None: ...


class TCPTransport:
    def __init__(self, host: str, port: int, timeout: float = 5.0):
        self.sock = socket.create_connection((host, port), timeout=timeout)
        self.sock.settimeout(timeout)

    def write(self, data: bytes) -> None:
        self.sock.sendall(data)

    def read(self, n: int) -> bytes:
        return self.sock.recv(n)

    def close(self) -> None:
        try:
            self.sock.close()
        except Exception:
            pass


class SerialTransport:
    def __init__(self, port: str, baud: int = 57600, timeout: float = 2.0):
        # RS-232 default: 57600, N, 8, 1 :contentReference[oaicite:6]{index=6}
        try:
            import serial  # pip install pyserial
        except ImportError:
            raise RuntimeError("Per usare la seriale: pip install pyserial")

        self.ser = serial.Serial(
            port=port,
            baudrate=baud,
            bytesize=8,
            parity="N",
            stopbits=1,
            timeout=timeout,
        )

    def write(self, data: bytes) -> None:
        self.ser.write(data)

    def read(self, n: int) -> bytes:
        return self.ser.read(n)

    def close(self) -> None:
        try:
            self.ser.close()
        except Exception:
            pass


@dataclass
class EpsonReply:
    kind: str  # "DATA" or "ERR"
    raw_apdu: str
    # DATA
    h1: Optional[str] = None
    h2: Optional[str] = None
    data: Optional[str] = None
    # ERR
    op: Optional[str] = None
    err_code: Optional[int] = None


class EpsonPDUClient:
    def __init__(self, transport: Transport, timeout: float = 5.0, start_cnt: Optional[int] = None):
        self.t = transport
        self.timeout = timeout
        self.cnt = start_cnt if start_cnt is not None else random.randint(1, 99)

    @staticmethod
    def _checksum(cnt2: str, iden: str, apdu: str) -> str:
        total = sum((cnt2 + iden + apdu).encode("ascii"))
        return f"{total % 100:02d}"

    def _build_frame(self, apdu: str) -> bytes:
        cnt2 = f"{self.cnt:02d}"
        iden = "E"
        cks = self._checksum(cnt2, iden, apdu)
        frame = STX + cnt2.encode("ascii") + iden.encode("ascii") + apdu.encode("ascii") + cks.encode("ascii") + ETX
        # CNT in uscita deve incrementare 01..99 
        self.cnt = 1 if self.cnt >= 99 else self.cnt + 1
        return frame

    def _read_frame(self) -> bytes:
        """
        Legge un frame fino a ETX. Se ACK mode fosse attivo, può arrivare 0x06: lo ignoriamo.
        """
        deadline = time.time() + self.timeout
        # cerca STX
        while time.time() < deadline:
            b = self.t.read(1)
            if not b:
                continue
            if b == ACK:
                continue
            if b == STX:
                buf = bytearray(b)
                break
        else:
            raise TimeoutError("Timeout in attesa di STX")

        # leggi fino a ETX
        while time.time() < deadline:
            b = self.t.read(1)
            if not b:
                continue
            buf += b
            if b == ETX:
                return bytes(buf)

        raise TimeoutError("Timeout in attesa di ETX")

    def _parse_reply(self, frame: bytes) -> EpsonReply:
        if len(frame) < 1 + 2 + 1 + 2 + 1:
            raise ValueError(f"Frame troppo corto: {frame!r}")
        if frame[0:1] != STX or frame[-1:] != ETX:
            raise ValueError(f"Frame non valido (STX/ETX): {frame!r}")

        cnt2 = frame[1:3].decode("ascii", errors="replace")
        iden = frame[3:4].decode("ascii", errors="replace")
        apdu = frame[4:-3].decode("ascii", errors="replace")
        cks = frame[-3:-1].decode("ascii", errors="replace")

        calc = self._checksum(cnt2, iden, apdu)
        if calc != cks:
            raise ValueError(f"Checksum errato: ricevuto={cks} calcolato={calc} apdu={apdu!r}")

        # Error PDU: "ERR" + OP(2) + N(2) :contentReference[oaicite:8]{index=8}
        if apdu.startswith("ERR"):
            op = apdu[3:5]
            code = int(apdu[5:7])
            return EpsonReply(kind="ERR", raw_apdu=apdu, op=op, err_code=code)

        # Data PDU: H1(1) + H2(3) + DATA :contentReference[oaicite:9]{index=9}
        h1 = apdu[0:1]
        h2 = apdu[1:4]
        data = apdu[4:]
        return EpsonReply(kind="DATA", raw_apdu=apdu, h1=h1, h2=h2, data=data)

    def send_apdu(self, apdu: str) -> EpsonReply:
        frame = self._build_frame(apdu)
        self.t.write(frame)
        resp = self._read_frame()
        return self._parse_reply(resp)


# -------------------------
# Helpers per campi fissi
# -------------------------
def only_ascii_upper(s: str) -> str:
    # Semplifica: solo ASCII stampabile, maiuscolo, niente accenti.
    s2 = "".join(ch for ch in s if 32 <= ord(ch) <= 126)
    return s2.upper()

def fmt_op(op: int) -> str:
    return f"{op:02d}"

def fmt_dep(dep: int) -> str:
    return f"{dep:02d}"

def fmt_qty_3dec(qty: float) -> str:
    # QTY 7 bytes: 0000.001 .. 9999.999 in millesimi; es: 1 => 0001000 
    v = int(round(qty * 1000))
    if v <= 0 or v > 9_999_999:
        raise ValueError("QTY fuori range")
    return f"{v:07d}"

def fmt_cents_9(amount_cents: int) -> str:
    if amount_cents < 0 or amount_cents > 999_999_999:
        raise ValueError("Importo fuori range")
    return f"{amount_cents:09d}"


# -------------------------
# Comandi (A.PDU)
# -------------------------
def apdu_begin_commercial(op: int) -> str:
    # TX 1 085 OP :contentReference[oaicite:11]{index=11}
    return "1" + "085" + fmt_op(op)

def apdu_print_item(op: int, descr: str, qty: float, unit_price_cents: int, dep: int, lr: int = 1) -> str:
    # TX 1 080 OP DESCR QTY PRICE DEP L/R :contentReference[oaicite:12]{index=12}
    d = only_ascii_upper(descr)[:38]
    return (
        "1" + "080" +
        fmt_op(op) +
        d +
        fmt_qty_3dec(qty) +
        fmt_cents_9(unit_price_cents) +
        fmt_dep(dep) +
        str(lr)
    )

def apdu_pay(op: int, descr: str, amount_cents: int, pay_type: int = 0, ind: int = 0, lr: int = 1) -> str:
    # TX 1 084 OP DESCR AMN TYPE IND L/R :contentReference[oaicite:13]{index=13}
    # Per contanti: TYPE=0, IND=00 (entra nel totalizzatore contanti) 
    d = only_ascii_upper(descr)[:20]
    return (
        "1" + "084" +
        fmt_op(op) +
        d +
        fmt_cents_9(amount_cents) +
        str(pay_type) +
        f"{ind:02d}" +
        str(lr)
    )

def apdu_end_commercial(op: int) -> str:
    # TX 1 087 OP :contentReference[oaicite:15]{index=15}
    return "1" + "087" + fmt_op(op)

def apdu_z_report(op: int) -> str:
    # TX 3 001 OP :contentReference[oaicite:16]{index=16}
    return "3" + "001" + fmt_op(op)

def apdu_reset(op: int) -> str:
    # TX 1 088 OP :contentReference[oaicite:17]{index=17}
    return "1" + "088" + fmt_op(op)


def main() -> int:
    p = argparse.ArgumentParser()
    conn = p.add_mutually_exclusive_group(required=True)
    conn.add_argument("--tcp", help="host:port (es. 192.168.1.50:9100)")
    conn.add_argument("--serial", help="porta seriale (es. COM3 o /dev/ttyUSB0)")
    p.add_argument("--baud", type=int, default=57600, help="baud rate seriale (default 57600)")
    p.add_argument("--timeout", type=float, default=8.0, help="timeout lettura frame (s)")
    p.add_argument("--op", type=int, default=1, help="operatore (01..12)")
    p.add_argument("--dep", type=int, default=1, help="reparto (01..99)")
    p.add_argument("--loops", type=int, default=1000, help="numero iterazioni")
    p.add_argument("--sleep", type=float, default=0.0, help="sleep tra i comandi (s)")
    args = p.parse_args()

    if args.tcp:
        host, port_s = args.tcp.split(":")
        t: Transport = TCPTransport(host, int(port_s), timeout=args.timeout)
    else:
        t = SerialTransport(args.serial, baud=args.baud, timeout=args.timeout)

    cli = EpsonPDUClient(t, timeout=args.timeout)

    try:
        # opzionale: due status per “agganciare” la comunicazione
        # TX 1 074 OP :contentReference[oaicite:18]{index=18}
        for _ in range(2):
            rep = cli.send_apdu("1" + "074" + fmt_op(args.op))
            if rep.kind == "ERR":
                print(f"[WARN] GET STATUS err={rep.err_code}")
            time.sleep(0.05)

        for i in range(1, args.loops + 1):
            print(f"\n=== ITER {i}/{args.loops} ===")

            # 1) BEGIN COMMERCIAL DOCUMENT
            r = cli.send_apdu(apdu_begin_commercial(args.op))
            if r.kind == "ERR":
                # se già aperto, sequenza errata ecc.
                print(f"[ERR] BEGIN COMMERCIAL -> {r.err_code} (OP={r.op})")
                # prova reset e riparti
                cli.send_apdu(apdu_reset(args.op))
                continue
            if args.sleep: time.sleep(args.sleep)

            # 2) SALE: 10,00€
            r = cli.send_apdu(apdu_print_item(args.op, "VENDITA 10 EURO", qty=1.0, unit_price_cents=1000, dep=args.dep, lr=1))
            if r.kind == "ERR":
                print(f"[ERR] PRINT ITEM -> {r.err_code} (OP={r.op})")
                cli.send_apdu(apdu_reset(args.op))
                continue
            if args.sleep: time.sleep(args.sleep)

            # 3) PAYMENT CASH 10,00€ (TYPE=0 IND=00)
            r = cli.send_apdu(apdu_pay(args.op, "CONTANTI", amount_cents=1000, pay_type=0, ind=0, lr=1))
            if r.kind == "ERR":
                print(f"[ERR] PAY -> {r.err_code} (OP={r.op})")
                cli.send_apdu(apdu_reset(args.op))
                continue

            # Check CMP (payment complete) se vuoi essere più rigido
            if r.kind == "DATA" and r.h1 == "1" and r.h2 == "084":
                # data: OP(2) + CMP(1) + ...
                cmp = (r.data or "")[2:3]
                if cmp != "1":
                    print(f"[WARN] Payment non completo (CMP={cmp}) -> reset")
                    cli.send_apdu(apdu_reset(args.op))
                    continue

            if args.sleep: time.sleep(args.sleep)

            # 4) END COMMERCIAL (necessario se JavaPOS-UPOS=1; altrimenti può dare ERR 16)
            r = cli.send_apdu(apdu_end_commercial(args.op))
            if r.kind == "ERR" and r.err_code in (16, 11):
                # 16 = NON PREVISTO se JavaPOS-UPOS non attivo :contentReference[oaicite:19]{index=19}
                # 11 = sequenza errata (es. già chiuso)
                print(f"[INFO] END COMMERCIAL ignorato (err={r.err_code})")
            elif r.kind == "ERR":
                print(f"[ERR] END COMMERCIAL -> {r.err_code}")
                cli.send_apdu(apdu_reset(args.op))
                continue

            if args.sleep: time.sleep(args.sleep)

            # 5) Z REPORT (chiusura giornaliera)
            r = cli.send_apdu(apdu_z_report(args.op))
            if r.kind == "ERR":
                print(f"[ERR] Z REPORT -> {r.err_code} (OP={r.op})")
                # se non riesce, reset e vai avanti
                cli.send_apdu(apdu_reset(args.op))
                continue
            else:
                # RX 3 001 OP DATE TIME FR.N :contentReference[oaicite:20]{index=20}
                print(f"[OK] Z report emesso. Raw={r.raw_apdu}")

            if args.sleep: time.sleep(args.sleep)

        return 0

    finally:
        t.close()


if __name__ == "__main__":
    raise SystemExit(main())

#python3 epson_fp90iii_loop.py --tcp 192.168.1.50:9100 --loops 1000
