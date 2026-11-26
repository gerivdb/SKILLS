#!/usr/bin/env python3
"""
cdp_tunnel_persistant.py — Tunnel WebSocket CDP persistant pour écriture sur Chromium.
Élimine la réouverture de connexion à chaque opération.
Usage: python cdp_tunnel_persistant.py "<prompt>" [cdp_tab_id] [keep_alive]
"""

import sys
import json
import hashlib
import websocket
import urllib.request
from datetime import datetime, timezone

CDP_PORT = 9222
GEMINI_URL_PATTERN = "gemini.google.com"


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def get_gemini_tab_id() -> str:
    resp = urllib.request.urlopen(f"http://127.0.0.1:{CDP_PORT}/json/list", timeout=10)
    tabs = json.load(resp)
    for t in tabs:
        url = t.get("url", "")
        if GEMINI_URL_PATTERN in url and t.get("type") == "page":
            return t.get("id")
    raise RuntimeError("Aucun onglet Gemini trouvé sur le port CDP")


def get_ws_url(tab_id: str) -> str:
    resp = urllib.request.urlopen(f"http://127.0.0.1:{CDP_PORT}/json", timeout=10)
    tabs = json.load(resp)
    for t in tabs:
        if t.get("id") == tab_id:
            return t.get("webSocketDebuggerUrl")
    raise RuntimeError(f"Onglet {tab_id} introuvable")


class CdpTunnel:
    def __init__(self, tab_id: str):
        self.tab_id = tab_id
        self.ws_url = get_ws_url(tab_id)
        self.ws = None
        self.cid_counter = [0]
        self.opened = False

    def open(self):
        self.ws = websocket.create_connection(self.ws_url, timeout=30)
        self._send("Page.enable", {})
        self._send("Runtime.enable", {})
        self.opened = True

    def _send(self, method: str, params: dict) -> dict:
        self.cid_counter[0] += 1
        cid = self.cid_counter[0]
        msg = {"id": cid, "method": method, "params": params or {}}
        self.ws.send(json.dumps(msg))
        while True:
            raw = self.ws.recv()
            resp = json.loads(raw)
            if resp.get("id") == cid:
                return resp

    def evaluate(self, expression: str) -> dict:
        if not self.opened:
            self.open()
        resp = self._send("Runtime.evaluate", {"expression": expression, "returnByValue": True})
        result = resp.get("result", {}).get("result", {})
        exception = result.get("exceptionDetails")
        value = result.get("value", "")
        return {"ok": exception is None, "value": value, "exception": exception}

    def close(self):
        if self.ws:
            self.ws.close()
            self.opened = False


def inject_and_send(prompt: str, selector: str, tab_id: str | None = None) -> dict:
    if tab_id is None:
        tab_id = get_gemini_tab_id()

    tunnel = CdpTunnel(tab_id)
    tunnel.open()

    try:
        # Injecter le prompt
        inject_expr = (
            f"var input = document.querySelector('{selector}');"
            f"if(input) {{ input.focus(); input.textContent = {json.dumps(prompt)};"
            f"input.innerText = {json.dumps(prompt)};"
            f"var ev = new Event('input', {{bubbles: true}}); input.dispatchEvent(ev);"
            f"'ok:' + input.textContent.length + ' chars'; }} else 'selector_not_found'"
        )
        inject_res = tunnel.evaluate(inject_expr)
        if not inject_res["ok"] or "selector_not_found" in str(inject_res["value"]):
            return {"ok": False, "error": inject_res.get("exception", inject_res["value"]), "cdp_tab_id": tab_id}

        # Cliquer sur Envoyer
        send_expr = (
            "var btn = document.querySelector('button[aria-label=\"Envoyer un message\"]');"
            "if(btn) { btn.focus(); btn.click(); 'clicked'; } else 'button_not_found'"
        )
        send_res = tunnel.evaluate(send_expr)
        if not send_res["ok"] or "button_not_found" in str(send_res["value"]):
            return {"ok": False, "error": send_res.get("exception", send_res["value"]), "cdp_tab_id": tab_id}

        return {
            "ok": True,
            "skill": "cdp-tunnel-persistant",
            "playground": "gemini",
            "inject_result": inject_res["value"],
            "send_result": send_res["value"],
            "connections_used": 1,
            "connections_saved": 2,
            "timestamp_utc": now_utc(),
            "cdp_tab_id": tab_id,
        }
    finally:
        tunnel.close()


def main():
    if len(sys.argv) < 2:
        print("Usage: python cdp_tunnel_persistant.py \"<prompt>\" [cdp_tab_id]")
        sys.exit(1)

    prompt = sys.argv[1]
    tab_id = sys.argv[2] if len(sys.argv) > 2 else None

    result = inject_and_send(prompt, "div.ql-editor.textarea", tab_id)
    print(json.dumps(result, indent=2, ensure_ascii=False))

    if not result.get("ok"):
        sys.exit(1)


if __name__ == "__main__":
    main()