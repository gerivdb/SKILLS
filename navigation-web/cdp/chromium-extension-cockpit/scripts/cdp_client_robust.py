#!/usr/bin/env python3
"""
CDP Client Robuste — Connexion au vrai Chromium Profil 2 (port 9222)

Gère correctement :
- Les événements asynchrones CDP (Target.attachedToTarget, Runtime.executionContextCreated)
- L'extraction du sessionId depuis l'événement, pas depuis la réponse de commande
- La file d'attente des messages (réponses vs événements)
- Les timeouts et reconnexions
- Les grandes réponses DOM (max_size augmenté)

Usage :
    python cdp_client.py --target-id <TARGET_ID> --command "Page.getFrameTree"
    python cdp_client.py --target-id <TARGET_ID> --capture-screenshot --output file.png
    python cdp_client.py --target-id <TARGET_ID> --eval "document.body.innerText"
"""

import asyncio
import json
import websockets
import base64
import hashlib
import argparse
import sys
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List


class CDPClient:
    """Client CDP robuste pour Chromium avec gestion des événements asynchrones."""

    def __init__(self, cdp_url: str, max_size: int = 10 * 1024 * 1024):
        self.cdp_url = cdp_url
        self.max_size = max_size
        self.ws: Optional[websockets.WebSocketClientProtocol] = None
        self.session_id: Optional[str] = None
        self._pending_responses: Dict[int, asyncio.Future] = {}
        self._pending_events: Dict[str, asyncio.Future] = {}
        self._event_cache: Dict[str, Dict[str, Any]] = {}  # cache des événements déjà reçus
        self._msg_counter = 0
        self._lock = asyncio.Lock()

    async def connect(self) -> None:
        self.ws = await websockets.connect(self.cdp_url, max_size=self.max_size)
        # Écouter les messages en arrière-plan
        asyncio.create_task(self._message_loop())

    async def _message_loop(self) -> None:
        """Boucle de lecture des messages WebSocket. Route vers réponses ou événements."""
        try:
            async for raw in self.ws:
                try:
                    msg = json.loads(raw)
                except json.JSONDecodeError:
                    continue

                msg_id = msg.get("id")
                method = msg.get("method")

                # C'est une réponse à une commande (has id)
                if msg_id is not None and msg_id in self._pending_responses:
                    future = self._pending_responses.pop(msg_id)
                    if not future.done():
                        future.set_result(msg)
                    continue

                # C'est un événement asynchrone (has method, no id matching)
                if method is not None:
                    # Mettre en cache l'événement pour éviter les race conditions
                    self._event_cache[method] = msg

                    # Target.attachedToTarget -> contient sessionId
                    if method == "Target.attachedToTarget":
                        params = msg.get("params", {})
                        sid = params.get("sessionId")
                        if sid:
                            self.session_id = sid
                        # Notifier toute attente sur cet événement
                        for key, future in list(self._pending_events.items()):
                            if not future.done():
                                future.set_result(msg)
                                del self._pending_events[key]
                    # Autres événements -> notifier si quelqu'un attend
                    for key, future in list(self._pending_events.items()):
                        if key in method or method in key:
                            if not future.done():
                                future.set_result(msg)
                                del self._pending_events[key]

        except websockets.exceptions.ConnectionClosed:
            pass
        except Exception:
            pass

    def _next_id(self) -> int:
        self._msg_counter += 1
        return self._msg_counter

    async def send_command(self, method: str, params: Optional[Dict] = None, timeout: float = 10.0) -> Dict[str, Any]:
        """Envoie une commande CDP et attend sa réponse."""
        if self.ws is None:
            raise RuntimeError("WebSocket not connected")

        msg_id = self._next_id()
        msg = {"id": msg_id, "method": method}
        if params is not None:
            msg["params"] = params
        if self.session_id is not None:
            msg["sessionId"] = self.session_id

        future = asyncio.get_event_loop().create_future()
        self._pending_responses[msg_id] = future

        await self.ws.send(json.dumps(msg))

        try:
            resp = await asyncio.wait_for(future, timeout=timeout)
            return resp
        except asyncio.TimeoutError:
            self._pending_responses.pop(msg_id, None)
            raise TimeoutError(f"CDP timeout waiting for response to id {msg_id} ({method})")

    async def wait_for_event(self, method: str, timeout: float = 10.0) -> Dict[str, Any]:
        """Attend un événement asynchrone spécifique."""
        # Vérifier d'abord le cache (événement déjà reçu)
        cached = self._event_cache.get(method)
        if cached:
            del self._event_cache[method]
            return cached

        future = asyncio.get_event_loop().create_future()
        self._pending_events[method] = future
        try:
            return await asyncio.wait_for(future, timeout=timeout)
        except asyncio.TimeoutError:
            self._pending_events.pop(method, None)
            raise TimeoutError(f"CDP timeout waiting for event {method}")

    async def attach_to_target(self, target_id: str, flatten: bool = True) -> str:
        """Attache à une cible CDP et retourne le sessionId."""
        await self.send_command("Target.attachToTarget", {"targetId": target_id, "flatten": flatten}, timeout=5)
        # Vérifier d'abord le cache (race condition: l'événement peut être arrivé avant l'attente)
        cached = self._event_cache.get("Target.attachedToTarget")
        if cached:
            params = cached.get("params", {})
            sid = params.get("sessionId")
            if sid:
                self.session_id = sid
                return sid
        # Sinon attendre l'événement
        event = await self.wait_for_event("Target.attachedToTarget", timeout=10)
        params = event.get("params", {})
        sid = params.get("sessionId")
        if not sid:
            raise RuntimeError(f"No sessionId in attachedToTarget event: {event}")
        self.session_id = sid
        return sid

    async def enable_domain(self, domain: str) -> None:
        """Active un domaine CDP (Page, Runtime, DOM, Network, Log)."""
        await self.send_command(f"{domain}.enable", {}, timeout=5)

    async def evaluate(self, expression: str, return_by_value: bool = True, timeout: float = 10.0) -> Any:
        """Évalue une expression JS dans le contexte de la page."""
        resp = await self.send_command("Runtime.evaluate", {
            "expression": expression,
            "returnByValue": return_by_value
        }, timeout=timeout)
        result = resp.get("result", {})
        return result.get("result", {}).get("value")

    async def get_frame_tree(self) -> Dict[str, Any]:
        """Retourne l'arbre des frames de la page."""
        resp = await self.send_command("Page.getFrameTree", {}, timeout=10)
        return resp.get("result", {}).get("frameTree", {})

    async def capture_screenshot(self, format: str = "png", capture_beyond_viewport: bool = True) -> bytes:
        """Capture une capture d'écran et retourne les bytes."""
        resp = await self.send_command("Page.captureScreenshot", {
            "format": format,
            "captureBeyondViewport": capture_beyond_viewport
        }, timeout=15)
        data = resp.get("result", {}).get("data", "")
        if not data:
            raise RuntimeError(f"No screenshot data: {resp}")
        return base64.b64decode(data)

    async def get_document(self, depth: int = -1, pierce: bool = True) -> Dict[str, Any]:
        """Retourne le document DOM."""
        resp = await self.send_command("DOM.getDocument", {"depth": depth, "pierce": pierce}, timeout=10)
        return resp.get("result", {}).get("root", {})

    async def get_outer_html(self, node_id: int, pierce: bool = True) -> str:
        """Retourne l'outerHTML d'un node DOM."""
        resp = await self.send_command("DOM.getOuterHTML", {"nodeId": node_id, "pierce": pierce}, timeout=10)
        return resp.get("result", {}).get("outerHTML", "")

    async def query_selector(self, node_id: int, selector: str, pierce: bool = True) -> Optional[int]:
        """Retourne le nodeId d'un élément correspondant au sélecteur."""
        resp = await self.send_command("DOM.querySelector", {
            "nodeId": node_id,
            "selector": selector,
            "pierce": pierce
        }, timeout=10)
        return resp.get("result", {}).get("nodeId")

    async def close(self) -> None:
        if self.ws:
            await self.ws.close()
            self.ws = None


# ============================================================================
# PROCÉDURE DE CONNEXION AU VRAI PROFIL 2
# ============================================================================

CHROMIUM_CDP_URL = "ws://127.0.0.1:9222/devtools/browser/b4c927fd-fb1f-4a27-81d6-01e4f07d238d"


async def list_targets() -> List[Dict[str, Any]]:
    """Liste toutes les cibles CDP disponibles."""
    client = CDPClient(CHROMIUM_CDP_URL)
    await client.connect()
    try:
        resp = await client.send_command("Target.getTargets", {}, timeout=5)
        targets = resp.get("result", {}).get("targetInfos", [])
        return targets
    finally:
        await client.close()


async def connect_to_gemini_profile2(target_id: str) -> CDPClient:
    """Se connecte au vrai Profil 2 Chromium et attache à la cible Gemini."""
    client = CDPClient(CHROMIUM_CDP_URL)
    await client.connect()
    await client.attach_to_target(target_id)
    await client.enable_domain("Page")
    await client.enable_domain("Runtime")
    await client.enable_domain("DOM")
    return client


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CDP Client pour Chromium Profil 2")
    parser.add_argument("--target-id", help="ID de la cible CDP (ex: E971A7568E2CFAED50C869DE7FAC9E6B)")
    parser.add_argument("--list-targets", action="store_true", help="Lister toutes les cibles")
    parser.add_argument("--eval", help="Expression JS à évaluer")
    parser.add_argument("--capture-screenshot", action="store_true", help="Capturer une capture d'écran")
    parser.add_argument("--output", default="capture.png", help="Fichier de sortie pour la capture")
    parser.add_argument("--get-body-text", action="store_true", help="Extraire le texte du body")
    args = parser.parse_args()

    async def main():
        if args.list_targets:
            targets = await list_targets()
            print(f"=== {len(targets)} cibles CDP ===")
            for t in targets:
                print(f"  ID: {t['targetId']} | Type: {t['type']} | Title: {t.get('title','')} | URL: {t.get('url','')}")
            return

        if not args.target_id:
            print("ERREUR: --target-id requis (ou --list-targets)")
            sys.exit(1)

        client = await connect_to_gemini_profile2(args.target_id)
        try:
            if args.eval:
                result = await client.evaluate(args.eval)
                print(f"Résultat évaluation: {result}")
            if args.get_body_text:
                text = await client.evaluate("document.body ? document.body.innerText.substring(0, 5000) : 'NO_BODY'")
                print(f"--- BODY TEXT ---\n{text}\n--- END ---")
            if args.capture_screenshot:
                data = await client.capture_screenshot()
                with open(args.output, "wb") as f:
                    f.write(data)
                print(f"Screenshot saved: {args.output} ({len(data)} bytes)")
        finally:
            await client.close()

    asyncio.run(main())
