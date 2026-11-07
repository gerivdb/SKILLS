#!/usr/bin/env python3
# =============================================================================
# api_inspector.py — Citizen API Inspector (L4-TOOLS/SKILLS)
#
# Inspecte un repo Python et extrait une cartographie statique de son API :
#   - Classes, méthodes publiques, signatures (types, retours, exceptions)
#   - Schémas de base de données (SQLite via sqlite3, DuckDB via duckdb)
#   - Tables, colonnes, types de colonnes
#
# Retourne un JSON structuré utilisable par les bridges générés par
# citizen-bridge-generator.
#
# Sceau : WAL-0x243-API-INSPECTOR-SELFTEST
# =============================================================================
from __future__ import annotations

import ast
import importlib.util
import inspect
import json
import sqlite3
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import duckdb  # type: ignore
except Exception:  # pragma: no cover - DuckDB optionnel
    duckdb = None  # type: ignore[assignment]

WAL_SEAL = "WAL-0x243-API-INSPECTOR-SELFTEST"


# ---------------------------------------------------------------------------
# Extraction statique du code Python
# ---------------------------------------------------------------------------
def _extract_signature(func: ast.FunctionDef) -> Dict[str, Any]:
    """Extrait la signature d'une fonction : noms, types, valeur de retour."""
    args: List[str] = []
    defaults: List[str] = []
    for arg in func.args.args:
        annotation = (
            ast.unparse(arg.annotation) if arg.annotation else "Any"
        )
        args.append(f"{arg.arg}: {annotation}")
    if func.returns:
        ret = ast.unparse(func.returns)
    else:
        ret = "Any"
    return {
        "name": func.name,
        "args": args,
        "returns": ret,
        "decorators": [
            ast.unparse(d) for d in func.decorator_list
        ],
        "is_async": isinstance(func, ast.AsyncFunctionDef),
    }


def _extract_class(node: ast.ClassDef) -> Dict[str, Any]:
    """Extrait une classe avec ses méthodes publiques."""
    methods: List[Dict[str, Any]] = []
    bases: List[str] = []
    for base in node.bases:
        bases.append(ast.unparse(base))
    for item in node.body:
        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if not item.name.startswith("_"):
                methods.append(_extract_signature(item))
    return {
        "name": node.name,
        "bases": bases,
        "methods": methods,
    }


def inspect_python_repo(repo_path: Path) -> Dict[str, Any]:
    """Parcourt un dossier et extrait toutes les classes publiques des .py."""
    result: Dict[str, Any] = {
        "classes": [],
        "total_files": 0,
        "inspected_at": datetime.now(timezone.utc).isoformat(),
    }
    for py_file in sorted(repo_path.rglob("*.py")):
        if py_file.name == "__init__.py":
            continue
        try:
            source = py_file.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(py_file))
        except SyntaxError:
            continue
        result["total_files"] += 1
        for node in tree.body:
            if isinstance(node, ast.ClassDef) and not node.name.startswith("_"):
                result["classes"].append(_extract_class(node))
    return result


# ---------------------------------------------------------------------------
# Détection de schémas de base de données
# ---------------------------------------------------------------------------
def inspect_sqlite_db(db_path: Path) -> Dict[str, Any]:
    """Extrait le schéma d'une base SQLite : tables, colonnes, types."""
    if not db_path.exists():
        return {"error": f"SQLite DB not found: {db_path}"}
    conn = sqlite3.connect(str(db_path))
    try:
        tables: List[Dict[str, Any]] = []
        rows = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' "
            "AND name NOT LIKE 'sqlite_%'"
        ).fetchall()
        for (table_name,) in rows:
            cols = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
            columns = [
                {
                    "name": col[1],
                    "type": col[2],
                    "notnull": bool(col[3]),
                    "default": col[4],
                    "pk": bool(col[5]),
                }
                for col in cols
            ]
            tables.append({"name": table_name, "columns": columns})
        return {"tables": tables, "engine": "sqlite"}
    finally:
        conn.close()


def inspect_duckdb_db(db_path: Path) -> Dict[str, Any]:
    """Extrait le schéma d'une base DuckDB : tables, colonnes, types."""
    if duckdb is None:
        return {"error": "DuckDB not installed"}
    if not db_path.exists():
        return {"error": f"DuckDB not found: {db_path}"}
    conn = duckdb.connect(str(db_path), read_only=True)
    try:
        tables: List[Dict[str, Any]] = []
        rows = conn.execute(
            "SELECT table_name FROM information_schema.tables "
            "WHERE table_schema NOT IN ('pg_catalog','information_schema')"
        ).fetchall()
        for (table_name,) in rows:
            cols = conn.execute(
                f"DESCRIBE {table_name}"
            ).fetchall()
            columns = [
                {
                    "name": col[0],
                    "type": col[1],
                    "null": col[2],
                    "default": col[4] if len(col) > 4 else None,
                }
                for col in cols
            ]
            tables.append({"name": table_name, "columns": columns})
        return {"tables": tables, "engine": "duckdb"}
    except Exception as exc:  # pragma: no cover - défense
        return {"error": str(exc), "engine": "duckdb"}
    finally:
        conn.close()


def inspect_repo_for_dbs(repo_path: Path) -> List[Dict[str, Any]]:
    """Cherche les fichiers de base de données (.db, .duckdb) dans le repo."""
    found: List[Dict[str, Any]] = []
    for db_file in sorted(repo_path.rglob("*.db")):
        found.append(inspect_sqlite_db(db_file))
    for db_file in sorted(repo_path.rglob("*.duckdb")):
        found.append(inspect_duckdb_db(db_file))
    return found


# ---------------------------------------------------------------------------
# Point d'entrée principal
# ---------------------------------------------------------------------------
def inspect_repo(repo_path: str | Path) -> Dict[str, Any]:
    """Point d'entrée : inspecte un repo Python et retourne le JSON structuré."""
    path = Path(repo_path)
    if not path.exists():
        return {"error": f"Repo not found: {path}"}
    result: Dict[str, Any] = {
        "repo": str(path.resolve()),
        "python": inspect_python_repo(path),
        "databases": inspect_repo_for_dbs(path),
        "inspected_at": datetime.now(timezone.utc).isoformat(),
    }
    return result


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------
def self_test() -> bool:
    """Test auto : crée un faux repo avec 1 classe, 1 méthode, 1 table SQLite,
    exécute l'inspection et vérifie que le JSON contient les 3 éléments."""
    print("[SELF-TEST] citizen_api_inspector — inspection statique ...")

    with tempfile.TemporaryDirectory(prefix="api_inspector_test_") as tmpdir:
        repo_path = Path(tmpdir) / "fake_repo"
        repo_path.mkdir()

        # 1 classe avec 1 méthode publique
        (repo_path / "mymodule.py").write_text(
            'class FakeService:\n'
            '    def process(self, data: str) -> bool:\n'
            '        """Traite une donnée."""\n'
            '        return True\n',
            encoding="utf-8",
        )

        # 1 table SQLite
        db_path = repo_path / "store.db"
        conn = sqlite3.connect(str(db_path))
        try:
            conn.execute(
                "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT)"
            )
            conn.execute("INSERT INTO users (id, name, email) VALUES (1, 'Alice', 'a@x.com')")
            conn.commit()
        finally:
            conn.close()

        result = inspect_repo(repo_path)

    # Vérifications
    classes = result["python"]["classes"]
    databases = result["databases"]

    has_class = any(c["name"] == "FakeService" for c in classes)
    has_method = any(
        any(m["name"] == "process" for m in c.get("methods", []))
        for c in classes
    )
    has_table = any(
        any(t["name"] == "users" for t in db.get("tables", []))
        for db in databases
        if "tables" in db
    )

    print(f"[SELF-TEST] Classe détectée : {has_class}")
    print(f"[SELF-TEST] Méthode détectée : {has_method}")
    print(f"[SELF-TEST] Table SQLite détectée : {has_table}")
    print(f"[SELF-TEST] Nombre de classes : {len(classes)}")
    print(f"[SELF-TEST] Nombre de bases de données : {len(databases)}")

    ok = has_class and has_method and has_table
    if ok:
        print("[SELF-TEST] PASS — citizen_api_inspector opérationnel.")
        print(f"[SELF-TEST] Sceau : {WAL_SEAL}")
        return True
    print("[SELF-TEST] FAIL — extraction incomplète.")
    print(f"[SELF-TEST] Sceau : {WAL_SEAL}")
    return False


def main() -> int:
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--self-test":
        return 0 if self_test() else 1
    if len(sys.argv) > 1:
        result = inspect_repo(sys.argv[1])
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    print("Usage: api_inspector.py --self-test  OR  api_inspector.py <repo_path>")
    return 1


if __name__ == "__main__":
    sys.exit(main())
