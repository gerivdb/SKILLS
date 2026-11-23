#!/usr/bin/env python3
# =============================================================================
# keep-x-import-simple.py — Import de notes Google Keep via citizen_keep_importer
#
# Utilise le script existant citizen_keep_importer.py (scraping DOM via CDP)
# pour extraire les notes de Google Keep et les injecter dans DuckDB.
#
# Politique :
# - Zéro dépendance gkeepapi
# - Zéro dialogue LLM requis
# - Déduplication par hash SHA-256
# - Merkle seal WAL-0x243
# =============================================================================
from __future__ import annotations

import sys
from pathlib import Path

# Ajout du répertoire ENV3-repo/scripts au PYTHONPATH
ENV3_SCRIPTS = r"D:\DO\WEB\TOOLS\L0-CANON\ENV3-repo\scripts"
if ENV3_SCRIPTS not in sys.path:
    sys.path.insert(0, ENV3_SCRIPTS)

from citizen_keep_importer import CitizenKeepImporter  # noqa: E402

DUCKDB_PATH = r"D:\DO\WEB\TOOLS\L0-CANON\ENV3-repo\WAL\do_core_inference.duckdb"
WAL_SEAL = "WAL-0x243-KEEP-IMPORT-SIMPLE"


def main() -> int:
    importer = CitizenKeepImporter()
    try:
        result = importer.import_notes(max_notes=20)
        import json
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0 if result["status"] == "ok" else 1
    except Exception as exc:  # noqa: BLE001
        print(f"[ERREUR] {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())