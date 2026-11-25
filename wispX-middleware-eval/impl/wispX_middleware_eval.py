#!/usr/bin/env python3
"""
wispX_middleware_eval.py — Évalue le rôle du middleware WISPX (port 9333) dans le pipeline d'écriture CDP.
Usage: python wispX_middleware_eval.py [wispX_port] [cdp_port]
"""

import sys
import json
import hashlib
import socket
import time
import urllib.request
from datetime import datetime, timezone

WISPX_PORT = 9333
CDP_PORT = 9222


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def tcp_check(host: str, port: int, timeout: float = 2.0) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception:
        return False


def http_get(url: str, timeout: float = 5.0) -> dict:
    try:
        resp = urllib.request.urlopen(url, timeout=timeout)
        return {"ok": True, "status": resp.status, "body": resp.read().decode("utf-8", errors="replace")[:500]}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def measure_cdp_latency(cdp_port: int) -> dict:
    import websocket

    resp = urllib.request.urlopen(f"http://127.0.0.1:{cdp_port}/json/list", timeout=10)
    tabs = json.load(resp)
    tab_id = None
    for t in tabs:
        url = t.get("url", "")
        if "gemini.google.com" in url and t.get("type") == "page":
            tab_id = t.get("id")
            break

    if not tab_id:
        return {"ok": False, "error": "Aucun onglet Gemini trouvé"}

    resp2 = urllib.request.urlopen(f"http://127.0.0.1:{cdp_port}/json", timeout=10)
    tabs2 = json.load(resp2)
    ws_url = None
    for t in tabs2:
        if t.get("id") == tab_id:
            ws_url = t.get("webSocketDebuggerUrl")
            break

    ws = websocket.create_connection(ws_url, timeout=30)
    cid = [0]

    def send(method, params):
        cid[0] += 1
        msg = {"id": cid[0], "method": method, "params": params or {}}
        ws.send(json.dumps(msg))
        while True:
            raw = ws.recv()
            r = json.loads(raw)
            if r.get("id") == cid[0]:
                return r

    send("Page.enable", {})
    send("Runtime.enable", {})

    t0 = time.perf_counter()
    r = send("Runtime.evaluate", {"expression": "1+1", "returnByValue": True})
    lat_ms = (time.perf_counter() - t0) * 1000

    value = r.get("result", {}).get("result", {}).get("value", "")
    ws.close()

    return {"ok": True, "latency_ms": round(lat_ms, 3), "value": value}


def main():
    wispx_port = int(sys.argv[1]) if len(sys.argv) > 1 else WISPX_PORT
    cdp_port = int(sys.argv[2]) if len(sys.argv) > 2 else CDP_PORT

    cdp_active = tcp_check("127.0.0.1", cdp_port)
    wispx_active = tcp_check("127.0.0.1", wispx_port)

    wispx_health = None
    if wispx_active:
        wispx_health = http_get(f"http://127.0.0.1:{wispx_port}/health", timeout=3.0)

    cdp_latency = None
    if cdp_active:
        cdp_latency = measure_cdp_latency(cdp_port)

    wispx_is_proxy = bool(wispx_active and wispx_health and wispx_health.get("ok"))

    result = {
        "ok": True,
        "skill": "wispX-middleware-eval",
        "cdp_port": cdp_port,
        "wispx_port": wispx_port,
        "cdp_active": cdp_active,
        "wispx_active": wispx_active,
        "wispx_has_health_endpoint": bool(wispx_health and wispx_health.get("ok")),
        "wispx_health_body": wispx_health.get("body", "") if wispx_health else None,
        "wispx_is_cdp_proxy": wispx_is_proxy,
        "latency_cdp_direct_ms": cdp_latency.get("latency_ms") if cdp_latency else None,
        "latency_wispx_ms": None,
        "recommendation": "",
        "timestamp_utc": now_utc(),
        "wal_seal": "WAL-0x243",
    }

    if not cdp_active:
        result["recommendation"] = "CDP inactif — impossible d'écrire sur Chromium"
    elif wispx_is_proxy:
        result["recommendation"] = "WISPX actif avec endpoint de santé — peut être un proxy CDP, mesurer latence via WISPX"
    else:
        result["recommendation"] = "CDP direct uniquement — WISPX n'est pas dans le tunnel d'écriture Chromium (inactif ou sans API de relay)"

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()