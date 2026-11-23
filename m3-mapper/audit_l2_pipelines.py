#!/usr/bin/env python3
"""
Audit en lecture seule de la maturité des pipelines dans L2-PLATFORM.
"""
import os
import json
import yaml
from pathlib import Path

L2_PATH = Path("D:/DO/WEB/TOOLS/L2-PLATFORM")


def audit_repo(repo_path):
    repo_name = repo_path.name
    results = {
        "repo": repo_name,
        "has_repo_yaml": False,
        "repo_yaml_valid": False,
        "has_github_actions": False,
        "workflow_count": 0,
        "has_githooks": False,
        "has_bridge_validation": False,
        "status": "UNKNOWN"
    }

    # 1. Check REPO.yaml
    repo_yaml = repo_path / "REPO.yaml"
    if repo_yaml.exists():
        results["has_repo_yaml"] = True
        try:
            with open(repo_yaml, 'r') as f:
                data = yaml.safe_load(f)
                if isinstance(data, dict) and "layer" in data:
                    results["repo_yaml_valid"] = True
        except Exception:
            pass

    # 2. Check GitHub Actions
    workflows_dir = repo_path / ".github" / "workflows"
    if workflows_dir.exists() and workflows_dir.is_dir():
        results["has_github_actions"] = True
        results["workflow_count"] = len(list(workflows_dir.glob("*.yml"))) + len(list(workflows_dir.glob("*.yaml")))

    # 3. Check Git Hooks & Bridge Validation
    githooks_dir = repo_path / ".githooks"
    if githooks_dir.exists():
        results["has_githooks"] = True
        pre_commit = githooks_dir / "pre-commit.ps1"
        if pre_commit.exists():
            try:
                content = pre_commit.read_text(encoding='utf-8')
                if "bridge-schema" in content or "audit.py" in content:
                    results["has_bridge_validation"] = True
            except Exception:
                pass

    # Determine Status
    if results["repo_yaml_valid"] and results["has_github_actions"] and results["has_bridge_validation"]:
        results["status"] = "INDUSTRIALIZED"
    elif results["has_github_actions"]:
        results["status"] = "PARTIAL"
    else:
        results["status"] = "LEGACY_ADHOC"

    return results


def main():
    if not L2_PATH.exists():
        print(f"❌ Chemin L2-PLATFORM introuvable : {L2_PATH}")
        return

    print(f"🔍 Audit des pipelines L2-PLATFORM en cours...\n")
    findings = []

    for repo_dir in sorted(L2_PATH.iterdir()):
        if repo_dir.is_dir() and not repo_dir.name.startswith('.'):
            findings.append(audit_repo(repo_dir))

    # Summary
    total = len(findings)
    industrialized = sum(1 for f in findings if f["status"] == "INDUSTRIALIZED")
    partial = sum(1 for f in findings if f["status"] == "PARTIAL")
    legacy = sum(1 for f in findings if f["status"] == "LEGACY_ADHOC")

    print(f"=== RÉSUMÉ AUDIT L2-PLATFORM ===")
    print(f"Total dépôts scannés : {total}")
    print(f"  - INDUSTRIALIZED (Canon complet) : {industrialized}")
    print(f"  - PARTIAL (CI présente, hooks manquants) : {partial}")
    print(f"  - LEGACY_ADHOC (Pas de CI structurée) : {legacy}\n")

    print("Détails des dépôts LEGACY ou PARTIEL (Cibles prioritaires) :")
    for f in findings:
        if f["status"] in ["LEGACY_ADHOC", "PARTIAL"]:
            print(f"  - {f['repo']}: REPO.yaml={f['repo_yaml_valid']}, CI={f['workflow_count']}, Hooks={f['has_bridge_validation']}")

    # Save raw data
    output_path = Path("l2_pipeline_audit.json")
    with open(output_path, "w") as f:
        json.dump(findings, f, indent=2)
    print(f"\n✅ Données brutes sauvegardées dans {output_path.resolve()}")


if __name__ == "__main__":
    main()
