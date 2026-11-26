#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
init_db.py — Initialisation de la base Chromium Control Plane (chromium_meta.db).

Lit le schéma SQL et crée/remet à zéro la base relationnelle unifiée du CCP.
"""

import sqlite3
from pathlib import Path

SCHEMA_PATH = Path(__file__).resolve().parent / "chromium_meta_schema.sql"
DB_PATH = Path(__file__).resolve().parent / "chromium_meta.db"


def init_db(reset: bool = False) -> None:
    """Crée la base à partir du schéma SQL.

    Args:
        reset: si True, supprime le fichier .db existant avant recréation.
    """
    if reset and DB_PATH.exists():
        DB_PATH.unlink()
        print(f"[INFO] Ancienne base supprimée : {DB_PATH}")

    schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.executescript(schema_sql)
        conn.commit()
        print(f"[SUCCÈS] Base CCP initialisée : {DB_PATH}")
        print(f"[INFO]   Schéma appliqué : {SCHEMA_PATH}")
    finally:
        conn.close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Initialise la base CCP (chromium_meta.db)")
    parser.add_argument("--reset", action="store_true", help="Supprime la base existante avant recréation")
    args = parser.parse_args()
    init_db(reset=args.reset)
