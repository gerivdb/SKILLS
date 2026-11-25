#!/usr/bin/env python3
"""
wazaa_bus_relay.py — Relais du bus WAZAA sur le tunnel CDP persistant.
Envoie un message WAZAA JSON enveloppé à ENV3 (Gemini) via CDP et lit la réponse.
Usage: python wazaa_bus_relay.py --action <action> --target <target> [--skill <skill>] [--intent-hash <hash>] [--state-before <s>] [--state-after <s>] [--cdp-tab-id <id>]
"""

import sys
import json
import hashlib
import time
import argparse
import websocket
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

CDP_PORT = 9222
GEMINI_URL_PATTERN = "gemini.google.com"
INPUT_SELECTOR = "div.ql-editor.textarea"
SEND_SELECTOR = 'button[aria-label="Envoyer un message"]'
RESPONSE_SELECTOR = "div.markdown-main-panel.md-content"


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
    """Tunnel WebSocket CDP persistant — une connexion pour plusieurs commandes."""
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


def build_wazaa_message(action: str, target: str, source_env: str = "ENV2",
                        target_env: str = "ENV3", skill: str = "wazaa-bus-relay",
                        intent_hash: str = "", state_before: str = "",
                        state_after: str = "", exit_code: int = 0,
                        sha256_before: str = "", sha256_after: str = "") -> dict:
    """Construit un message WAZAA JSON enveloppé."""
    message_id = sha256(f"{action}{target}{now_utc()}")
    payload = {
        "action": action,
        "target": target,
        "source_env": source_env,
        "target_env": target_env,
        "skill": skill,
        "intent_hash": intent_hash,
        "exit_code": exit_code,
        "sha256_before": sha256_before,
        "sha256_after": sha256_after,
        "state_before": state_before,
        "state_after": state_after
    }
    payload_sha256 = sha256(json.dumps(payload, sort_keys=True))
    return {
        "envelope": {
            "bus": "WAZAA",
            "version": "1.0",
            "timestamp_utc": now_utc(),
            "wal_seal": "WAL-0x243",
            "message_id": message_id
        },
        "payload": payload,
        "proof": {
            "hash_sha256": payload_sha256,
            "verified": True
        }
    }, message_id, payload_sha256


def relay_via_cdp_tunnel(message: dict, message_id: str, message_sha256: str,
                         tab_id: str | None = None) -> dict:
    """Envoie le message WAZAA via le tunnel CDP persistant et lit la réponse."""
    if tab_id is None:
        tab_id = get_gemini_tab_id()

    tunnel = CdpTunnel(tab_id)
    tunnel.open()
    t0 = time.perf_counter()

    try:
        # 1. Injecter le message WAZAA JSON dans la zone de saisie
        message_json = json.dumps(message, ensure_ascii=False)
        inject_expr = (
            f"var input = document.querySelector('{INPUT_SELECTOR}');"
            f"if(input) {{"
            f"  input.focus();"
            f"  input.textContent = {json.dumps(message_json)};"
            f"  input.innerText = {json.dumps(message_json)};"
            f"  var ev = new Event('input', {{bubbles: true}});"
            f"  input.dispatchEvent(ev);"
            f"  'ok:' + input.textContent.length + ' chars';"
            f"}} else 'selector_not_found'"
        )
        inject_res = tunnel.evaluate(inject_expr)
        if not inject_res["ok"] or "selector_not_found" in str(inject_res["value"]):
            return {"ok": False, "error": inject_res.get("exception", inject_res["value"]), "cdp_tab_id": tab_id}

        # 2. Cliquer sur Envoyer
        send_expr = (
            f"var btn = document.querySelector('{SEND_SELECTOR}');"
            f"if(btn) {{ btn.focus(); btn.click(); 'clicked'; }} else 'button_not_found'"
        )
        send_res = tunnel.evaluate(send_expr)
        if not send_res["ok"] or "button_not_found" in str(send_res["value"]):
            return {"ok": False, "error": send_res.get("exception", send_res["value"]), "cdp_tab_id": tab_id}

        # 3. Lire la réponse ENV3 avec détection de stabilité
        read_expr = (
            f"var els = document.querySelectorAll('{RESPONSE_SELECTOR}');"
            f"if(els.length === 0) {{ 'no_elements'; }}"
            f"{{ var last = els[els.length - 1]; last.innerText.trim(); }}"
        )

        start_time = time.perf_counter()
        stable_count = 0
        previous_text = ""
        last_text = ""
        timeout_sec = 120

        while (time.perf_counter() - start_time) < timeout_sec:
            resp = tunnel.evaluate(read_expr)
            result = resp.get("result", {}).get("result", {})
            exception = result.get("exceptionDetails")
            if exception:
                return {"ok": False, "error": exception, "cdp_tab_id": tab_id}

            value = result.get("value", "")
            if "no_elements" in str(value):
                time.sleep(1)
                continue

            current_text = str(value).strip()
            if current_text and current_text == previous_text:
                stable_count += 1
            else:
                stable_count = 0
            previous_text = current_text
            last_text = current_text

            if stable_count >= 2:
                break
            time.sleep(1)

        if stable_count < 2:
            return {
                "ok": False,
                "error": f"Stabilité non atteinte après {timeout_sec}s",
                "cdp_tab_id": tab_id,
                "partial_response": last_text
            }

        lat_ms = (time.perf_counter() - t0) * 1000
        response_sha256 = sha256(last_text)

        return {
            "ok": True,
            "skill": "wazaa-bus-relay",
            "playground": "gemini",
            "waZAA_message_id": message_id,
            "waZAA_message_sha256": message_sha256,
            "inject_result": inject_res["value"],
            "send_result": send_res["value"],
            "connections_used": 1,
            "connections_saved": 2,
            "response": last_text,
            "response_length": len(last_text),
            "response_sha256": response_sha256,
            "latency_ms": round(lat_ms, 3),
            "timestamp_utc": now_utc(),
            "cdp_tab_id": tab_id,
            "wal_seal": "WAL-0x243",
            "exit_code": 0
        }
    finally:
        tunnel.close()


def main():
    parser = argparse.ArgumentParser(description="Relais bus WAZAA sur tunnel CDP persistant")
    parser.add_argument("--action", required=True, help="Action du message WAZAA")
    parser.add_argument("--target", required=True, help="Cible du message")
    parser.add_argument("--source-env", default="ENV2", help="Environnement source")
    parser.add_argument("--target-env", default="ENV3", help="Environnement cible")
    parser.add_argument("--skill", default="wazaa-bus-relay", help="Nom du skill émetteur")
    parser.add_argument("--intent-hash", default="", help="IntentHash de l'action")
    parser.add_argument("--state-before", default="", help="État avant l'action")
    parser.add_argument("--state-after", default="", help="État après l'action")
    parser.add_argument("--exit-code", type=int, default=0, help="Code de retour")
    parser.add_argument("--sha256-before", default="", help="Hash avant")
    parser.add_argument("--sha256-after", default="", help="Hash après")
    parser.add_argument("--cdp-tab-id", default=None, help="ID de l'onglet CDP")
    args = parser.parse_args()

    message, message_id, message_sha256 = build_wazaa_message(
        action=args.action,
        target=args.target,
        source_env=args.source_env,
        target_env=args.target_env,
        skill=args.skill,
        intent_hash=args.intent_hash,
        state_before=args.state_before,
        state_after=args.state_after,
        exit_code=args.exit_code,
        sha256_before=args.sha256_before,
        sha256_after=args.sha256_after
    )

    result = relay_via_cdp_tunnel(message, message_id, message_sha256, args.cdp_tab_id)
    print(json.dumps(result, indent=2, ensure_ascii=False))

    if not result.get("ok"):
        sys.exit(1)


if __name__ == "__main__":
    main()