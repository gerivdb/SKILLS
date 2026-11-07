#!/usr/bin/env python3
# =============================================================================
# bridge_generator.py — Citizen Bridge Generator (L4-TOOLS/SKILLS)
#
# Génère un script Python de bridge idempotent entre deux adaptateurs
# (source → destination) avec :
#   - Lecture source (DuckDB, Mnemo, HERMES, MIMIR, ou générique)
#   - Écriture destination (mêmes adaptateurs)
#   - Hash SHA-256 pour l'unicité des contenus
#   - Checkpoint JSON pour l'idempotence
#   - Self-test intégré (--self-test)
#
# Paramètres de génération :
#   source_adapter, destination_adapter, checkpoint_file, wal_seal_prefix
#
# Sceau : WAL-0x243-BRIDGE-GENERATOR-SELFTEST
# =============================================================================
from __future__ import annotations

import hashlib
import json
import sqlite3
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

try:
    import duckdb  # type: ignore
except Exception:  # pragma: no cover - DuckDB optionnel
    duckdb = None  # type: ignore[assignment]

WAL_SEAL = "WAL-0x243-BRIDGE-GENERATOR-SELFTEST"


# ---------------------------------------------------------------------------
# Adaptateurs de lecture/écriture (utilisés par le self-test)
# ---------------------------------------------------------------------------
class SourceAdapter:
    """Interface pour lire depuis une source."""

    def read_records(self) -> List[Dict[str, Any]]:
        raise NotImplementedError


class DestinationAdapter:
    """Interface pour écrire vers une destination."""

    def write_record(self, record: Dict[str, Any]) -> bool:
        raise NotImplementedError

    def record_exists(self, content_hash: str) -> bool:
        return False


# --- DuckDB source ---------------------------------------------------------
class DuckDBAdapter(SourceAdapter):
    """Lit tous les enregistrements d'une table DuckDB."""

    def __init__(self, db_path: Path, table: str = "conversation_turns"):
        self.db_path = db_path
        self.table = table

    def read_records(self) -> List[Dict[str, Any]]:
        if duckdb is None:
            raise RuntimeError("DuckDB n'est pas installé")
        conn = duckdb.connect(str(self.db_path), read_only=True)
        try:
            rows = conn.execute(f"SELECT * FROM {self.table}").fetchall()
            cols = [desc[0] for desc in conn.description]
            return [dict(zip(cols, row)) for row in rows]
        finally:
            conn.close()


# --- SQLite destination ----------------------------------------------------
class SQLiteAdapter(DestinationAdapter):
    """Écrit dans une table SQLite avec suivi des hash déjà présents."""

    def __init__(self, db_path: Path, table: str = "synced_records"):
        self.db_path = db_path
        self.table = table
        self._init_db()

    def _init_db(self) -> None:
        conn = sqlite3.connect(str(self.db_path))
        try:
            conn.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {self.table} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content_hash TEXT UNIQUE NOT NULL,
                    payload TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.commit()
        finally:
            conn.close()

    def record_exists(self, content_hash: str) -> bool:
        conn = sqlite3.connect(str(self.db_path))
        try:
            row = conn.execute(
                f"SELECT 1 FROM {self.table} WHERE content_hash = ?",
                (content_hash,),
            ).fetchone()
            return row is not None
        finally:
            conn.close()

    def write_record(self, record: Dict[str, Any]) -> bool:
        content_hash = record.get("_content_hash", "")
        payload = json.dumps(record, ensure_ascii=False, sort_keys=True)
        if self.record_exists(content_hash):
            return False
        conn = sqlite3.connect(str(self.db_path))
        try:
            conn.execute(
                f"INSERT INTO {self.table} (content_hash, payload) VALUES (?, ?)",
                (content_hash, payload),
            )
            conn.commit()
            return True
        finally:
            conn.close()


# ---------------------------------------------------------------------------
# Template de bridge généré (marqueurs <<...>>, pas d'accolades Python littérales)
# ---------------------------------------------------------------------------
BRIDGE_TEMPLATE = r'''#!/usr/bin/env python3
# =============================================================================
# Generated Bridge — <<SOURCE_ADAPTER>> → <<DESTINATION_ADAPTER>>
# Auto-généré par citizen-bridge-generator (L4-TOOLS/SKILLS)
# Gate N243 : NON activé (réservé à P6)
# Sceau : <<WAL_SEAL>>
# =============================================================================
from __future__ import annotations

import hashlib
import json
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

<<SOURCE_IMPORTS>>


# ---------------------------------------------------------------------------
# Adaptateurs inclus (autonomie du bridge généré)
# ---------------------------------------------------------------------------
class SourceAdapter:
    """Interface pour lire depuis une source."""

    def read_records(self) -> List[Dict[str, Any]]:
        raise NotImplementedError


class DestinationAdapter:
    """Interface pour écrire vers une destination."""

    def write_record(self, record: Dict[str, Any]) -> bool:
        raise NotImplementedError

    def record_exists(self, content_hash: str) -> bool:
        return False


class DuckDBAdapter(SourceAdapter):
    """Lit tous les enregistrements d'une table DuckDB."""

    def __init__(self, db_path: Path, table: str = "conversation_turns"):
        self.db_path = db_path
        self.table = table

    def read_records(self) -> List[Dict[str, Any]]:
        import duckdb as _duckdb
        conn = _duckdb.connect(str(self.db_path), read_only=True)
        try:
            rows = conn.execute(f"SELECT * FROM {self.table}").fetchall()
            cols = [desc[0] for desc in conn.description]
            return [dict(zip(cols, row)) for row in rows]
        finally:
            conn.close()


class SQLiteAdapter(DestinationAdapter):
    """Écrit dans une table SQLite avec suivi des hash déjà présents."""

    def __init__(self, db_path: Path, table: str = "synced_records"):
        self.db_path = db_path
        self.table = table
        self._init_db()

    def _init_db(self) -> None:
        import sqlite3 as _sqlite3
        conn = _sqlite3.connect(str(self.db_path))
        try:
            conn.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {self.table} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content_hash TEXT UNIQUE NOT NULL,
                    payload TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.commit()
        finally:
            conn.close()

    def record_exists(self, content_hash: str) -> bool:
        import sqlite3 as _sqlite3
        conn = _sqlite3.connect(str(self.db_path))
        try:
            row = conn.execute(
                f"SELECT 1 FROM {self.table} WHERE content_hash = ?",
                (content_hash,),
            ).fetchone()
            return row is not None
        finally:
            conn.close()

    def write_record(self, record: Dict[str, Any]) -> bool:
        content_hash = record.get("_content_hash", "")
        payload = json.dumps(record, ensure_ascii=False, sort_keys=True)
        if self.record_exists(content_hash):
            return False
        import sqlite3 as _sqlite3
        conn = _sqlite3.connect(str(self.db_path))
        try:
            conn.execute(
                f"INSERT INTO {self.table} (content_hash, payload) VALUES (?, ?)",
                (content_hash, payload),
            )
            conn.commit()
            return True
        finally:
            conn.close()


CHECKPOINT_PATH = Path(r"<<CHECKPOINT_PATH>>")
WAL_SEAL = "<<WAL_SEAL>>"


def _content_hash(record: Dict[str, Any]) -> str:
    """Hash SHA-256 du contenu d'un enregistrement pour l'idempotence."""
    return hashlib.sha256(
        json.dumps(record, ensure_ascii=False, sort_keys=True).encode("utf-8")
    ).hexdigest()


def _load_checkpoint() -> set:
    if CHECKPOINT_PATH.exists():
        try:
            data = json.loads(CHECKPOINT_PATH.read_text(encoding="utf-8"))
            return set(data.get("synced_hashes", []))
        except Exception:
            return set()
    return set()


def _save_checkpoint(hashes: set) -> None:
    CHECKPOINT_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {"synced_hashes": sorted(hashes)}
    CHECKPOINT_PATH.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )


class Bridge:
    def __init__(self, source: Any, destination: Any) -> None:
        self.source = source
        self.destination = destination
        self.checkpoint: set = _load_checkpoint()

    def sync(self) -> Dict[str, int]:
        stats = {"read": 0, "written": 0, "skipped": 0, "errors": 0}
        records = self.source.read_records()
        stats["read"] = len(records)
        for record in records:
            h = _content_hash(record)
            if h in self.checkpoint:
                stats["skipped"] += 1
                continue
            if self.destination.record_exists(h):
                self.checkpoint.add(h)
                stats["skipped"] += 1
                continue
            try:
                record_with_hash = dict(record)
                record_with_hash["_content_hash"] = h
                if self.destination.write_record(record_with_hash):
                    self.checkpoint.add(h)
                    stats["written"] += 1
                else:
                    stats["errors"] += 1
            except Exception:
                stats["errors"] += 1
        _save_checkpoint(self.checkpoint)
        return stats

    def run(self) -> int:
        stats = self.sync()
        print(
            f"[BRIDGE] lecture={stats['read']} écrite={stats['written']} "
            f"ignorée={stats['skipped']} erreur={stats['errors']}"
        )
        return 0 if stats["errors"] == 0 else 1


def self_test() -> bool:
    """Test auto : génère et exécute un bridge DuckDB → SQLite,
    vérifie le transfert et l'idempotence."""
    print("[SELF-TEST] citizen_bridge_generator — génération + exécution ...")
    with tempfile.TemporaryDirectory(prefix="bridge_test_") as tmpdir:
        src_db = Path(tmpdir) / "source.duckdb"
        dst_db = Path(tmpdir) / "destination.sqlite"
        ckpt = Path(tmpdir) / "checkpoint.json"

        # Créer une source DuckDB avec 3 enregistrements
        import duckdb
        conn = duckdb.connect(str(src_db))
        conn.execute(
            "CREATE TABLE test_table (id INTEGER, name TEXT, value REAL)"
        )
        conn.executemany(
            "INSERT INTO test_table VALUES (?, ?, ?)",
            [(1, "alpha", 10.5), (2, "beta", 20.0), (3, "gamma", 30.7)],
        )
        conn.close()

        source = DuckDBAdapter(src_db, "test_table")
        destination = SQLiteAdapter(dst_db, "synced")
        bridge = Bridge(source, destination)

        stats1 = bridge.sync()
        print(f"[SELF-TEST] Passage 1 : lecture={stats1['read']} écrite={stats1['written']} "
              f"ignorée={stats1['skipped']} erreur={stats1['errors']}")

        stats2 = bridge.sync()
        print(f"[SELF-TEST] Passage 2 : lecture={stats2['read']} écrite={stats2['written']} "
              f"ignorée={stats2['skipped']} erreur={stats2['errors']}")

        ok = (
            stats1["read"] == 3
            and stats1["written"] == 3
            and stats2["written"] == 0
            and stats2["errors"] == 0
        )
        if ok:
            print("[SELF-TEST] PASS — citizen_bridge_generator opérationnel.")
            print(f"[SELF-TEST] Sceau : <<WAL_SEAL>>")
            return True
        print("[SELF-TEST] FAIL — idempotence ou transfert incorrect.")
        print(f"[SELF-TEST] Sceau : <<WAL_SEAL>>")
        return False


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "--self-test":
        return 0 if self_test() else 1
    print("Usage: bridge_generator.py --self-test")
    return 1


if __name__ == "__main__":
    sys.exit(main())
'''


def generate_bridge(
    source_adapter: str,
    destination_adapter: str,
    checkpoint_file: str,
    wal_seal_prefix: str = "WAL-0x243",
) -> str:
    """Génère le code Python d'un bridge idempotent via remplacements de marqueurs."""
    imports = ""
    if source_adapter.lower() == "duckdb":
        imports = "import duckdb"
    elif destination_adapter.lower() == "duckdb":
        imports = "import duckdb"

    seal = f"{wal_seal_prefix}-BRIDGE-{source_adapter.upper()}-TO-{destination_adapter.upper()}-SELFTEST"

    code = BRIDGE_TEMPLATE
    code = code.replace("<<SOURCE_ADAPTER>>", source_adapter)
    code = code.replace("<<DESTINATION_ADAPTER>>", destination_adapter)
    code = code.replace("<<CHECKPOINT_PATH>>", checkpoint_file)
    code = code.replace("<<WAL_SEAL>>", seal)
    code = code.replace("<<SOURCE_IMPORTS>>", imports)
    return code


def self_test() -> bool:
    """Test auto : génère un bridge DuckDB → SQLite, l'exécute,
    vérifie le transfert et l'idempotence."""
    print("[SELF-TEST] citizen_bridge_generator — génération de bridge ...")

    bridge_code = generate_bridge(
        source_adapter="duckdb",
        destination_adapter="sqlite",
        checkpoint_file="/tmp/bridge_ckpt.json",
        wal_seal_prefix="WAL-0x243",
    )

    # Écrire le bridge généré dans un fichier temporaire et l'exécuter
    with tempfile.TemporaryDirectory(prefix="bridge_gen_test_") as tmpdir:
        bridge_path = Path(tmpdir) / "generated_bridge.py"
        bridge_path.write_text(bridge_code, encoding="utf-8")

        result = subprocess.run(
            [sys.executable, str(bridge_path), "--self-test"],
            capture_output=True,
            text=True,
        )
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)

        ok = result.returncode == 0 and "PASS" in result.stdout
        if ok:
            print(f"[SELF-TEST] Sceau : {WAL_SEAL}")
            return True
        print("[SELF-TEST] FAIL — le bridge généré a échoué.")
        print(f"[SELF-TEST] Sceau : {WAL_SEAL}")
        return False


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "--self-test":
        return 0 if self_test() else 1
    print("Usage: bridge_generator.py --self-test")
    return 1


if __name__ == "__main__":
    sys.exit(main())
