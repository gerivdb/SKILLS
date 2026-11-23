#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cdp_proxy_mitm.py — Skill chromium-profile-2 (Shard B, Pilier 2)
Proxy MitM CDP : écoute sur 9223, forward vers Chromium 9222,
journalise toutes les trames JSON-RPC (BDCP Guardian).

Usage:
    python cdp_proxy_mitm.py          # lance le proxy (bloquant)
    python cdp_proxy_mitm.py --once   # un seul cycle puis sortie (test)
"""

from __future__ import annotations

import asyncio
import json
import logging
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

import websockets
from websockets.server import serve

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
PROXY_PORT = 9223
CHROMIUM_PORT = 9222
CHROMIUM_HOST = "127.0.0.1"
LOG_DIR = Path(__file__).resolve().parent / "proxy_logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / f"cdp_proxy_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.jsonl"

# Règles BDCP : commandes bloquées (non autorisées)
BDCP_BLOCKED_DOMAINS: set[str] = set()
BDCP_BLOCKED_METHODS: set[str] = {
    # Exemple : bloquer Network.setBlockedURLs (modification du comportement réseau)
    "Network.setBlockedURLs",
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [CDP-PROXY] %(levelname)s: %(message)s",
)


def log_frame(direction: str, frame: Dict[str, Any], ws_id: str):
    """Écrit une trame JSON-RPC dans le log journalier."""
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "direction": direction,  # "client->chromium" ou "chromium->client"
        "ws_id": ws_id,
        "frame": frame,
    }
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def bdcp_check(frame: Dict[str, Any]) -> tuple[bool, Optional[str]]:
    """
    Vérifie si une trame est autorisée par les règles BDCP.
    Retourne (autorisé, raison_blocage_si_refuse).
    """
    method = frame.get("method", "")
    # Vérifier les méthodes bloquées
    for blocked in BDCP_BLOCKED_METHODS:
        if method == blocked or method.startswith(blocked + "."):
            return False, f"Méthode BDCP bloquée: {method}"
    return True, None


async def discover_cdp_ws_url() -> str:
    """Découvre l'URL WebSocket CDP de Chromium via l'endpoint HTTP /json/version."""
    import urllib.request

    url = f"http://{CHROMIUM_HOST}:{CHROMIUM_PORT}/json/version"
    with urllib.request.urlopen(url, timeout=5) as r:
        data = json.loads(r.read().decode())
    ws_url = data.get("webSocketDebuggerUrl")
    if not ws_url:
        raise RuntimeError("Aucune webSocketDebuggerUrl retournée par Chromium")
    return ws_url


async def proxy_websocket(websocket, path):
    """Proxy une connexion WebSocket client vers Chromium CDP."""
    ws_id = str(uuid.uuid4())[:8]
    logging.info(f"[{ws_id}] Nouvelle connexion client sur {path}")

    # Découvrir l'URL CDP de Chromium
    try:
        cdp_ws_url = await discover_cdp_ws_url()
        logging.info(f"[{ws_id}] Connexion CDP Chromium: {cdp_ws_url}")
    except Exception as e:
        logging.error(f"[{ws_id}] Impossible de découvrir l'URL CDP: {e}")
        await websocket.close(code=1011, reason=str(e))
        return

    # Connexion vers Chromium
    try:
        async with websockets.connect(cdp_ws_url) as cdp_ws:
            logging.info(f"[{ws_id}] Connecté à Chromium CDP")

            async def client_to_chromium():
                """Transfert client → Chromium avec vérification BDCP."""
                try:
                    async for message in websocket:
                        try:
                            frame = json.loads(message)
                        except json.JSONDecodeError:
                            # Trame non-JSON : forward tel quel
                            await cdp_ws.send(message)
                            log_frame("client->chromium", {"raw": message[:500]}, ws_id)
                            continue

                        allowed, reason = bdcp_check(frame)
                        if not allowed:
                            logging.warning(f"[{ws_id}] BDCP BLOC: {reason}")
                            # Envoyer une erreur CDP au client au lieu de forward
                            error_response = {
                                "jsonrpc": "2.0",
                                "id": frame.get("id"),
                                "error": {
                                    "code": -32603,
                                    "message": f"BDCP blocked: {reason}",
                                },
                            }
                            await websocket.send(json.dumps(error_response))
                            continue

                        log_frame("client->chromium", frame, ws_id)
                        await cdp_ws.send(message)
                except websockets.ConnectionClosed:
                    pass

            async def chromium_to_client():
                """Transfert Chromium → client avec journalisation."""
                try:
                    async for message in cdp_ws:
                        try:
                            frame = json.loads(message)
                        except json.JSONDecodeError:
                            await websocket.send(message)
                            log_frame("chromium->client", {"raw": message[:500]}, ws_id)
                            continue

                        log_frame("chromium->client", frame, ws_id)
                        await websocket.send(message)
                except websockets.ConnectionClosed:
                    pass

            # Exécuter les deux directions en parallèle
            await asyncio.gather(
                client_to_chromium(),
                chromium_to_client(),
            )

    except Exception as e:
        logging.error(f"[{ws_id}] Erreur connexion Chromium: {e}")
        try:
            await websocket.close(code=1011, reason=str(e))
        except Exception:
            pass

    logging.info(f"[{ws_id}] Connexion fermée")


async def main():
    logging.info(f"Démarrage proxy CDP MitM sur ws://127.0.0.1:{PROXY_PORT}")
    logging.info(f"Target Chromium: ws://127.0.0.1:{CHROMIUM_PORT}")
    logging.info(f"Logs: {LOG_FILE}")

    async with serve(proxy_websocket, "127.0.0.1", PROXY_PORT):
        logging.info(f"Proxy en écoute sur le port {PROXY_PORT}")
        await asyncio.Future()  # Run forever


if __name__ == "__main__":
    if "--once" in sys.argv:
        # Mode test : un seul cycle
        async def test_once():
            try:
                url = await discover_cdp_ws_url()
                print(f"CDP WS URL découvert: {url}")
            except Exception as e:
                print(f"Erreur: {e}")
                sys.exit(1)

        asyncio.run(test_once())
    else:
        asyncio.run(main())
