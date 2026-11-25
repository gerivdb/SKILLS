#!/usr/bin/env python3
"""
cdp_latence_diagnostic.py — Diagnostique la latence CDP sur Chromium Profil 2.
Usage: python cdp_latence_diagnostic.py [cdp_tab_id] [n_measurements]
"""

import sys
import json
import hashlib
import statistics
import time
import websocket
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

CDP_PORT = 9222
GEMINI_URL_PATTERN = "gemini.google.com"


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def proof_record(action, target, state_before, state_after, exit_code,
                 sha256_before, sha256_after, skill, intent_hash):
    return {
        "action": action,
        "target": target,
        "state_before": state_before,
        "state_after": state_after,
        "exit_code": exit_code,
        "sha256_before": sha256_before,
        "sha256_after": sha256_after,
        "timestamp_utc": now_utc(),
        "wal_seal": "WAL-0x243",
        "skill": skill,
        "intent_hash": intent_hash,
    }


def get_gemini_tabs() -> list:
    resp = urllib.request.urlopen(f"http://127.0.0.1:{CDP_PORT}/json/list", timeout=10)
    tabs = json.load(resp)
    all_tabs = []
    gemini_tabs = []
    for t in tabs:
        url = t.get("url", "")
        info = {
            "id": t.get("id"),
            "type": t.get("type"),
            "url": url[:100] if url else "",
            "title": t.get("title", "")[:100] if t.get("title") else "",
        }
        all_tabs.append(info)
        if GEMINI_URL_PATTERN in url and t.get("type") == "page":
            gemini_tabs.append(info)
    return all_tabs, gemini_tabs


def get_ws_url(tab_id: str) -> str:
    resp = urllib.request.urlopen(f"http://127.0.0.1:{CDP_PORT}/json", timeout=10)
    tabs = json.load(resp)
    for t in tabs:
        if t.get("id") == tab_id:
            return t.get("webSocketDebuggerUrl")
    raise RuntimeError(f"Onglet {tab_id} introuvable")


def measure_cdp_latency(tab_id: str, n_measurements: int = 10) -> dict:
    ws_url = get_ws_url(tab_id)
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

    latencies = []
    for _ in range(n_measurements):
        t0 = time.perf_counter()
        r = send("Runtime.evaluate", {"expression": "1+1", "returnByValue": True})
        lat_ms = (time.perf_counter() - t0) * 1000
        latencies.append(lat_ms)

    ws.close()

    return {
        "count": n_measurements,
        "min_ms": round(min(latencies), 3),
        "max_ms": round(max(latencies), 3),
        "avg_ms": round(statistics.mean(latencies), 3),
        "median_ms": round(statistics.median(latencies), 3),
        "p95_ms": round(sorted(latencies)[int(n_measurements * 0.95)], 3),
        "all_ms": [round(l, 3) for l in latencies],
    }


def measure_dom_size(tab_id: str) -> dict:
    ws_url = get_ws_url(tab_id)
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

    # Taille du HTML
    r_html = send("Runtime.evaluate", {
        "expression": "document.documentElement.outerHTML.length",
        "returnByValue": True
    })
    html_size = r_html.get("result", {}).get("result", {}).get("value", 0)

    # Nombre d'éléments DOM
    r_dom = send("Runtime.evaluate", {
        "expression": "document.querySelectorAll('*').length",
        "returnByValue": True
    })
    dom_count = r_dom.get("result", {}).get("result", {}).get("value", 0)

    ws.close()
    return {"html_size_bytes": html_size, "dom_element_count": dom_count}


def main():
    tab_id = sys.argv[1] if len(sys.argv) > 1 else None
    n_measurements = int(sys.argv[2]) if len(sys.argv) > 2 else 10

    results = []

    # 1. Compter les onglets
    all_tabs, gemini_tabs = get_gemini_tabs()
    results.append(proof_record(
        action="DIAG_COMPTER_ONGLETS",
        target=f"CDP port {CDP_PORT}",
        state_before="sans_mesure",
        state_after=f"total_tabs={len(all_tabs)} gemini_tabs={len(gemini_tabs)}",
        exit_code=0,
        sha256_before="",
        sha256_after=sha256(json.dumps(all_tabs, sort_keys=True)),
        skill="cdp_latence_diagnostic",
        intent_hash="0xSKILL_CDP_LATENCE_DIAGNOSTIC_20261125",
    ))

    # 2. Sélectionner l'onglet Gemini pour le diagnostic
    if not gemini_tabs:
        print(json.dumps({"ok": False, "error": "Aucun onglet Gemini trouvé"}, indent=2))
        sys.exit(1)

    target_tab_id = tab_id or gemini_tabs[0]["id"]

    # 3. Mesurer la taille du DOM
    dom_info = measure_dom_size(target_tab_id)
    results.append(proof_record(
        action="DIAG_MESURER_DOM_GEMINI",
        target=f"onglet {target_tab_id}",
        state_before="sans_mesure",
        state_after=f"dom_elements={dom_info['dom_element_count']} html_size={dom_info['html_size_bytes']}",
        exit_code=0,
        sha256_before="",
        sha256_after=sha256(json.dumps(dom_info, sort_keys=True)),
        skill="cdp_latence_diagnostic",
        intent_hash="0xSKILL_CDP_LATENCE_DIAGNOSTIC_20261125",
    ))

    # 4. Mesurer la latence CDP
    latency_info = measure_cdp_latency(target_tab_id, n_measurements)
    results.append(proof_record(
        action="DIAG_MESURER_LATENCE_CDP",
        target=f"onglet {target_tab_id} ({n_measurements} mesures)",
        state_before="sans_mesure",
        state_after=f"avg={latency_info['avg_ms']}ms min={latency_info['min_ms']}ms max={latency_info['max_ms']}ms p95={latency_info['p95_ms']}ms",
        exit_code=0,
        sha256_before="",
        sha256_after=sha256(json.dumps(latency_info, sort_keys=True)),
        skill="cdp_latence_diagnostic",
        intent_hash="0xSKILL_CDP_LATENCE_DIAGNOSTIC_20261125",
    ))

    report = {
        "diagnostic": "CDP_LATENCE_DIAGNOSTIC",
        "environment": "ENV2_HP_Z600_Shard_G",
        "timestamp_utc": now_utc(),
        "tabs": {
            "total_count": len(all_tabs),
            "gemini_count": len(gemini_tabs),
            "all_tabs": all_tabs,
        },
        "dom": dom_info,
        "latency": latency_info,
        "proof_records": results,
    }

    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()