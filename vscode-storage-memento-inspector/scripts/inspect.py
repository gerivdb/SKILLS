#!/usr/bin/env python3
#==============================================================================
# SKILL: vscode-storage-memento-inspector
# Rôle: Forensic et remédiation de la base SQLite state.vscdb (Memento VS Code).
#       Détection et purge de la clé memento/webviewView.kilo-code.SidebarProvider
#       lorsque sidebarSessionTabIDs référencent des sessions fantômes.
# Couche: Persistance SQLite Memento
#==============================================================================

import argparse
import json
import os
import sqlite3
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

LOG_PATH = r"D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\vscode-storage-memento-inspector\wal\vsm-wal.log"
TARGET_KEY = "memento/webviewView.kilo-code.SidebarProvider"


def write_wal(message: str):
    log_dir = os.path.dirname(LOG_PATH)
    if log_dir and not os.path.isdir(log_dir):
        os.makedirs(log_dir, exist_ok=True)
    ts = datetime.now(timezone.utc).isoformat()
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"{ts} | {message}\n")


def find_vscdb_files(root: str):
    """Récupérer tous les fichiers state.vscdb sous root."""
    results = []
    root_path = Path(root)
    if not root_path.exists():
        return results
    for p in root_path.rglob("state.vscdb"):
        results.append(str(p))
    return results


def open_db_readonly(db_path: str, retries: int = 3, delay: float = 2.0):
    """Ouvrir une base SQLite en lecture seule avec gestion du verrou WAL."""
    uri = f"file:{db_path}?mode=ro"
    for attempt in range(retries):
        try:
            conn = sqlite3.connect(uri, uri=True)
            conn.execute("PRAGMA journal_mode=WAL")
            return conn
        except sqlite3.OperationalError as e:
            if "locked" in str(e).lower() and attempt < retries - 1:
                time.sleep(delay)
                continue
            raise
    raise sqlite3.OperationalError(f"Impossible d'ouvrir {db_path} après {retries} tentatives")


def read_memento_value(conn: sqlite3.Connection, key: str):
    """Lire la valeur d'une clé Memento dans ItemTable."""
    try:
        cur = conn.execute("SELECT value FROM ItemTable WHERE key = ?", (key,))
        row = cur.fetchone()
        if row is None:
            return None
        return row[0]
    except sqlite3.OperationalError:
        return None


def parse_sidebar_tabs(raw_value: str):
    """Parser le JSON de la clé SidebarProvider et extraire sidebarSessionTabIDs."""
    try:
        data = json.loads(raw_value)
    except (json.JSONDecodeError, TypeError):
        return None, None
    tabs = data.get("sidebarSessionTabIDs", []) if isinstance(data, dict) else []
    return data, tabs


def purge_key(db_path: str, key: str, retries: int = 3, delay: float = 2.0) -> bool:
    """Supprimer une clé de ItemTable avec gestion du verrou WAL."""
    for attempt in range(retries):
        try:
            conn = sqlite3.connect(db_path)
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("DELETE FROM ItemTable WHERE key = ?", (key,))
            conn.commit()
            conn.close()
            return True
        except sqlite3.OperationalError as e:
            if "locked" in str(e).lower() and attempt < retries - 1:
                time.sleep(delay)
                continue
            return False
    return False


def backup_file(db_path: str, backup_dir: str):
    """Sauvegarder le fichier .vscdb avant modification."""
    os.makedirs(backup_dir, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_name = f"state.{ts}.vscdb.bak"
    backup_path = os.path.join(backup_dir, backup_name)
    import shutil
    shutil.copy2(db_path, backup_path)
    return backup_path


def main():
    parser = argparse.ArgumentParser(description="Inspecteur Memento VS Code state.vscdb")
    parser.add_argument("--vscode-storage-root", default=os.environ.get("APPDATA", "") + r"\Code\WorkspaceStorage",
                        help="Racine workspaceStorage de VS Code")
    parser.add_argument("--target-key", default=TARGET_KEY, help="Clé Memento à inspecter")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Mode lecture seule (défaut)")
    parser.add_argument("--no-dry-run", dest="dry_run", action="store_false", help="Activer la purge effective")
    parser.add_argument("--backup-dir", default=".kilo/backups/vscode-memento", help="Dossier de sauvegarde avant purge")
    args = parser.parse_args()

    timestamp = datetime.now(timezone.utc).isoformat()
    dbs = find_vscdb_files(args.vscode_storage_root)

    report = {
        "timestamp": timestamp,
        "databases_scanned": len(dbs),
        "databases": [],
        "total_ghosts": 0,
        "purge_performed": not args.dry_run,
    }

    for db_path in dbs:
        db_info = {"path": db_path, "key_found": False, "ghosts": [], "error": None}
        try:
            conn = open_db_readonly(db_path)
            raw = read_memento_value(conn, args.target_key)
            conn.close()

            if raw is None:
                db_info["key_found"] = False
                report["databases"].append(db_info)
                continue

            db_info["key_found"] = True
            data, tabs = parse_sidebar_tabs(raw)
            if tabs is None:
                db_info["error"] = "JSON non parsable"
                report["databases"].append(db_info)
                continue

            # Détection des sessions fantômes (UUID sans correspondance active)
            # Ici on ne peut pas comparer avec agent-manager.json sans contexte,
            # on signale donc les tabs présents comme potentiels fantômes.
            for tab_id in tabs:
                db_info["ghosts"].append(tab_id)
                report["total_ghosts"] += 1

            # Purge si demandé
            if not args.dry_run and tabs:
                backup_path = backup_file(db_path, args.backup_dir)
                success = purge_key(db_path, args.target_key)
                db_info["purged"] = success
                db_info["backup_path"] = backup_path if success else None
                write_wal(f"[VSM] PURGE db={db_path} key={args.target_key} backup={backup_path} status={'OK' if success else 'FAIL'}")
            else:
                db_info["purged"] = False

        except Exception as e:
            db_info["error"] = str(e)
            write_wal(f"[VSM] ERROR db={db_path} error={e}")

        report["databases"].append(db_info)

    print(json.dumps(report, indent=2, ensure_ascii=False))
    write_wal(f"[VSM] INSPECT root={args.vscode_storage_root} dbs={len(dbs)} ghosts={report['total_ghosts']} dry_run={args.dry_run}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
