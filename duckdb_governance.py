#!/usr/bin/env python3
# =============================================================================
# duckdb_governance.py — Métaskill de gouvernance DuckDB (GOVERNANCE-HUB)
#
# Gère les migrations versionnées de la base DuckDB centrale. Lit les fichiers
# SQL dans un dossier db/migrations/ et les applique dans l'ordre, en tenant un
# registre des migrations appliquées (table schema_migrations).
#
# WAL-0x243-DUCKDB-GOVERNANCE-SELFTEST
# =============================================================================
from __future__ import annotations

import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

import duckdb

# On utilise un fichier temporaire pour le test afin d'éviter les verrous
# sur le fichier de production do_core_inference.duckdb.
WAL_SEAL = "WAL-0x243-DUCKDB-GOVERNANCE-SELFTEST"


class DuckDBGovernance:
    """Métaskill de gouvernance DuckDB : migrations versionnées."""

    def __init__(self, db_path: Path, migrations_dir: Path) -> None:
        self.db_path = str(db_path)
        self.migrations_dir = migrations_dir
        self._conn = None

    def connect(self) -> None:
        import duckdb
        self._conn = duckdb.connect(self.db_path)
        self._ensure_migrations_table()

    def _ensure_migrations_table(self) -> None:
        assert self._conn is not None
        self._conn.execute("""
            CREATE TABLE IF NOT EXISTS schema_migrations (
                id VARCHAR PRIMARY KEY,
                migration_name VARCHAR,
                applied_at TIMESTAMP,
                merkle_seal VARCHAR
            )
        """)

    def _get_applied(self) -> set:
        assert self._conn is not None
        rows = self._conn.execute("SELECT migration_name FROM schema_migrations").fetchall()
        return {r[0] for r in rows}

    def _get_pending(self) -> List[Path]:
        if not self.migrations_dir.exists():
            return []
        files = sorted(self.migrations_dir.glob("*.sql"))
        applied = self._get_applied()
        return [f for f in files if f.stem not in applied]

    def apply_migration(self, path: Path) -> None:
        assert self._conn is not None
        sql = path.read_text(encoding="utf-8")
        self._conn.execute(sql)
        self._conn.execute(
            "INSERT INTO schema_migrations (id, migration_name, applied_at, merkle_seal) VALUES (?, ?, ?, ?)",
            (
                path.stem,
                path.stem,
                datetime.now(timezone.utc).isoformat(),
                WAL_SEAL,
            ),
        )

    def apply_all(self) -> List[str]:
        """Applique toutes les migrations en attente."""
        assert self._conn is not None
        pending = self._get_pending()
        applied_names: List[str] = []
        for migration in pending:
            self.apply_migration(migration)
            applied_names.append(migration.stem)
        return applied_names

    def close(self) -> None:
        if self._conn is not None:
            try:
                self._conn.close()
            except Exception:
                pass


def self_test() -> bool:
    """Test auto : crée une migration de test, l'applique, vérifie la colonne."""
    print("[SELF-TEST] duckdb_governance — création d'une migration de test...")
    tmpdir = Path(tempfile.mkdtemp(prefix="webx_duckdb_gov_"))
    migrations_dir = tmpdir / "migrations"
    migrations_dir.mkdir()

    # Créer un fichier DuckDB temporaire pour le test
    test_db = tmpdir / "test.duckdb"

    migration_sql = """
    CREATE TABLE IF NOT EXISTS test_migration_table (
        id VARCHAR PRIMARY KEY,
        name VARCHAR
    );
    """
    migration_file = migrations_dir / "001_test_table.sql"
    migration_file.write_text(migration_sql, encoding="utf-8")

    gov = DuckDBGovernance(db_path=test_db, migrations_dir=migrations_dir)
    try:
        gov.connect()
        applied = gov.apply_all()
        print(f"[SELF-TEST] {len(applied)} migration(s) appliquée(s): {applied}")

        # Vérifier que la table existe
        rows = gov._conn.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_name = 'test_migration_table'"
        ).fetchall()
        if len(rows) > 0:
            print("[SELF-TEST] PASS — duckdb_governance opérationnel.")
            print(f"[SELF-TEST] Sceau : {WAL_SEAL}")
            gov.close()
            return True
        print("[SELF-TEST] FAIL — Table test_migration_table non créée.")
        print(f"[SELF-TEST] Sceau : {WAL_SEAL}")
        gov.close()
        return False
    except Exception as exc:  # noqa: BLE001
        print(f"[SELF-TEST] FAIL — {exc}")
        print(f"[SELF-TEST] Sceau : {WAL_SEAL}")
        gov.close()
        return False
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "--self-test":
        return 0 if self_test() else 1
    print("Usage: python duckdb_governance.py --self-test")
    return 1


if __name__ == "__main__":
    sys.exit(main())
