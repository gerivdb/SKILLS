#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script souverain d'orchestration des worktrees Agent Manager sur ENV2.
Conforme à la topologie des strates L* | Respect strict CP1252 | Zéro-pollution
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

# Chemins canoniques conformes aux strates ENV2
DEFAULT_REPO = r"D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS"
DEFAULT_WORKTREE_BASE = r"D:\DO\WEB\TOOLS\L6-WORK\worktrees"
DEFAULT_MANIFEST = r"D:\DO\WEB\TOOLS\L6-WORK\agent_tasks_manifest.json"

DEFAULT_TASKS = [
    {
        "name": "forensics-audit-fix",
        "branch": "agent/forensics-fix",
        "prompt": "Audit the 5 core forensic skills and ensure all NTFS junctions and scripts are fully verified."
    },
    {
        "name": "registry-synchronization",
        "branch": "agent/registry-sync",
        "prompt": "Cross-reference REGISTRY.yaml with physical directories and purge any remaining orphaned entries."
    }
]


def run_git(cmd, cwd):
    """Exécute une commande git avec capture sécurisée."""
    print(f"[*] Git: {' '.join(cmd)} (dans {cwd})")
    res = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[-] Erreur Git : {res.stderr.strip()}")
        return False, res.stderr.strip()
    out = res.stdout.strip()
    if out:
        print(f"[+] Git OK : {out}")
    return True, out


def is_git_repo(path):
    """Vérifie si le répertoire cible est un dépôt Git valide."""
    git_dir = Path(path) / ".git"
    return git_dir.exists()


def main():
    parser = argparse.ArgumentParser(description="Orchestrateur de Worktrees Agent Manager ENV2")
    parser.add_argument("--repo", default=DEFAULT_REPO, help="Chemin absolu du dépôt Git source")
    parser.add_argument("--worktree-base", default=DEFAULT_WORKTREE_BASE, help="Dossier de destination L6-WORK")
    parser.add_argument("--manifest", default=DEFAULT_MANIFEST, help="Chemin du fichier manifeste JSON de sortie")
    args = parser.parse_args()

    repo_path = os.path.abspath(args.repo)
    wt_base = os.path.abspath(args.worktree_base)
    manifest_path = os.path.abspath(args.manifest)

    print("=== Orchestrateur de Worktrees Kilo Agent Manager ===")
    print(f"[*] Dépôt source : {repo_path}")
    print(f"[*] Base Worktree (Strate L6) : {wt_base}")

    # 1. Vérification d'intégrité du dépôt
    if not is_git_repo(repo_path):
        print(f"[FATAL] Le chemin source n'est pas un dépôt Git valide : {repo_path}")
        sys.exit(1)

    os.makedirs(wt_base, exist_ok=True)
    os.makedirs(os.path.dirname(manifest_path), exist_ok=True)

    workflow_payload = {
        "mode": "worktree",
        "versions": False,
        "tasks": []
    }

    # 2. Déploiement des worktrees
    for task in DEFAULT_TASKS:
        task_name = task["name"]
        branch_name = task["branch"]
        wt_path = os.path.join(wt_base, task_name)

        print(f"\n--- Préparation de la tâche : {task_name} ---")

        if not os.path.exists(wt_path):
            ok, _ = run_git(["git", "worktree", "add", "-b", branch_name, wt_path], cwd=repo_path)
            if not ok:
                # Tentative si la branche existe déjà
                print(f"[*] Tentative de rattachement à la branche existante '{branch_name}'...")
                ok, _ = run_git(["git", "worktree", "add", wt_path, branch_name], cwd=repo_path)
                if not ok:
                    print(f"[-] Échec de création du worktree pour {task_name} — saut")
                    continue
            print(f"[+] Worktree créé avec succès dans L6 : {wt_path}")
        else:
            print(f"[*] Le worktree existe déjà à l'emplacement : {wt_path}")

        workflow_payload["tasks"].append({
            "name": task_name,
            "branchName": branch_name,
            "worktreePath": wt_path,
            "prompt": task["prompt"]
        })

    # 3. Écriture du manifeste JSON pour Kilo Code
    print(f"\n[*] Écriture du manifeste d'orchestration : {manifest_path}")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(workflow_payload, f, indent=2, ensure_ascii=False)

    print(f"[SUCCESS] {len(workflow_payload['tasks'])} tâches prêtes pour l'Agent Manager.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
