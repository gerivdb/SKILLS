#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ccp_telemetry_ingester.py — Ingester de télémétrie CDP pour le Chromium Control Plane.

Maintenant une connexion WebSocket asynchrone vers le port CDP (9222 par défaut) et
ingère en continu les événements :
  - Runtime.exceptionThrown (stack traces des Service Workers d'extensions)
  - Console.messageAdded (console.error / console.warn / console.log)
  - Log.entryAdded (violations de sécurité, avertissements moteur Chromium)

Chaque événement est corrélé à une extension via son ID Chrome
(`chrome-extension://<id>/...`) et écrit dans la table `telemetry_events` de
`chromium_meta.db` avec batching (flush toutes les 250 ms ou 50 événements).

Usage :
    python ccp_telemetry_ingester.py [--port 9222] [--db-path ...] [--once]

Nécessite : `websockets` (`pip install websockets`) et un Chromium écoutant
sur le port CDP (auto-spawn géré par le cockpit si le port est fermé).
"""

import argparse
import asyncio
import json
import re
import sqlite3
import sys
import time
from pathlib import Path
from typing import Optional

try:
    import websockets
except ImportError:
    websockets = None

DB_PATH = Path(__file__).resolve().parent / "chromium_meta.db"
CDP_URL = "ws://127.0.0.1:9222/devtools/browser"
BATCH_INTERVAL_MS = 250
BATCH_MAX_SIZE = 50

# Mapping des niveaux CDP vers nos niveaux internes
LEVEL_MAP = {
    "error": "error",
    "warning": "warning",
    "log": "info",
    "info": "info",
    "debug": "debug",
}

# Regex pour extraire l'ID d'extension depuis une URL chrome-extension://
EXT_ID_RE = re.compile(r"chrome-extension://([a-z]{32})")


# ---------------------------------------------------------------------------
# Base de données
# ---------------------------------------------------------------------------
def get_db() -> sqlite3.Connection:
    """Ouvre une connexion SQLite en mode WAL (lectures simultanées autorisées)."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.row_factory = sqlite3.Row
    return conn


def resolve_extension_id(conn: sqlite3.Connection, extension_id_chrome: str) -> Optional[int]:
    """Corrèle un ID Chrome (32 caractères) vers l'ID interne de la table extensions."""
    row = conn.execute(
        "SELECT id FROM extensions WHERE slug = ? OR manifest_path LIKE ?",
        (extension_id_chrome, f"%{extension_id_chrome}%"),
    ).fetchone()
    return row["id"] if row else None


def insert_event(conn: sqlite3.Connection, ext_id: Optional[int], source: str,
                 level: str, message: str, stack_trace: Optional[str] = None) -> None:
    """Insère un événement de télémétrie."""
    conn.execute(
        """INSERT INTO telemetry_events
           (extension_id, source, level, message, stack_trace)
           VALUES (?, ?, ?, ?, ?)""",
        (ext_id, source, level, message, stack_trace),
    )


# ---------------------------------------------------------------------------
# Extraction de l'ID d'extension depuis un message ou une URL
# ---------------------------------------------------------------------------
def extract_extension_id(text: str) -> Optional[str]:
    """Cherche un ID Chrome (32 caractères) dans un texte brut."""
    m = EXT_ID_RE.search(text)
    return m.group(1) if m else None


# ---------------------------------------------------------------------------
# Ingester principal
# ---------------------------------------------------------------------------
class TelemetryIngester:
    def __init__(self, cdp_url: str = CDP_URL, db_path: Path = DB_PATH):
        self.cdp_url = cdp_url
        self.db_path = db_path
        self._buffer: list[tuple] = []
        self._last_flush = 0.0
        self._running = False

    def _flush(self, conn: sqlite3.Connection) -> None:
        if not self._buffer:
            return
        conn.executemany(
            """INSERT INTO telemetry_events
               (extension_id, source, level, message, stack_trace)
               VALUES (?, ?, ?, ?, ?)""",
            self._buffer,
        )
        conn.commit()
        self._buffer.clear()
        self._last_flush = time.time()

    def _should_flush(self) -> bool:
        now = time.time()
        return (len(self._buffer) >= BATCH_MAX_SIZE or
                (self._buffer and (now - self._last_flush) * 1000 >= BATCH_INTERVAL_MS))

    def _add_event(self, ext_id: Optional[int], source: str, level: str,
                   message: str, stack_trace: Optional[str] = None) -> None:
        self._buffer.append((ext_id, source, level, message, stack_trace))
        if self._should_flush():
            conn = get_db()
            try:
                self._flush(conn)
            finally:
                conn.close()

    async def _handle_message(self, message: dict, conn: sqlite3.Connection) -> None:
        method = message.get("method", "")
        params = message.get("params", {})

        if method == "Runtime.exceptionThrown":
            detail = params.get("exceptionDetails", {})
            text = detail.get("text", "")
            stack = detail.get("stackTrace", {})

            # Extraire l'ID d'extension depuis l'URL ou le texte
            url = detail.get("url", "")
            ext_id_chrome = extract_extension_id(url) or extract_extension_id(text)
            ext_id = resolve_extension_id(conn, ext_id_chrome) if ext_id_chrome else None

            # Reconstruire un stack trace lisible
            frames = []
            for cf in stack.get("callFrames", []):
                frames.append(f"{cf.get('url', '')}:{cf.get('lineNumber', 0)}:{cf.get('columnNumber', 0)} "
                              f"in {cf.get('functionName', '?')}")
            stack_trace = "\n".join(frames) if frames else None

            self._add_event(
                ext_id=ext_id,
                source="runtime",
                level="error",
                message=text or "Uncaught exception",
                stack_trace=stack_trace,
            )

        elif method == "Console.messageAdded":
            msg = params.get("message", {})
            level = LEVEL_MAP.get(msg.get("level", "log"), "info")
            text = msg.get("text", "")
            url = msg.get("url", "")

            ext_id_chrome = extract_extension_id(url) or extract_extension_id(text)
            ext_id = resolve_extension_id(conn, ext_id_chrome) if ext_id_chrome else None

            # Ne pas logger les messages de niveau "log" sauf s'ils viennent d'une extension
            if level == "info" and not ext_id:
                return

            self._add_event(
                ext_id=ext_id,
                source="console",
                level=level,
                message=text,
            )

        elif method == "Log.entryAdded":
            entry = params.get("entry", {})
            level = LEVEL_MAP.get(entry.get("level", "info"), "info")
            text = entry.get("text", "")
            source = entry.get("source", "")

            ext_id_chrome = extract_extension_id(text) or extract_extension_id(source)
            ext_id = resolve_extension_id(conn, ext_id_chrome) if ext_id_chrome else None

            self._add_event(
                ext_id=ext_id,
                source=source or "log",
                level=level,
                message=text,
            )

    async def run(self) -> None:
        """Boucle principale d'ingestion CDP."""
        if websockets is None:
            print("[ERREUR] Le module 'websockets' n'est pas installé. Exécutez : pip install websockets")
            return

        self._running = True
        print(f"[INFO] Connexion CDP vers {self.cdp_url} ...")

        async with websockets.connect(self.cdp_url) as ws:
            # Activer les domaines CDP pertinents
            await ws.send(json.dumps({"id": 1, "method": "Runtime.enable"}))
            await ws.send(json.dumps({"id": 2, "method": "Console.enable"}))
            await ws.send(json.dumps({"id": 3, "method": "Log.enable"}))
            await ws.send(json.dumps({"id": 4, "method": "Target.setDiscoverTargets", "params": {"discover": True}}))
            print("[SUCCÈS] Domaines CDP activés. Ingestion en cours...")

            conn = get_db()
            try:
                while self._running:
                    try:
                        raw = await asyncio.wait_for(ws.recv(), timeout=1.0)
                    except asyncio.TimeoutError:
                        # Flush périodique même sans message
                        self._flush(conn)
                        continue

                    try:
                        message = json.loads(raw)
                    except json.JSONDecodeError:
                        continue

                    # Ignorer les réponses aux commandes (id présent)
                    if "id" in message and "method" not in message:
                        continue

                    await self._handle_message(message, conn)

                    # Flush si le buffer est plein
                    if self._should_flush():
                        self._flush(conn)
            finally:
                self._flush(conn)
                conn.close()
                print("\n[INFO] Ingestion arrêtée proprement.")

    def stop(self) -> None:
        self._running = False


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingester de télémétrie CDP pour le CCP")
    parser.add_argument("--port", type=int, default=9222, help="Port CDP de Chromium")
    parser.add_argument("--db-path", type=str, default=str(DB_PATH), help="Chemin vers chromium_meta.db")
    parser.add_argument("--once", action="store_true", help="Exécuter un seul cycle puis quitter (test)")
    args = parser.parse_args()

    db_path = Path(args.db_path)
    if not db_path.exists():
        print(f"[ERREUR] Base CCP introuvable : {db_path}. Exécutez d'abord init_db.py --reset")
        sys.exit(1)

    cdp_url = f"ws://127.0.0.1:{args.port}/devtools/browser"
    ingester = TelemetryIngester(cdp_url=cdp_url, db_path=db_path)

    try:
        asyncio.run(ingester.run())
    except KeyboardInterrupt:
        ingester.stop()
        print("\n[INFO] Arrêt demandé par l'utilisateur.")


if __name__ == "__main__":
    main()
