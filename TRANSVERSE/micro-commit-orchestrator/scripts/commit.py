#!/usr/bin/env python3
"""
micro-commit-orchestrator -- Workflow git atomique par ATOM.

Workflow: stage -> validate -> commit -> verify -> push
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Optional


ATOM_PATTERN = re.compile(r"^ATOM-(\d+)$")
CONVENTIONAL_TYPES = {"feat", "fix", "docs", "refactor", "test", "chore", "perf"}
COMMIT_PATTERN = re.compile(r"^(feat|fix|docs|refactor|test|chore|perf)\(ATOM-\d+\): .+")


def run_cmd(cmd: List[str], cwd: Path = None, dry_run: bool = False) -> subprocess.CompletedProcess:
    """Execute commande avec gestion dry-run."""
    if dry_run:
        print(f"[DRY-RUN] {' '.join(cmd)}")
        return subprocess.CompletedProcess(cmd, 0, "", "")
    
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[ERROR] {' '.join(cmd)}", file=sys.stderr)
        print(f"  stderr: {result.stderr}", file=sys.stderr)
    return result


def validate_atom_number(atom: str) -> bool:
    """Valide format ATOM-XXX."""
    return bool(ATOM_PATTERN.match(atom))


def validate_files(files: List[str]) -> tuple[bool, str]:
    """Valide liste fichiers (<= 3)."""
    if len(files) > 3:
        return False, f"Trop de fichiers: {len(files)} (max 3)"
    for f in files:
        if not Path(f).exists():
            return False, f"Fichier introuvable: {f}"
    return True, ""


def validate_commit_message(msg: str, atom: str = None) -> tuple[bool, str]:
    """Valide format Conventional Commits + ATOM."""
    if atom and f"({atom})" not in msg:
        return False, f"Message doit contenir ({atom})"
    if not COMMIT_PATTERN.match(msg):
        return False, "Format invalide: type(ATOM-XXX): description"
    return True, ""


def check_secrets(files: List[str]) -> tuple[bool, str]:
    """Scan basique secrets dans fichiers stages."""
    secret_patterns = [
        r"password\s*=\s*['\"][^'\"]+['\"]",
        r"token\s*=\s*['\"][^'\"]+['\"]",
        r"api_key\s*=\s*['\"][^'\"]+['\"]",
        r"secret\s*=\s*['\"][^'\"]+['\"]",
        r"ghp_[a-zA-Z0-9]{36}",
        r"sk_[a-zA-Z0-9]{48}",
    ]
    for f in files:
        try:
            content = Path(f).read_text(encoding="utf-8", errors="ignore")
            import re
            for pattern in secret_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    return False, f"Secret potentiel dans {f}: {pattern}"
        except:
            pass
    return True, ""


def get_staged_files() -> List[str]:
    """Retourne fichiers stages."""
    result = subprocess.run(["git", "diff", "--cached", "--name-only"], capture_output=True, text=True)
    return [f for f in result.stdout.strip().split("\n") if f]


def main():
    parser = argparse.ArgumentParser(
        description="Workflow git atomique par ATOM (stage -> commit -> verify -> push)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--atom", help="Numero ATOM (ex: ATOM-062)")
    parser.add_argument("--files", help="Fichiers a committer (space-separated)")
    parser.add_argument("--msg", help="Description courte")
    parser.add_argument("--type", default="feat", choices=list(CONVENTIONAL_TYPES), help="Type commit")
    parser.add_argument("--intent", help="IntentHash (0x...)")
    parser.add_argument("--refs", help="Refs ADR/INTENT/EPIC (comma-separated)")
    parser.add_argument("--branch", help="Branche cible")
    parser.add_argument("--stage-only", action="store_true", help="Seulement git add")
    parser.add_argument("--commit-only", action="store_true", help="Seulement git commit")
    parser.add_argument("--verify-only", action="store_true", help="Seulement verification")
    parser.add_argument("--push-only", action="store_true", help="Seulement git push")
    parser.add_argument("--check-format", action="store_true", help="Verifier format message")
    parser.add_argument("--dry-run", action="store_true", help="Simuler sans executer")
    
    args = parser.parse_args()
    
    # Determine files
    if args.files:
        files = args.files.split()
    else:
        files = get_staged_files()
    
    if not files:
        print("[ERROR] Aucun fichier a committer", file=sys.stderr)
        sys.exit(2)
    
    # Validate files count
    ok, err = validate_files(files)
    if not ok:
        print(f"[ERROR] {err}", file=sys.stderr)
        sys.exit(1)
    
    # Build commit message
    if args.msg:
        if args.atom:
            commit_msg = f"{args.type}({args.atom}): {args.msg}"
        else:
            commit_msg = f"{args.type}: {args.msg}"
        
        # Add IntentHash
        if args.intent:
            commit_msg += f"\n\nIntentHash: {args.intent}"
        
        # Add Refs
        if args.refs:
            commit_msg += f"\nRefs: {args.refs}"
    else:
        commit_msg = None
    
    # Check format only
    if args.check_format:
        if not commit_msg:
            print("[ERROR] --msg requis pour --check-format", file=sys.stderr)
            sys.exit(2)
        ok, err = validate_commit_message(commit_msg, args.atom)
        if ok:
            print("[OK] Format message valide")
            sys.exit(0)
        else:
            print(f"[ERROR] {err}", file=sys.stderr)
            sys.exit(1)
    
    if not commit_msg:
        print("[ERROR] --msg requis", file=sys.stderr)
        sys.exit(2)
    
    # Validate commit message
    ok, err = validate_commit_message(commit_msg, args.atom)
    if not ok:
        print(f"[ERROR] Message invalide: {err}", file=sys.stderr)
        sys.exit(1)
    
    # Check secrets
    ok, err = check_secrets(files)
    if not ok:
        print(f"[ERROR] {err}", file=sys.stderr)
        sys.exit(1)
    
    cwd = Path.cwd()
    dry_run = args.dry_run
    
    # STEP 1: STAGE
    if not args.commit_only and not args.verify_only and not args.push_only:
        print(f"[STAGE] {' '.join(files)}")
        result = run_cmd(["git", "add"] + files, cwd, dry_run)
        if result.returncode != 0:
            sys.exit(1)
        if args.stage_only:
            print("[OK] Stage complete")
            return
    
    # STEP 2: COMMIT
    if not args.stage_only and not args.verify_only and not args.push_only:
        print(f"[COMMIT] {commit_msg.split(chr(10))[0]}")
        result = run_cmd(["git", "commit", "-m", commit_msg], cwd, dry_run)
        if result.returncode != 0:
            sys.exit(1)
        if args.commit_only:
            print("[OK] Commit complete")
            return
    
    # STEP 3: VERIFY
    if not args.stage_only and not args.commit_only and not args.push_only:
        print("[VERIFY] git log --oneline -1")
        result = run_cmd(["git", "log", "--oneline", "-1"], cwd, dry_run)
        if result.returncode == 0:
            print(f"  {result.stdout.strip()}")
        if args.verify_only:
            print("[OK] Verify complete")
            return
    
    # STEP 4: PUSH
    if not args.stage_only and not args.commit_only and not args.verify_only:
        branch = args.branch or subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True).stdout.strip()
        print(f"[PUSH] origin {branch}")
        result = run_cmd(["git", "push", "origin", branch], cwd, dry_run)
        if result.returncode != 0:
            sys.exit(1)
    
    print("[OK] ATOM livree avec succes")
    sys.exit(0)


if __name__ == "__main__":
    main()
