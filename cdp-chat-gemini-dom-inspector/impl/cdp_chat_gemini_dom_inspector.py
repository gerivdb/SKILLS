#!/usr/bin/env python3
"""
cdp_chat_gemini_dom_inspector.py — Inspection du DOM de l'onglet Gemini via CDP.
Découvre les sélecteurs CSS réels des messages assistant.
Usage: python cdp_chat_gemini_dom_inspector.py [cdp_tab_id] [max_elements]
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


def inspect_dom(tab_id: str | None = None, max_elements: int = 50) -> dict:
    """Inspecte le DOM de l'onglet Gemini pour trouver les éléments candidats 'message assistant'."""
    if tab_id is None:
        tab_id = get_gemini_tab_id()

    ws_url = get_ws_url(tab_id)
    ws = websocket.create_connection(ws_url, timeout=30)
    cid_counter = [0]

    try:
        cdp_send(ws, "Page.enable", {}, cid_counter)
        cdp_send(ws, "Runtime.enable", {}, cid_counter)

        expression = (
            "(() => {"
            "  const candidates = [];"
            "  const seen = new Set();"
            "  const add = (el) => {"
            "    const key = el.tagName + '|' + el.className + '|' + el.getAttribute('role');"
            "    if (seen.has(key)) return;"
            "    seen.add(key);"
            "    candidates.push({"
            "      tag: el.tagName,"
            "      role: el.getAttribute('role'),"
            "      class: el.className,"
            "      'aria-label': el.getAttribute('aria-label'),"
            "      'data-message-author-role': el.getAttribute('data-message-author-role'),"
            "      innerText: el.innerText ? el.innerText.substring(0, 120) : null,"
            "      children: el.children.length"
            "    });"
            "  };"
            "  // Chercher par rôle assistant/article/region"
            "  document.querySelectorAll('[role]').forEach(el => {"
            "    const role = el.getAttribute('role');"
            "    if (role && (role.includes('assistant') || role.includes('article') || role.includes('region'))) {"
            "      add(el);"
            "    }"
            "  });"
            "  // Chercher par classe contenant message/assistant/model"
            "  document.querySelectorAll('[class*=\"message\"], [class*=\"assistant\"], [class*=\"model\"]').forEach(el => {"
            "    add(el);"
            "  });"
            "  return candidates.slice(0, " + str(max_elements) + ");"
            "})()"
        )

        resp = cdp_send(
            ws,
            "Runtime.evaluate",
            {"expression": expression, "returnByValue": True},
            cid_counter,
        )

        result = resp.get("result", {})
        value = result.get("result", {}).get("value", [])
        exception = result.get("result", {}).get("exceptionDetails")

        if exception:
            return {
                "ok": False,
                "error": f"CDP evaluate exception: {exception}",
                "cdp_tab_id": tab_id,
            }

        dump_hash = sha256(json.dumps(value, ensure_ascii=False))

        return {
            "ok": True,
            "skill": "cdp-chat-gemini-dom-inspector",
            "playground": "gemini",
            "elements": value,
            "element_count": len(value),
            "dom_dump_sha256": dump_hash,
            "timestamp_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "cdp_tab_id": tab_id,
        }
    finally:
        ws.close()


def main():
    tab_id = sys.argv[1] if len(sys.argv) > 1 else None
    max_elements = int(sys.argv[2]) if len(sys.argv) > 2 else 50

    result = inspect_dom(tab_id, max_elements)
    print(json.dumps(result, indent=2, ensure_ascii=False))

    if not result.get("ok"):
        sys.exit(1)


if __name__ == "__main__":
    main()
