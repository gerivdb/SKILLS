#!/usr/bin/env python3
"""
inject_qwen_m3.py — Injection unique dans une conversation Qwen via CDP natif (port 9222).
Zéro Playwright. Une connexion WebSocket pour l'injection, une pour la lecture.
Conforme à l'économie d'API : pas de polling, pas de requêtes répétées.

Conforme à la règle Absolute Portability : ressources adjacentes localisées via
Path(__file__).parent, zéro dépendance à os.getcwd().
"""

import argparse
import asyncio
import json
import sys
import urllib.request
import websockets
from pathlib import Path

WS_URL = None


def discover_qwen_target():
    """Récupère la target CDP dont l'URL contient qwen.ai sur le port 9222."""
    global WS_URL
    with urllib.request.urlopen("http://127.0.0.1:9222/json", timeout=5) as resp:
        targets = json.loads(resp.read().decode("utf-8"))
    for t in targets:
        if "qwen.ai" in t.get("url", ""):
            WS_URL = t["webSocketDebuggerUrl"]
            return t
    return None


DEFAULT_MESSAGE = """Bonjour. Je suis Kilo (ENV2), architecte de l'écosystème gerivdb. J'ai complété une réflexion procédurale M3 sur les scénarios d'accès aux LLMs externes et le contournement de quotas (BDCP, profils éphémères vs profil 2 authentifié, CDP natif port 9222). Le document est sur disque à D:\\DO\\WEB\\TOOLS\\L0-CANON\\ENV3-repo\\M3-REFLEXION-PROCEDURALE-SCENARIOS-GOST.md.

Je souhaite que nous co-construisions le meilleur procédé pour éviter l'amnésie et le contournement de quotas.

Pouvez-vous identifier les lacunes de ce document et proposer le meilleur procédé pour :
1. Maintenir la distinction BDCP réseau (localhost:18000) vs routage Gateway (localhost:13378) ?
2. Empêcher le contournement de quota par profils éphémères ?
3. Intégrer cette réflexion dans GOST de façon pérenne ?

Répondez factuellement et concisement. Une seule réponse suffit."""

INJECT_JS_TEMPLATE = """
(function() {
    var sel = ['textarea', '[role="textbox"]', 'input[type="text"]', 'div[contenteditable="true"]'];
    var input = null;
    for (var i = 0; i < sel.length; i++) {
        input = document.querySelector(sel[i]);
        if (input) break;
    }
    if (!input) return 'NO_INPUT_FOUND';
    input.focus();
    input.value = {message};
    input.dispatchEvent(new Event('input', {{bubbles: true}}));
    input.dispatchEvent(new Event('change', {{bubbles: true}}));
    var ke = new KeyboardEvent('keydown', {{key: 'Enter', code: 'Enter', bubbles: true}});
    input.dispatchEvent(ke);
    return 'INJECTED_AND_SUBMITTED';
})();
"""


async def cdp_eval(expression):
    """Se connecte en WebSocket à la target Qwen et évalue une expression JS."""
    async with websockets.connect(WS_URL) as ws:
        await ws.send(json.dumps({"id": 1, "method": "Runtime.evaluate", "params": {"expression": expression}}))
        res = json.loads(await ws.recv())
        return res


async def inject(message, wait_seconds):
    """Injecte le message dans Qwen, attend, puis lit le DOM."""
    res = await cdp_eval(INJECT_JS_TEMPLATE.replace("{message}", json.dumps(message)))
    value = res.get("result", {}).get("result", {}).get("value", str(res))
    print(f"[INJECTION] {value}")

    print(f"[ATTENTE] Lecture de la réponse Qwen ({wait_seconds} s)...")
    await asyncio.sleep(wait_seconds)

    read_res = await cdp_eval("document.body.innerText")
    text = read_res.get("result", {}).get("result", {}).get("value", "")
    if not text:
        print("[AUCUN TEXTE] La page est vide ou non accessible.")
        sys.exit(0)

    tail = text[-5000:] if len(text) > 5000 else text
    print("--- RÉPONSE QWEN (extrait) ---")
    print(tail)


async def main(message, wait_seconds):
    target = discover_qwen_target()
    if not target:
        print("[ERREUR] Aucune target Qwen trouvée sur 127.0.0.1:9222")
        sys.exit(1)
    print(f"[OK] Target Qwen : {target['id']} | {target.get('url')}")

    await inject(message, wait_seconds)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Injecte un message dans Qwen via CDP 9222 (vrai profil 2)")
    parser.add_argument("--message", dest="message", default=None, help="Message à injecter (défaut : message M3)")
    parser.add_argument("--wait", dest="wait_seconds", type=int, default=20, help="Secondes d'attente après injection (défaut: 20)")
    args = parser.parse_args()

    msg = args.message if args.message else DEFAULT_MESSAGE
    asyncio.run(main(msg, args.wait_seconds))
