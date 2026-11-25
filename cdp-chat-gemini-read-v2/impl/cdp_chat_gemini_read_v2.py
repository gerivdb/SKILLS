#!/usr/bin/env python3
"""
cdp_chat_gemini_read_v2.py — Lecture de la réponse assistant du chat Gemini via CDP.
Utilise le sélecteur DOM actuel : div.markdown-main-panel.md-content.
Usage: python cdp_chat_gemini_read_v2.py [cdp_tab_id] [timeout_sec] [poll_interval_ms] [stability_polls]
"""

import sys
import json
import hashlib
import time
import websocket
import urllib.request
from datetime import datetime, timezone

CDP_PORT = 9222
GEMINI_URL_PATTERN = "gemini.google.com"
SELECTOR = "div.markdown-main-panel.md-content"


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def get_gemini_tab_id() -> str:
    """Trouve l'ID de l'onglet Gemini via l'API CDP."""
    resp = urllib.request.urlopen(f"http://127.0.0.1:{CDP_PORT}/json/list", timeout=10)
    tabs = json.load(resp)
    for t in tabs:
        url = t.get("url", "")
        if GEMINI_URL_PATTERN in url and t.get("type") == "page":
            return t.get("id")
    raise RuntimeError("Aucun onglet Gemini trouvé sur le port CDP")


def get_ws_url(tab_id: str) -> str:
    """Récupère l'URL WebSocket de debug pour un onglet donné."""
    resp = urllib.request.urlopen(f"http://127.0.0.1:{CDP_PORT}/json", timeout=10)
    tabs = json.load(resp)
    for t in tabs:
        if t.get("id") == tab_id:
            return t.get("webSocketDebuggerUrl")
    raise RuntimeError(f"Onglet {tab_id} introuvable")


def cdp_send(ws, method: str, params: dict, cid_counter: list) -> dict:
    """Envoie une commande CDP et attend la réponse correspondante."""
    cid_counter[0] += 1
    cid = cid_counter[0]
    msg = {"id": cid, "method": method, "params": params or {}}
    ws.send(json.dumps(msg))
    while True:
        raw = ws.recv()
        resp = json.loads(raw)
        if resp.get("id") == cid:
            return resp


def read_assistant_response(
    tab_id: str | None = None,
    timeout_sec: int = 120,
    poll_interval_ms: int = 1000,
    stability_polls: int = 2,
) -> dict:
    """Lit la réponse assistant Gemini avec détection de stabilité via CDP."""
    if tab_id is None:
        tab_id = get_gemini_tab_id()

    ws_url = get_ws_url(tab_id)
    ws = websocket.create_connection(ws_url, timeout=30)
    cid_counter = [0]

    try:
        cdp_send(ws, "Page.enable", {}, cid_counter)
        cdp_send(ws, "Runtime.enable", {}, cid_counter)

        # Polling loop with stability detection
        start_time = time.time()
        stable_count = 0
        previous_text = ""
        last_text = ""

        while (time.time() - start_time) < timeout_sec:
            expression = (
                f"var els = document.querySelectorAll('{SELECTOR}');"
                f"if(els.length === 0) {{ 'no_elements'; }}"
                f"{{ var last = els[els.length - 1]; last.innerText.trim(); }}"
            )
            resp = cdp_send(
                ws,
                "Runtime.evaluate",
                {"expression": expression, "returnByValue": True},
                cid_counter,
            )

            result = resp.get("result", {})
            value = result.get("result", {}).get("value", "")
            exception = result.get("result", {}).get("exceptionDetails")

            if exception:
                return {
                    "ok": False,
                    "error": f"CDP evaluate exception: {exception}",
                    "cdp_tab_id": tab_id,
                }

            if "no_elements" in str(value):
                time.sleep(poll_interval_ms / 1000.0)
                continue

            current_text = str(value).strip()

            if current_text == previous_text:
                stable_count += 1
            else:
                stable_count = 0

            previous_text = current_text
            last_text = current_text

            if stable_count >= stability_polls:
                break

            time.sleep(poll_interval_ms / 1000.0)

        if stable_count < stability_polls:
            return {
                "ok": False,
                "error": f"Stabilité non atteinte après {timeout_sec}s (dernier texte: {last_text[:80]}...)",
                "cdp_tab_id": tab_id,
                "partial_response": last_text,
            }

        return {
            "ok": True,
            "skill": "cdp-chat-gemini-read-v2",
            "playground": "gemini",
            "selector": SELECTOR,
            "response": last_text,
            "response_length": len(last_text),
            "sha256_response": sha256(last_text),
            "stability_polls": stable_count,
            "timestamp_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "cdp_tab_id": tab_id,
        }
    finally:
        ws.close()


def main():
    tab_id = sys.argv[1] if len(sys.argv) > 1 else None
    timeout_sec = int(sys.argv[2]) if len(sys.argv) > 2 else 120
    poll_interval_ms = int(sys.argv[3]) if len(sys.argv) > 3 else 1000
    stability_polls = int(sys.argv[4]) if len(sys.argv) > 4 else 2

    result = read_assistant_response(tab_id, timeout_sec, poll_interval_ms, stability_polls)
    print(json.dumps(result, indent=2, ensure_ascii=False))

    if not result.get("ok"):
        sys.exit(1)


if __name__ == "__main__":
    main()
