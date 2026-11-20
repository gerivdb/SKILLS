#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ccp_vscode_diagnostics.py — Pont de diagnostics VS Code pour le Chromium Control Plane.

Poll les événements non résolus (level IN ('error', 'warning')) dans
telemetry_events, résout le chemin disque du fichier source via
extensions.manifest_path, et émet sur stdout au format standard VS Code
problemMatcher :

    D:/chemin/fichier.js:42:15: error [sidekeep-x]: WebSocket connection failed

Usage :
    python ccp_vscode_diagnostics.py [--db-path ...] [--poll-interval 2.0] [--once]

Nécessite : chromium_meta.db déjà initialisée (init_db.py --reset).
"""

import argparse
import hashlib
import json
import re
import sqlite3
import sys
import time
from pathlib import Path
from typing import Optional

DB_PATH = Path(__file__).resolve().parent / "chromium_meta.db"

# Format de sortie VS Code problemMatcher :
# <chemin_absolu>:<ligne>:<colonne>: <sévérité> [<code>]: <message>
OUTPUT_RE = re.compile(
    r"^(?P<path>[^:]+):(?P<line>\d+):(?P<col>\d+): "
    r"(?P<severity>error|warning|info) "
    r"\[(?P<code>[^\]]+)\]: (?P<message>.+)$"
)

# Regex pour extraire fichier:ligne:colonne depuis une stack trace JS
STACK_FRAME_RE = re.compile(
    r"(?P<path>[^\n:]+):(?P<line>\d+):(?P<col>\d+)"
)

# Regex pour extraire un ID Chrome depuis une URL ou un texte
EXT_ID_RE = re.compile(r"chrome-extension://([a-z]{32})")


# ---------------------------------------------------------------------------
# Base de données
# ---------------------------------------------------------------------------
def get_db(db_path: Path = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.row_factory = sqlite3.Row
    return conn


def resolve_source_path(conn: sqlite3.Connection, extension_id_chrome: str,
                        relative_path: str) -> Optional[str]:
    """Résout le chemin disque absolu d'un fichier source d'extension.

    La table extensions stocke manifest_path (chemin vers manifest.json).
    Le dossier de l'extension est le parent de manifest.json.
    """
    row = conn.execute(
        "SELECT manifest_path FROM extensions WHERE slug = ? OR manifest_path LIKE ?",
        (extension_id_chrome, f"%{extension_id_chrome}%"),
    ).fetchone()
    if not row:
        return None
    manifest_path = Path(row["manifest_path"])
    ext_dir = manifest_path.parent
    target = (ext_dir / relative_path).resolve()
    if target.exists():
        return str(target)
    return None


def get_unresolved_events(conn: sqlite3.Connection, last_id: int = 0):
    """Récupère les événements non résolus depuis le dernier ID traité."""
    rows = conn.execute(
        """SELECT t.id, t.timestamp, e.slug, t.source, t.level, t.message,
                  t.stack_trace, e.manifest_path
           FROM telemetry_events t
           LEFT JOIN extensions e ON e.id = t.extension_id
           WHERE t.resolved = 0 AND t.level IN ('error', 'warning')
             AND t.id > ?
           ORDER BY t.id ASC""",
        (last_id,),
    ).fetchall()
    return rows


def mark_event_resolved(conn: sqlite3.Connection, event_id: int) -> None:
    conn.execute("UPDATE telemetry_events SET resolved = 1 WHERE id = ?", (event_id,))
    conn.commit()


# ---------------------------------------------------------------------------
# Extraction de la localisation depuis un événement
# ---------------------------------------------------------------------------
def extract_location(message: str, stack_trace: Optional[str]) -> Optional[tuple]:
    """Tente d'extraire (chemin_relatif, ligne, colonne) depuis un message ou une stack trace.

    Retourne (relative_path, line, col) ou None.
    """
    if stack_trace:
        for line in stack_trace.splitlines():
            m = STACK_FRAME_RE.search(line)
            if m:
                return (m.group("path"), int(m.group("line")), int(m.group("col")))

    # Fallback : chercher dans le message brut
    m = STACK_FRAME_RE.search(message)
    if m:
        return (m.group("path"), int(m.group("line")), int(m.group("col")))

    return None


def extract_extension_id_from_text(text: str) -> Optional[str]:
    m = EXT_ID_RE.search(text)
    return m.group(1) if m else None


# ---------------------------------------------------------------------------
# Émission VS Code
# ---------------------------------------------------------------------------
def emit_diagnostic(event_id: int, ext_slug: str, level: str, message: str,
                    source_path: Optional[str], line: int, col: int) -> str:
    """Formate une ligne de diagnostic au format VS Code problemMatcher."""
    severity = "error" if level == "error" else "warning"
    code = ext_slug or "unknown"
    # Échapper les barres obliques inversées pour Windows
    path_str = str(source_path) if source_path else "<inconnu>"
    return f"{path_str}:{line}:{col}: {severity}|{code}|{message}"


def process_event(conn: sqlite3.Connection, row: sqlite3.Row,
                  processed_hashes: set) -> Optional[str]:
    """Traite un événement et retourne la ligne de diagnostic à émettre, ou None."""
    event_id = row["id"]
    ext_slug = row["slug"] or "unknown"
    level = row["level"]
    message = row["message"]
    stack_trace = row["stack_trace"]
    manifest_path = row["manifest_path"]

    # Déduplication par hash du contenu
    content_hash = hashlib.sha256(
        f"{ext_slug}:{level}:{message}:{stack_trace or ''}".encode("utf-8")
    ).hexdigest()
    if content_hash in processed_hashes:
        return None
    processed_hashes.add(content_hash)

    # Résolution du chemin source
    source_path = None
    line = 1
    col = 1

    loc = extract_location(message, stack_trace)
    if loc:
        relative_path, line, col = loc
        # Si on a un manifest_path, résoudre le chemin absolu
        if manifest_path:
            resolved = resolve_source_path(
                conn, ext_slug if ext_slug != "unknown" else "", relative_path
            )
            if resolved:
                source_path = resolved
            else:
                source_path = str(Path(relative_path).resolve()
                                  if Path(relative_path).exists() else relative_path)
        else:
            source_path = str(Path(relative_path).resolve()
                              if Path(relative_path).exists() else relative_path)
    else:
        # Pas de localisation : utiliser le manifest_path comme repère
        if manifest_path:
            source_path = str(Path(manifest_path).parent)

    if not source_path:
        source_path = "<inconnu>"

    # Marquer comme résolu après émission (polling à usage unique)
    mark_event_resolved(conn, event_id)

    return emit_diagnostic(event_id, ext_slug, level, message,
                           source_path, line, col)


# ---------------------------------------------------------------------------
# Boucle principale
# ---------------------------------------------------------------------------
def poll_once(conn: sqlite3.Connection, processed_hashes: set,
              last_id: int) -> tuple[int, int]:
    """Effectue un cycle de poll. Retourne (last_id, nb_diagnostics_emis)."""
    rows = get_unresolved_events(conn, last_id)
    emitted = 0
    new_last_id = last_id
    for row in rows:
        new_last_id = max(new_last_id, row["id"])
        diagnostic = process_event(conn, row, processed_hashes)
        if diagnostic:
            print(diagnostic, flush=True)
            emitted += 1
    return new_last_id, emitted


def run_poll(db_path: Path = DB_PATH, poll_interval: float = 2.0,
             once: bool = False) -> None:
    if not db_path.exists():
        print(f"[ERREUR] Base CCP introuvable : {db_path}. Exécutez d'abord init_db.py --reset",
              file=sys.stderr)
        sys.exit(1)

    conn = get_db(db_path)
    processed_hashes: set = set()
    last_id = 0

    print(f"[INFO] Pont de diagnostics VS Code démarré (poll {poll_interval}s)", file=sys.stderr)
    print("[INFO] Format : chemin:ligne:colonne: sévérité [code]: message", file=sys.stderr)

    try:
        while True:
            last_id, emitted = poll_once(conn, processed_hashes, last_id)
            if once:
                break
            time.sleep(poll_interval)
    except KeyboardInterrupt:
        print("\n[INFO] Arrêt du pont de diagnostics.", file=sys.stderr)
    finally:
        conn.close()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Pont de diagnostics VS Code pour le Chromium Control Plane"
    )
    parser.add_argument("--db-path", type=str, default=str(DB_PATH),
                        help="Chemin vers chromium_meta.db")
    parser.add_argument("--poll-interval", type=float, default=2.0,
                        help="Intervalle de poll en secondes (défaut 2.0)")
    parser.add_argument("--once", action="store_true",
                        help="Effectuer un seul cycle de poll puis quitter")
    args = parser.parse_args()

    run_poll(db_path=Path(args.db_path), poll_interval=args.poll_interval, once=args.once)


if __name__ == "__main__":
    main()
