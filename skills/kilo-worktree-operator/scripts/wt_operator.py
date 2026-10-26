#!/usr/bin/env python3
#==============================================================================
# SKILL: kilo-worktree-operator (6 super-pouvoirs)
# Rôle: Manipulateur headless de l'Agent Manager via CLI.
# 6 commandes : wt:purge-merged, wt:organize-sections, wt:sync-all,
#             wt:pin, wt:unpin, wt:spawn-clean, wt:ghost-buster
# Couche CRUD — Create, Read, Update, Delete sur l'écosystème worktree.
#==============================================================================

import argparse
import json
import os
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# --- Constantes ---
SKILLS_REPO = Path(r"D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS")
RAGX_REPO = Path(r"D:\DO\WEB\L0-CANON\RAGX")
AM_JSON = SKILLS_REPO / ".kilo" / "agent-manager.json"
WAL_LOG = SKILLS_REPO / "wal" / "kwo-wal.log"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def wal_log(message: str) -> None:
    WAL_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(WAL_LOG, "a", encoding="utf-8") as f:
        f.write(f"[{utc_now()}] {message}\n")


def load_agent_manager() -> dict:
    if not AM_JSON.exists():
        return {"worktrees": {}, "sessions": {}, "tabOrder": {"local": []}, "worktreeOrder": []}
    with open(AM_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def save_agent_manager(data: dict) -> None:
    AM_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(AM_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    wal_log(f"agent-manager.json mis à jour")


def get_repo_path(project_id: str) -> Path:
    if project_id == "RAGX":
        return RAGX_REPO
    return SKILLS_REPO


def git_run(repo: Path, *args) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
    )


# ---------------------------------------------------------------------------
# 1. wt:purge-merged
# ---------------------------------------------------------------------------
def cmd_purge_merged(project_id: str) -> dict:
    repo = get_repo_path(project_id)
    wal_log(f"wt:purge-merged debut project={project_id}")

    # Récupérer les branches mergées dans main
    res = git_run(repo, "branch", "--merged", "main")
    if res.returncode != 0:
        return {"command": "wt:purge-merged", "status": "FAIL", "error": res.stderr.strip()}

    merged_lines = [l.strip().lstrip("* ").strip() for l in res.stdout.splitlines() if l.strip()]
    # Exclure main elle-même
    merged_branches = [b for b in merged_lines if b != "main"]

    data = load_agent_manager()
    purged = []
    errors = []

    for branch in merged_branches:
        # Trouver le worktree associé dans agent-manager.json
        wt_id_to_remove = None
        wt_path = None
        for wt_id, wt_info in data.get("worktrees", {}).items():
            if wt_info.get("branch") == branch:
                wt_id_to_remove = wt_id
                wt_path = wt_info.get("path")
                break

        # Supprimer le dossier physique du worktree
        if wt_path and os.path.exists(wt_path):
            try:
                # D'abord retirer le worktree de git
                git_run(repo, "worktree", "remove", "--force", wt_path)
                # Puis supprimer le dossier physique
                import shutil
                shutil.rmtree(wt_path, ignore_errors=True)
                purged.append({"branch": branch, "worktree_id": wt_id_to_remove, "path": wt_path})
                wal_log(f"wt:purge-merged supprime worktree branch={branch} id={wt_id_to_remove}")
            except Exception as e:
                errors.append({"branch": branch, "error": str(e)})
                wal_log(f"wt:purge-merged echec branch={branch}: {e}")

        # Retirer de agent-manager.json
        if wt_id_to_remove:
            data["worktrees"].pop(wt_id_to_remove, None)
            if "worktreeOrder" in data:
                data["worktreeOrder"] = [w for w in data["worktreeOrder"] if w != wt_id_to_remove]

            # Supprimer aussi la branche Git locale
            git_run(repo, "branch", "-D", branch)

    save_agent_manager(data)

    return {
        "command": "wt:purge-merged",
        "project": project_id,
        "status": "OK",
        "merged_branches": merged_branches,
        "purged": purged,
        "errors": errors,
        "count": len(purged),
    }


# ---------------------------------------------------------------------------
# 2. wt:organize-sections
# ---------------------------------------------------------------------------
def cmd_organize_sections(project_id: str) -> dict:
    repo = get_repo_path(project_id)
    wal_log(f"wt:organize-sections debut project={project_id}")

    data = load_agent_manager()
    sections = {}
    ungrouped = []

    for wt_id, wt_info in data.get("worktrees", {}).items():
        branch = wt_info.get("branch", "")
        # Extraire le préfixe (avant le premier tiret ou slash)
        prefix = branch.split("-")[0] if "-" in branch else branch.split("/")[0] if "/" in branch else "ungrouped"
        section_name = prefix if prefix != "ungrouped" else "ungrouped"

        if section_name not in sections:
            sections[section_name] = []
        sections[section_name].append(wt_id)

        if section_name == "ungrouped":
            ungrouped.append(wt_id)

    # Mettre à jour agent-manager.json avec les sections
    data["sections"] = {k: v for k, v in sections.items()}
    save_agent_manager(data)

    return {
        "command": "wt:organize-sections",
        "project": project_id,
        "status": "OK",
        "sections": {k: len(v) for k, v in sections.items()},
        "ungrouped_count": len(ungrouped),
        "ungrouped_worktrees": ungrouped,
    }


# ---------------------------------------------------------------------------
# 3. wt:sync-all
# ---------------------------------------------------------------------------
def _sync_one(repo: Path, wt_id: str, wt_info: dict) -> dict:
    wt_path = wt_info.get("path", "")
    branch = wt_info.get("branch", "")
    result = {"worktree_id": wt_id, "branch": branch, "status": "skipped", "detail": ""}

    if not wt_path or not os.path.exists(wt_path):
        result["detail"] = "chemin absent"
        return result

    # Fetch explicite (protocole BDCP)
    fetch_res = git_run(repo, "fetch", "origin")
    if fetch_res.returncode != 0:
        result["status"] = "fail"
        result["detail"] = fetch_res.stderr.strip()
        return result

    # Merge origin/main sur la branche du worktree
    merge_res = git_run(repo, "merge", f"origin/main")
    if merge_res.returncode == 0:
        result["status"] = "synced"
        result["detail"] = "merge origin/main OK"
    else:
        result["status"] = "conflict"
        result["detail"] = merge_res.stderr.strip()

    return result


def cmd_sync_all(project_id: str) -> dict:
    repo = get_repo_path(project_id)
    wal_log(f"wt:sync-all debut project={project_id}")

    data = load_agent_manager()
    worktrees = data.get("worktrees", {})

    results = []
    with ThreadPoolExecutor(max_workers=min(len(worktrees), 8)) as executor:
        futures = {
            executor.submit(_sync_one, repo, wt_id, wt_info): wt_id
            for wt_id, wt_info in worktrees.items()
        }
        for future in as_completed(futures):
            results.append(future.result())

    synced = sum(1 for r in results if r["status"] == "synced")
    conflicts = sum(1 for r in results if r["status"] == "conflict")
    skipped = sum(1 for r in results if r["status"] == "skipped")
    failed = sum(1 for r in results if r["status"] == "fail")

    return {
        "command": "wt:sync-all",
        "project": project_id,
        "status": "OK" if conflicts == 0 and failed == 0 else "PARTIAL",
        "synced": synced,
        "conflicts": conflicts,
        "skipped": skipped,
        "failed": failed,
        "details": results,
    }


# ---------------------------------------------------------------------------
# 4. wt:pin / wt:unpin
# ---------------------------------------------------------------------------
def cmd_pin(project_id: str, worktree_id: str) -> dict:
    data = load_agent_manager()
    if worktree_id not in data.get("worktrees", {}):
        return {"command": "wt:pin", "status": "FAIL", "error": f"worktree {worktree_id} introuvable"}

    if "pinnedWorktrees" not in data:
        data["pinnedWorktrees"] = []
    if worktree_id not in data["pinnedWorktrees"]:
        data["pinnedWorktrees"].append(worktree_id)
    save_agent_manager(data)
    wal_log(f"wt:pin worktree={worktree_id}")

    return {"command": "wt:pin", "worktree_id": worktree_id, "status": "OK", "pinned": True}


def cmd_unpin(project_id: str, worktree_id: str) -> dict:
    data = load_agent_manager()
    pinned = data.get("pinnedWorktrees", [])
    if worktree_id in pinned:
        pinned.remove(worktree_id)
        data["pinnedWorktrees"] = pinned
        save_agent_manager(data)
        wal_log(f"wt:unpin worktree={worktree_id}")
        return {"command": "wt:unpin", "worktree_id": worktree_id, "status": "OK", "pinned": False}
    return {"command": "wt:unpin", "worktree_id": worktree_id, "status": "OK", "pinned": False, "detail": "déjà non épinglé"}


# ---------------------------------------------------------------------------
# 5. wt:spawn-clean
# ---------------------------------------------------------------------------
def cmd_spawn_clean(project_id: str, branch_name: str) -> dict:
    repo = get_repo_path(project_id)
    wal_log(f"wt:spawn-clean debut branch={branch_name} project={project_id}")

    # 1. Créer la branche depuis main
    checkout_res = git_run(repo, "checkout", "main")
    if checkout_res.returncode != 0:
        return {"command": "wt:spawn-clean", "status": "FAIL", "error": f"checkout main échoué: {checkout_res.stderr}"}

    branch_res = git_run(repo, "checkout", "-b", branch_name)
    if branch_res.returncode != 0:
        return {"command": "wt:spawn-clean", "status": "FAIL", "error": f"création branche échouée: {branch_res.stderr}"}

    # 2. Poser le worktree
    wt_path = repo / ".kilo" / "worktrees" / branch_name
    add_res = git_run(repo, "worktree", "add", str(wt_path), branch_name)
    if add_res.returncode != 0:
        return {"command": "wt:spawn-clean", "status": "FAIL", "error": f"worktree add échoué: {add_res.stderr}"}

    # 3. Générer metadata.json
    metadata = {
        "branch": branch_name,
        "worktree_path": str(wt_path),
        "created_at": utc_now(),
        "project": project_id,
        "status": "active",
    }
    metadata_path = wt_path / "metadata.json"
    metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")

    # 4. Inscrire la session dans agent-manager.json SANS clé pending:
    wt_id = f"wt-{int(datetime.now().timestamp() * 1000)}-{uuid.uuid4().hex[:6]}"
    data = load_agent_manager()
    data.setdefault("worktrees", {})[wt_id] = {
        "branch": branch_name,
        "path": str(wt_path),
        "parentBranch": "main",
        "createdAt": utc_now(),
        "remote": "origin",
    }
    data.setdefault("sessions", {})[f"ses_{uuid.uuid4().hex[:16]}"] = {
        "worktreeId": wt_id,
        "createdAt": utc_now(),
    }
    data.setdefault("worktreeOrder", []).append(wt_id)
    # Pas de clé pending: dans tabOrder.local — instanciation propre
    save_agent_manager(data)

    return {
        "command": "wt:spawn-clean",
        "branch": branch_name,
        "worktree_id": wt_id,
        "worktree_path": str(wt_path),
        "status": "OK",
        "metadata": metadata,
    }


# ---------------------------------------------------------------------------
# 6. wt:ghost-buster
# ---------------------------------------------------------------------------
def cmd_ghost_buster(project_id: str) -> dict:
    repo = get_repo_path(project_id)
    wal_log(f"wt:ghost-buster debut project={project_id}")

    data = load_agent_manager()

    # Détecter les sessions orphelines (session dont le worktree n'existe plus)
    active_wt_ids = set(data.get("worktrees", {}).keys())
    orphan_sessions = []
    for sid, sinfo in data.get("sessions", {}).items():
        if sinfo.get("worktreeId") not in active_wt_ids:
            orphan_sessions.append(sid)
            wal_log(f"wt:ghost-buster session orpheline: {sid}")

    # Supprimer les sessions orphelines
    for sid in orphan_sessions:
        data["sessions"].pop(sid, None)

    # Détecter et éliminer les clés pending:<uuid> dans tabOrder.local
    tab_local = data.get("tabOrder", {}).get("local", [])
    pending_keys = [e for e in tab_local if isinstance(e, str) and e.startswith("pending:")]
    clean_tab = [e for e in tab_local if not (isinstance(e, str) and e.startswith("pending:"))]

    if clean_tab != tab_local:
        data.setdefault("tabOrder", {})["local"] = clean_tab
        wal_log(f"wt:ghost-buster {len(pending_keys)} clé(s) pending supprimée(s)")

    save_agent_manager(data)

    return {
        "command": "wt:ghost-buster",
        "project": project_id,
        "status": "OK",
        "orphan_sessions_removed": len(orphan_sessions),
        "orphan_session_ids": orphan_sessions,
        "pending_keys_removed": len(pending_keys),
        "pending_key_ids": pending_keys,
    }


# ---------------------------------------------------------------------------
# Dispatcher principal
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="kilo-worktree-operator — 6 super-pouvoirs")
    sub = parser.add_subparsers(dest="command", required=True)

    # wt:purge-merged
    p_purge = sub.add_parser("wt:purge-merged")
    p_purge.add_argument("--project", default="SKILLS")

    # wt:organize-sections
    p_org = sub.add_parser("wt:organize-sections")
    p_org.add_argument("--project", default="SKILLS")

    # wt:sync-all
    p_sync = sub.add_parser("wt:sync-all")
    p_sync.add_argument("--project", default="SKILLS")

    # wt:pin / wt:unpin
    p_pin = sub.add_parser("wt:pin")
    p_pin.add_argument("--worktree", required=True)
    p_pin.add_argument("--project", default="SKILLS")

    p_unpin = sub.add_parser("wt:unpin")
    p_unpin.add_argument("--worktree", required=True)
    p_unpin.add_argument("--project", default="SKILLS")

    # wt:spawn-clean
    p_spawn = sub.add_parser("wt:spawn-clean")
    p_spawn.add_argument("--branch", required=True)
    p_spawn.add_argument("--project", default="SKILLS")

    # wt:ghost-buster
    p_ghost = sub.add_parser("wt:ghost-buster")
    p_ghost.add_argument("--project", default="SKILLS")

    args = parser.parse_args()

    result = None
    cmd = args.command
    project = getattr(args, "project", "SKILLS")

    try:
        if cmd == "wt:purge-merged":
            result = cmd_purge_merged(project)
        elif cmd == "wt:organize-sections":
            result = cmd_organize_sections(project)
        elif cmd == "wt:sync-all":
            result = cmd_sync_all(project)
        elif cmd == "wt:pin":
            result = cmd_pin(project, args.worktree)
        elif cmd == "wt:unpin":
            result = cmd_unpin(project, args.worktree)
        elif cmd == "wt:spawn-clean":
            result = cmd_spawn_clean(project, args.branch)
        elif cmd == "wt:ghost-buster":
            result = cmd_ghost_buster(project)
    except Exception as e:
        result = {"command": cmd, "status": "FAIL", "error": str(e)}
        wal_log(f"{cmd} ERREUR: {e}")

    print(json.dumps(result, indent=2, ensure_ascii=False))
    wal_log(f"{cmd} terminé status={result.get('status')}")
    sys.exit(0 if result.get("status") == "OK" else 1)


if __name__ == "__main__":
    main()