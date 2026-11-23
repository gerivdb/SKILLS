#!/usr/bin/env python3
"""
Propage le Golden Template L2 vers un dépôt cible.
Usage: python propagate_template.py <repo_path> [--dry-run]
"""
import sys
import shutil
from pathlib import Path
from datetime import datetime
import argparse

TEMPLATE_DIR = Path(__file__).parent


def propagate(repo_path: Path, dry_run: bool = False):
    repo_name = repo_path.name

    print(f"🎯 Propagation vers {repo_name}...")

    # 1. REPO.yaml
    repo_yaml_template = TEMPLATE_DIR / "REPO.yaml.template"
    repo_yaml_target = repo_path / "REPO.yaml"

    if repo_yaml_target.exists():
        print(f"  ⚠️  REPO.yaml existe déjà. Backup créé.")
        if not dry_run:
            backup = repo_path / f"REPO.yaml.backup-{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            shutil.copy2(repo_yaml_target, backup)

    if not dry_run:
        # Lire le template et remplacer les placeholders
        content = repo_yaml_template.read_text()
        content = content.replace("{{REPO_NAME}}", repo_name)
        content = content.replace("{{REPO_NAME_UPPER}}", repo_name.upper())
        content = content.replace("{{TIMESTAMP_ISO}}", datetime.now().isoformat())
        content = content.replace("{{REPO_DESCRIPTION}}", f"Platform component: {repo_name}")

        repo_yaml_target.write_text(content)
        print(f"  ✅ REPO.yaml créé/mis à jour")

    # 2. GitHub Actions CI
    workflows_dir = repo_path / ".github" / "workflows"
    ci_template = TEMPLATE_DIR / "ci.yml.template"
    ci_target = workflows_dir / "ci.yml"

    if not dry_run:
        workflows_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ci_template, ci_target)
        print(f"  ✅ CI workflow créé")

    # 3. Git Hooks
    githooks_dir = repo_path / ".githooks"
    hook_template = TEMPLATE_DIR / "pre-commit.ps1.template"
    hook_target = githooks_dir / "pre-commit.ps1"

    if not dry_run:
        githooks_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(hook_template, hook_target)
        print(f"  ✅ Pre-commit hook créé")

        # Configurer core.hooksPath
        import subprocess
        subprocess.run(["git", "config", "core.hooksPath", ".githooks"], cwd=repo_path, check=True)
        print(f"  ✅ core.hooksPath configuré")

    print(f"  🎉 Propagation terminée pour {repo_name}")

    if dry_run:
        print(f"  [DRY-RUN] Aucune modification effectuée")


def main():
    parser = argparse.ArgumentParser(description="Propager le Golden Template L2")
    parser.add_argument("repo_path", type=Path, help="Chemin du dépôt cible")
    parser.add_argument("--dry-run", action="store_true", help="Simuler sans modifier")

    args = parser.parse_args()

    if not args.repo_path.exists():
        print(f"❌ Chemin inexistant: {args.repo_path}")
        sys.exit(1)

    propagate(args.repo_path, args.dry_run)


if __name__ == "__main__":
    main()
