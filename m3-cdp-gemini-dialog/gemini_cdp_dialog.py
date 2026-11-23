#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gemini_cdp_dialog.py — Skill m3-cdp-gemini-dialog
Dialogue CDP ENV2 -> Gemini via Profil 2 authentifie (port 9222).
Usage: python gemini_cdp_dialog.py "<message>" [--conv-id <id>] [--timeout <s>]
"""

import argparse
import asyncio
import json
import sys
import time
import urllib.request
import websockets
from datetime import datetime, timezone

CDP_HOST = "127.0.0.1"
CDP_PORT = 9222
CDP_VERSION_URL = "http://" + CDP_HOST + ":" + str(CDP_PORT) + "/json/version"
CDP_LIST_URL = "http://" + CDP_HOST + ":" + str(CDP_PORT) + "/json/list"
INPUT_SELECTOR = 'div[aria-label="Saisissez un prompt pour Gemini"]'
RESPONSE_SELECTOR = "div.response-content"
RESPONSE_SELECTOR_ALT = "div.markdown.markdown-main-panel"


def http_get(url, timeout=5):
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return json.loads(r.read().decode())


def check_cdp_port():
    try:
        info = http_get(CDP_VERSION_URL, timeout=3)
        return True, info
    except Exception as e:
        return False, str(e)


def list_tabs():
    return http_get(CDP_LIST_URL, timeout=5)


def find_gemini_tab(tabs, conv_id=None):
    for t in tabs:
        title = t.get("title", "") or ""
        url = t.get("url", "") or ""
        if conv_id and conv_id in url:
            return t
        if "gemini.google.com" in url or "Gemini" in title:
            return t
    return None


def build_ws_url(tab_id):
    return "ws://" + CDP_HOST + ":" + str(CDP_PORT) + "/devtools/page/" + tab_id


async def cdp_send(ws, method, params=None, msg_id=1):
    msg = {"id": msg_id, "method": method, "params": params or {}}
    await ws.send(json.dumps(msg))
    while True:
        raw = await ws.recv()
        resp = json.loads(raw)
        if resp.get("id") == msg_id:
            return resp


async def evaluate_js(ws, expression, msg_id=1):
    await cdp_send(ws, "Runtime.enable", msg_id=msg_id)
    resp = await cdp_send(ws, "Runtime.evaluate", {
        "expression": expression,
        "returnByValue": True
    }, msg_id=msg_id + 1)
    result = resp.get("result", {}).get("result", {})
    return result.get("value", "")


async def inject_and_read(message, conv_id=None, timeout=60):
    ok, info = check_cdp_port()
    if not ok:
        print("ERREUR: Port CDP " + str(CDP_PORT) + " non accessible: " + info, file=sys.stderr)
        return {"ok": False, "error": "CDP_PORT_UNREACHABLE: " + info}

    tabs = list_tabs()
    tab = find_gemini_tab(tabs, conv_id)
    if not tab:
        print("ERREUR: Aucun onglet Gemini trouve sur le port CDP.", file=sys.stderr)
        return {"ok": False, "error": "GEMINI_TAB_NOT_FOUND"}

    tab_id = tab["id"]
    ws_url = build_ws_url(tab_id)

    async with websockets.connect(ws_url, ping_interval=None) as ws:
        await cdp_send(ws, "Runtime.enable", msg_id=1)

        if not conv_id:
            await cdp_send(ws, "Page.navigate", {"url": "https://gemini.google.com/app"}, msg_id=2)
            await asyncio.sleep(3)

        js_write = (
            "(function(){"
            "const el=document.querySelector(" + json.dumps(INPUT_SELECTOR) + ");"
            "if(el){el.focus();"
            "el.textContent=" + json.dumps(message) + ";"
            "el.dispatchEvent(new Event('input',{bubbles:true}));"
            "el.dispatchEvent(new Event('change',{bubbles:true}));"
            'return "WRITE_OK";}'
            'return "WRITE_ERR";'
            "})()"
        )
        result = await evaluate_js(ws, js_write, msg_id=10)
        if result != "WRITE_OK":
            return {"ok": False, "error": "WRITE_FAILED", "result": result}

        await asyncio.sleep(1)

        await cdp_send(ws, "Input.dispatchKeyEvent", {
            "type": "keyDown", "key": "Enter", "code": "Enter", "windowsVirtualKeyCode": 13
        }, msg_id=20)
        await asyncio.sleep(0.1)
        await cdp_send(ws, "Input.dispatchKeyEvent", {
            "type": "keyUp", "key": "Enter", "code": "Enter", "windowsVirtualKeyCode": 13
        }, msg_id=21)

        js_check = (
            "(function(){"
            "const el=document.querySelector(" + json.dumps(INPUT_SELECTOR) + ");"
            "return el ? el.textContent : 'NOT_FOUND';"
            "})()"
        )
        input_state = await evaluate_js(ws, js_check, msg_id=30)

        deadline = time.time() + timeout
        response_text = ""
        while time.time() < deadline:
            response_text = await evaluate_js(
                ws,
                "(function(){const el=document.querySelector(" + json.dumps(RESPONSE_SELECTOR) + "); return el ? el.textContent : '';})()",
                msg_id=40
            )
            if response_text and len(response_text) > 50:
                break
            response_text = await evaluate_js(
                ws,
                "(function(){const el=document.querySelector(" + json.dumps(RESPONSE_SELECTOR_ALT) + "); return el ? el.textContent : '';})()",
                msg_id=41
            )
            if response_text and len(response_text) > 50:
                break
            await asyncio.sleep(3)

        if not response_text or len(response_text) <= 50:
            return {
                "ok": False,
                "error": "RESPONSE_NOT_FOUND",
                "input_state": input_state,
                "tab_id": tab_id,
                "tab_url": tab.get("url", "")
            }

        return {
            "ok": True,
            "tab_id": tab_id,
            "tab_url": tab.get("url", ""),
            "input_cleared": input_state in ("", "<p><br></p>"),
            "response": response_text,
            "timestamp_utc": datetime.now(timezone.utc).isoformat()
        }


def main():
    parser = argparse.ArgumentParser(description="Dialogue CDP ENV2 -> Gemini via Profil 2")
    parser.add_argument("message", help="Message a envoyer a Gemini")
    parser.add_argument("--conv-id", default=None, help="ID de conversation Gemini (optionnel)")
    parser.add_argument("--timeout", type=int, default=60, help="Timeout en secondes pour attendre la reponse")
    args = parser.parse_args()

    result = asyncio.run(inject_and_read(args.message, args.conv_id, args.timeout))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
