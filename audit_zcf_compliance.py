#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit_zcf_compliance.py — Auditeur de conformité Zero Cost Framework (ZCF).

Détecte les dépendances Python payantes (PAID) dans l'écosystème gerivdb
en scannant les requirements.txt et pyproject.toml d'une arborescence donnée.

Invariants : WAL 0x243 | Friction: 0.0 | Entropy: 0.0 |
             Seal: WAL-0x243-ZCF-COMPLIANCE-PASS

Usage :
    python audit_zcf_compliance.py --root D:\\DO\\WEB\\TOOLS --json
    python audit_zcf_compliance.py --self-test
"""

import argparse
import json
import os
import re
import sys
import tomllib
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory

# --- Constantes d'invariance WAL 0x243 ---
WAL_ID = "0x243"
SEAL = "WAL-0x243-ZCF-COMPLIANCE-PASS"
SELF_TEST_SEAL = "WAL-0x243-ZCF-COMPLIANCE-SELFTEST-PASS"

# Chemins par défaut (absolus)
DEFAULT_ROOT = r"D:\DO\WEB\TOOLS"
DEFAULT_TAXONOMY = r"D:\DO\WEB\TOOLS\L0-CANON\GOVERNANCE-HUB\config\zcf_packages.json"

# Fichiers de dépendances à scanner
DEPENDENCY_FILES = ("requirements.txt", "pyproject.toml")


def now_utc_iso():
    """Retourne l'horodatage UTC ISO 8601."""
    return datetime.now(timezone.utc).isoformat()


def load_taxonomy(taxonomy_path: str) -> dict:
    """Charge la taxonomie ZCF depuis un fichier JSON."""
    with open(taxonomy_path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_lookup_tables(taxonomy: dict) -> tuple[dict, dict]:
    """
    Construit deux tables de recherche : nom_package -> catégorie.
    Retourne (paid_lookup, free_lookup) où chaque clé est le nom du package
    en minuscules et la valeur est la catégorie ("PAID" ou "FREE").
    """
    paid_lookup = {}
    free_lookup = {}

    for pkg in taxonomy.get("paid_ai_sdks", []):
        paid_lookup[pkg.lower()] = "PAID"
    for pkg in taxonomy.get("paid_cloud_apis", []):
        paid_lookup[pkg.lower()] = "PAID"
    for pkg in taxonomy.get("free_ai_sdks", []):
        free_lookup[pkg.lower()] = "FREE"
    for pkg in taxonomy.get("free_cloud_apis", []):
        free_lookup[pkg.lower()] = "FREE"

    return paid_lookup, free_lookup


def normalize_package_name(raw: str) -> str:
    """
    Extrait le nom canonique d'une dépendance depuis une ligne de requirements.txt
    ou d'une entrée de dépendance pyproject.toml.

    Supprime :
    - versions (==1.2.3, >=1.0, etc.)
    - extras ([extra1,extra2])
    - marqueurs environnementaux (; python_version > "3.8")
    - commentaires inline
    """
    if not raw:
        return ""

    # Supprimer les commentaires inline
    raw = raw.split("#")[0].strip()
    if not raw:
        return ""

    # Supprimer les marqueurs environnementaux
    raw = raw.split(";")[0].strip()

    # Supprimer les extras
    raw = raw.split("[")[0].strip()

    # Extraire le nom avant tout séparateur de version
    match = re.match(r"^([A-Za-z0-9][A-Za-z0-9._-]*)", raw)
    if match:
        return match.group(1).lower()

    return raw.strip().lower()


def parse_requirements_txt(file_path: str) -> list[str]:
    """Parse un fichier requirements.txt et retourne la liste des noms de packages."""
    packages = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                # Ignorer les lignes vides, commentaires, options pip, inclusions
                if not line or line.startswith("#"):
                    continue
                if line.startswith("-") or line.startswith("--"):
                    continue
                pkg = normalize_package_name(line)
                if pkg:
                    packages.append(pkg)
    except Exception:
        pass
    return packages


def parse_pyproject_toml(file_path: str) -> list[str]:
    """Parse un fichier pyproject.toml et retourne la liste des noms de packages."""
    packages = []
    try:
        with open(file_path, "rb") as f:
            data = tomllib.load(f)
    except Exception:
        return packages

    # [project.dependencies]
    project = data.get("project", {})
    deps = project.get("dependencies", [])
    if isinstance(deps, list):
        for dep in deps:
            if isinstance(dep, str):
                pkg = normalize_package_name(dep)
                if pkg:
                    packages.append(pkg)

    # [dependency-groups] (PEP 735)
    dep_groups = data.get("dependency-groups", {})
    if isinstance(dep_groups, dict):
        for group_name, group_deps in dep_groups.items():
            if isinstance(group_deps, list):
                for dep in group_deps:
                    if isinstance(dep, str):
                        pkg = normalize_package_name(dep)
                        if pkg:
                            packages.append(pkg)

    # [tool.poetry.dependencies] (legacy Poetry)
    tool = data.get("tool", {})
    poetry = tool.get("poetry", {})
    poetry_deps = poetry.get("dependencies", {})
    if isinstance(poetry_deps, dict):
        for pkg_name in poetry_deps:
            if pkg_name.lower() != "python":
                packages.append(pkg_name.lower())

    return packages


def scan_repository(repo_dir: Path, paid_lookup: dict, free_lookup: dict) -> dict:
    """
    Scanne un seul repository (dossier contenant requirements.txt ou pyproject.toml).
    Retourne un dict avec les dépendances trouvées classées.
    """
    repo_name = repo_dir.name
    result = {
        "repo": repo_name,
        "path": str(repo_dir),
        "files": [],
        "paid": [],
        "free": [],
        "unknown": [],
    }

    for dep_file in DEPENDENCY_FILES:
        file_path = repo_dir / dep_file
        if not file_path.exists():
            continue

        file_entry = {
            "file": dep_file,
            "path": str(file_path),
            "packages": [],
        }

        if dep_file == "requirements.txt":
            pkgs = parse_requirements_txt(str(file_path))
        else:
            pkgs = parse_pyproject_toml(str(file_path))

        file_entry["packages"] = pkgs
        result["files"].append(file_entry)

        for pkg in pkgs:
            if pkg in paid_lookup:
                result["paid"].append({
                    "package": pkg,
                    "file": dep_file,
                    "category": "PAID",
                    "reason": f"Package '{pkg}' listé dans la taxonomie paid_ai_sdks ou paid_cloud_apis",
                })
            elif pkg in free_lookup:
                result["free"].append({
                    "package": pkg,
                    "file": dep_file,
                    "category": "FREE",
                })
            else:
                result["unknown"].append({
                    "package": pkg,
                    "file": dep_file,
                })

    return result


def scan_tree(root_path: str, taxonomy_path: str) -> dict:
    """
    Scanne récursivement une arborescence à la recherche de fichiers de dépendances.
    Retourne le rapport complet de conformité.
    """
    taxonomy = load_taxonomy(taxonomy_path)
    paid_lookup, free_lookup = build_lookup_tables(taxonomy)

    root = Path(root_path)
    if not root.exists():
        return {
            "compliant": False,
            "error": f"Répertoire racine introuvable : {root_path}",
            "wal_seal": SEAL,
            "timestamp_utc": now_utc_iso(),
        }

    repo_results = []
    all_violations = []
    all_unknowns = []
    total_paid = 0
    total_free = 0
    total_unknown = 0
    total_repos = 0
    total_files = 0

    # Dossiers à ignorer totalement (ne pas descendre dedans)
    IGNORED_DIRS = {
        ".git", "__pycache__", ".venv", "venv", "env", ".env",
        "node_modules", ".mypy_cache", ".pytest_cache", ".ruff_cache",
        ".idea", ".vscode", "build", "dist", ".eggs",
    }

    def _should_ignore(path: Path) -> bool:
        """Vérifie si un composant de chemin doit être ignoré."""
        parts = set(path.parts)
        return bool(parts & IGNORED_DIRS)

    # Trouver directement tous les fichiers de dépendance via rglob (plus rapide qu'os.walk)
    dep_files_found: list[Path] = []
    for dep_file in DEPENDENCY_FILES:
        try:
            dep_files_found.extend(root.rglob(dep_file))
        except Exception:
            pass

    # Grouper par dossier parent (chaque dossier contenant un fichier de dépendance = un repo)
    repos_map: dict[Path, list[Path]] = {}
    for dep_file in dep_files_found:
        if _should_ignore(dep_file):
            continue
        parent = dep_file.parent
        if parent not in repos_map:
            repos_map[parent] = []
        repos_map[parent].append(dep_file)

    for repo_dir, files in repos_map.items():
        total_repos += 1
        repo_result = scan_repository(repo_dir, paid_lookup, free_lookup)
        # Ne garder que les fichiers effectivement trouvés
        repo_result["files"] = [
            f for f in repo_result["files"]
            if (repo_dir / f["file"]).exists()
        ]
        total_files += len(repo_result["files"])
        repo_results.append(repo_result)

        for violation in repo_result["paid"]:
            all_violations.append({
                "repo": repo_result["repo"],
                "file": violation["file"],
                "package": violation["package"],
                "reason": violation["reason"],
            })
            total_paid += 1

        for unknown in repo_result["unknown"]:
            all_unknowns.append({
                "repo": repo_result["repo"],
                "file": unknown["file"],
                "package": unknown["package"],
            })
            total_unknown += 1

        total_free += len(repo_result["free"])

    compliant = total_paid == 0

    report = {
        "wal_seal": SEAL,
        "finops": "ZCF-0.0",
        "strate": "ENV2.pur",
        "timestamp_utc": now_utc_iso(),
        "root": str(root),
        "taxonomy": taxonomy_path,
        "compliant": compliant,
        "summary": {
            "total_repos_scanned": total_repos,
            "total_dependency_files": total_files,
            "paid_count": total_paid,
            "free_count": total_free,
            "unknown_count": total_unknown,
        },
        "violations": all_violations,
        "unknowns": all_unknowns,
        "repo_details": repo_results,
    }

    return report


def self_test() -> bool:
    """
    Exécute un self-test avec TemporaryDirectory.
    Crée 2 faux repos : un avec 'openai' (PAID), un avec 'groq' (FREE).
    Vérifie que le scan détecte correctement les deux et que compliant=False.
    """
    print("=" * 60)
    print("ZCF COMPLIANCE AUDITOR — SELF-TEST")
    print("WAL ID:", WAL_ID)
    print("Seal:", SEAL)
    print("=" * 60)

    taxonomy_path = DEFAULT_TAXONOMY
    paid_lookup, free_lookup = build_lookup_tables(load_taxonomy(taxonomy_path))

    with TemporaryDirectory(prefix="zcf_self_test_") as tmpdir:
        tmp_path = Path(tmpdir)

        # Repo 1 : dépendance PAID (openai) + package inconnu
        repo_paid = tmp_path / "repo-paid"
        repo_paid.mkdir()
        (repo_paid / "requirements.txt").write_text(
            "openai==1.40.0\nrequests>=2.31.0\nunknown-pkg-xyz>=1.0\n", encoding="utf-8"
        )

        # Repo 2 : dépendance FREE (groq)
        repo_free = tmp_path / "repo-free"
        repo_free.mkdir()
        (repo_free / "requirements.txt").write_text(
            "groq>=0.9.0\nollama>=0.1.0\n", encoding="utf-8"
        )

        results = []
        for repo_dir in [repo_paid, repo_free]:
            result = scan_repository(repo_dir, paid_lookup, free_lookup)
            results.append(result)

        # Vérifications
        all_pass = True

        # TEST 1 : openai détecté comme PAID
        paid_repo = results[0]
        openai_found = any(v["package"] == "openai" for v in paid_repo["paid"])
        print(f"\n[TEST 1] openai détecté comme PAID dans repo-paid : {'PASS' if openai_found else 'FAIL'}")
        if not openai_found:
            all_pass = False

        # TEST 2 : groq détecté comme FREE
        free_repo = results[1]
        groq_found = any(v["package"] == "groq" for v in free_repo["free"])
        print(f"[TEST 2] groq détecté comme FREE dans repo-free : {'PASS' if groq_found else 'FAIL'}")
        if not groq_found:
            all_pass = False

        # TEST 3 : compliant=False car openai (PAID) présent
        report = scan_tree(str(tmp_path), taxonomy_path)
        compliant_is_false = report["compliant"] is False
        print(f"[TEST 3] compliant=False (présence de openai PAID) : {'PASS' if compliant_is_false else 'FAIL'}")
        if not compliant_is_false:
            all_pass = False

        # TEST 4 : violations contient openai
        violation_packages = [v["package"] for v in report["violations"]]
        openai_in_violations = "openai" in violation_packages
        print(f"[TEST 4] openai présent dans les violations : {'PASS' if openai_in_violations else 'FAIL'}")
        if not openai_in_violations:
            all_pass = False

        # TEST 5 : requests détecté comme FREE (présent dans free_cloud_apis de la taxonomie)
        all_free_packages = []
        for rd in report["repo_details"]:
            all_free_packages.extend([v["package"] for v in rd["free"]])
        requests_is_free = "requests" in all_free_packages
        print(f"[TEST 5] requests détecté comme FREE : {'PASS' if requests_is_free else 'FAIL'}")
        if not requests_is_free:
            all_pass = False

        # TEST 6 : unknown-pkg-xyz détecté comme UNKNOWN
        unknown_packages = [u["package"] for u in report["unknowns"]]
        unknown_found = "unknown-pkg-xyz" in unknown_packages
        print(f"[TEST 6] unknown-pkg-xyz détecté comme UNKNOWN : {'PASS' if unknown_found else 'FAIL'}")
        if not unknown_found:
            all_pass = False

    print("\n" + "=" * 60)
    print("RÉSUMÉ DU SELF-TEST")
    print("=" * 60)
    print(f"Résultat global : {'PASS' if all_pass else 'FAIL'}")
    print(f"Sceau final : {SELF_TEST_SEAL if all_pass else SEAL + '-SELFTEST-FAIL'}")

    return all_pass


def main():
    parser = argparse.ArgumentParser(
        description="audit_zcf_compliance.py — Auditeur de conformité ZCF (WAL 0x243)"
    )
    parser.add_argument(
        "--root", default=DEFAULT_ROOT,
        help=f"Répertoire racine à scanner (défaut: {DEFAULT_ROOT})"
    )
    parser.add_argument(
        "--taxonomy", default=DEFAULT_TAXONOMY,
        help=f"Chemin vers zcf_packages.json (défaut: {DEFAULT_TAXONOMY})"
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Afficher le rapport JSON sur stdout"
    )
    parser.add_argument(
        "--output", default=None,
        help="Écrire le rapport JSON dans un fichier"
    )
    parser.add_argument(
        "--self-test", action="store_true",
        help="Exécuter le self-test avec TemporaryDirectory"
    )
    args = parser.parse_args()

    if args.self_test:
        success = self_test()
        sys.exit(0 if success else 1)

    report = scan_tree(args.root, args.taxonomy)

    if args.json or args.output:
        report_json = json.dumps(report, ensure_ascii=False, indent=2)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(report_json + "\n")
            print(f"Rapport écrit dans : {args.output}")
        if args.json:
            print(report_json)
    else:
        # Affichage résumé lisible
        print(f"ZCF Compliance Audit — {report['timestamp_utc']}")
        print(f"Racine : {report['root']}")
        print(f"Conforme : {report['compliant']}")
        print(f"Violations PAID : {report['summary']['paid_count']}")
        print(f"Dépendances FREE : {report['summary']['free_count']}")
        print(f"Inconnues : {report['summary']['unknown_count']}")
        if report["violations"]:
            print("\nViolations :")
            for v in report["violations"]:
                print(f"  - {v['repo']} / {v['file']} : {v['package']} ({v['reason']})")


if __name__ == "__main__":
    main()
