#!/usr/bin/env python3
"""
check_skill.py — Gate anti-doublon DAX pour la règle skill-citizen-prealable.

Interroge DAX (table entities, entity_type='SKILL', status='active') et
skills-index.json (L4-TOOLS/SKILLS) pour vérifier qu'aucun skill canonique
actif ne couvre déjà le besoin exprimé.

Usage :
    python check_skill.py --need "<besoin>" [--dax-db <chemin>] [--skills-index <chemin>]

Retour (stdout) :
    EXISTING_SKILL:<nom>   -> un skill actif couvre le besoin, bloquer le inline
    NO_ACTIVE_SKILL        -> aucun skill actif, autoriser la creation

Exit code : 0 = ok, 1 = erreur, 2 = skill existant trouve
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_DAX_DB = Path("D:/DO/WEB/TOOLS/L1-INFRA/DAX/data/skills_database.db")
DEFAULT_SKILLS_INDEX = Path("D:/DO/WEB/TOOLS/L4-TOOLS/SKILLS/skills-index.json")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def hash_sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_skills_index(path: Path) -> dict:
    if not path.exists():
        print(f"ERREUR: skills-index.json introuvable : {path}", file=sys.stderr)
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("skills", {})


def tokenize(text: str) -> list[str]:
    """Decoupe un texte en tokens significatifs (3+ caracteres, alnum)."""
    import re
    return [t for t in re.split(r"[^a-z0-9]+", text.lower()) if len(t) >= 3]


def matches_needle(haystack: str, need: str) -> bool:
    """Verifie si au moins un token du besoin est present dans le haystack."""
    tokens = tokenize(need)
    if not tokens:
        return False
    return any(t in haystack for t in tokens)


def query_dax(dax_db: Path, need: str) -> list[dict]:
    """Recherche dans DAX un skill actif dont le name, l'intent_hash ou les triggers matchent le besoin."""
    if not dax_db.exists():
        return []
    conn = sqlite3.connect(str(dax_db))
    cur = conn.cursor()
    cur.execute(
        """SELECT name, intent_hash, status, stratum, triggers, anti_triggers, description
           FROM entities
           WHERE entity_type = 'SKILL' AND status = 'active'""",
    )
    rows = cur.fetchall()
    conn.close()
    haystack_needle = need.lower()
    results = []
    for r in rows:
        haystack = f"{r[0]} {r[1] or ''} {r[4] or ''} {r[6] or ''}".lower()
        if matches_needle(haystack, haystack_needle):
            results.append(
                {
                    "name": r[0],
                    "intent_hash": r[1],
                    "status": r[2],
                    "stratum": r[3],
                    "triggers": r[4] or "",
                    "anti_triggers": r[5] or "",
                    "description": r[6] or "",
                }
            )
    return results


def query_skills_index(skills: dict, need: str) -> list[dict]:
    """Recherche dans skills-index.json un skill actif dont le name ou les triggers matchent le besoin."""
    results = []
    for name, data in skills.items():
        status = data.get("status", "active")
        if status != "active":
            continue
        triggers = data.get("trigger") or data.get("triggers", [])
        if isinstance(triggers, str):
            triggers = [triggers]
        description = data.get("description", "")
        haystack = f"{name} {data.get('intent_hash', '')} {' '.join(triggers)} {description}".lower()
        if matches_needle(haystack, need.lower()):
            results.append(
                {
                    "name": name,
                    "intent_hash": data.get("intent_hash", ""),
                    "status": status,
                    "stratum": data.get("stratum", data.get("layer", "")),
                    "triggers": ",".join(triggers),
                    "anti_triggers": ",".join(data.get("anti_triggers", []) if isinstance(data.get("anti_triggers"), list) else [data.get("anti_triggers", "")]),
                    "description": description,
                }
            )
    return results


def record_proof(dax_db: Path, entity_name: str, entity_type: str, result: str, exit_code: int, files_modified: str = "") -> None:
    """Enregistre une preuve d'exécution dans la table entity_usage_log de DAX."""
    if not dax_db.exists():
        return
    try:
        conn = sqlite3.connect(str(dax_db))
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO entity_usage_log
               (entity_name, entity_type, shard_id, result, exit_code, hash_sha256, files_modified, timestamp_utc)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                entity_name,
                entity_type,
                "G",
                result,
                exit_code,
                hash_sha256(f"{entity_name}|{result}|{now_iso()}"),
                files_modified,
                now_iso(),
            ),
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"WARN: enregistrement preuve DAX echec : {e}", file=sys.stderr)


def main() -> int:
    parser = argparse.ArgumentParser(description="Gate anti-doublon DAX (skill-citizen-prealable)")
    parser.add_argument("--need", required=True, help="Besoin exprime (mots-cles de recherche)")
    parser.add_argument("--dax-db", type=Path, default=DEFAULT_DAX_DB, help="Chemin vers la DB DAX")
    parser.add_argument("--skills-index", type=Path, default=DEFAULT_SKILLS_INDEX, help="Chemin vers skills-index.json")
    args = parser.parse_args()

    need = args.need

    # 1. Requete DAX
    dax_results = query_dax(args.dax_db, need)

    # 2. Requete skills-index.json
    skills = load_skills_index(args.skills_index)
    index_results = query_skills_index(skills, need)

    # Fusionner (dedup par name)
    seen = set()
    existing = []
    for r in dax_results + index_results:
        if r["name"] not in seen:
            seen.add(r["name"])
            existing.append(r)

    if existing:
        # Un skill actif couvre le besoin -> bloquer le inline
        best = existing[0]
        record_proof(args.dax_db, best["name"], "SKILL", "BLOCKED_INLINE", 2, files_modified="")
        print(f"EXISTING_SKILL:{best['name']}")
        print(f"  intent_hash : {best['intent_hash']}")
        print(f"  stratum     : {best['stratum']}")
        print(f"  triggers    : {best['triggers']}")
        print(f"  description : {best['description']}")
        return 2

    # Aucun skill actif -> autoriser la creation
    record_proof(args.dax_db, "dax-skill-citizen-prealable", "SKILL", "NO_ACTIVE_SKILL", 0, files_modified="")
    print("NO_ACTIVE_SKILL")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
