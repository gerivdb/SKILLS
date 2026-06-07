#!/usr/bin/env python3
"""
mc-rnn-env2-bench — Benchmark MC-RNN sur ENV2 (HP Z600, Xeon E5620)

Execute zig build test + zig build mc-rnn-bench sur CodeDB-E5620.
Produit des logs dans logs/ avec timestamp.

Usage:
    python scripts/mc-rnn-env2-bench.py [--repo-path PATH] [--output-dir DIR]

Reference: ADR adr-mc-rnn-closure-20260607.md lacune L3 (remede P0)
"""

import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime

DEFAULT_REPO = r"D:\DO\WEB\TOOLS\L4-TOOLS\CodeDB-E5620"
DEFAULT_OUTPUT = r"D:\DO\WEB\TOOLS\L4-TOOLS\CodeDB-E5620\logs"

def check_zig():
    """Verifier que Zig est disponible."""
    result = subprocess.run(["zig", "version"], capture_output=True, text=True)
    if result.returncode != 0:
        print("[FAIL] Zig non trouve dans PATH")
        print("[INFO] Installer Zig 0.14+ sur ENV2: https://ziglang.org/download/")
        return False
    print(f"[OK] Zig: {result.stdout.strip()}")
    return True

def run_zig_test(repo_path, output_dir):
    """Lancer zig build test."""
    print("\n[STEP 1] zig build test")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(output_dir, f"zig-test-{timestamp}.log")
    
    result = subprocess.run(
        ["zig", "build", "test", "--summary", "all"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        timeout=300
    )
    
    # Ecrire le log
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write(f"STDOUT:\n{result.stdout}\n")
        f.write(f"STDERR:\n{result.stderr}\n")
        f.write(f"Return code: {result.returncode}\n")
    
    if result.returncode == 0:
        print(f"[PASS] Tests Zig OK — log: {log_file}")
        # Compter les tests
        for line in result.stdout.split('\n'):
            if 'test' in line.lower() and ('pass' in line.lower() or 'fail' in line.lower()):
                print(f"  {line.strip()}")
        return True
    else:
        print(f"[FAIL] Tests Zig ECHEC (rc={result.returncode}) — log: {log_file}")
        print(result.stderr[-500:] if result.stderr else result.stdout[-500:])
        return False

def run_zig_bench(repo_path, output_dir):
    """Lancer zig build mc-rnn-bench."""
    print("\n[STEP 2] zig build mc-rnn-bench")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(output_dir, f"zig-bench-{timestamp}.log")
    
    result = subprocess.run(
        ["zig", "build", "mc-rnn-bench"],
        cwd=repo_path,
        capture_output=True,
        text=True,
        timeout=300
    )
    
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write(f"STDOUT:\n{result.stdout}\n")
        f.write(f"STDERR:\n{result.stderr}\n")
        f.write(f"Return code: {result.returncode}\n")
    
    if result.returncode == 0:
        print(f"[PASS] Bench Zig OK — log: {log_file}")
        # Afficher les resultats du bench
        for line in result.stdout.split('\n'):
            if 'tokens' in line.lower() or 'sec' in line.lower() or 'bench' in line.lower():
                print(f"  {line.strip()}")
        return True
    else:
        print(f"[FAIL] Bench Zig ECHEC (rc={result.returncode}) — log: {log_file}")
        print(result.stderr[-500:] if result.stderr else result.stdout[-500:])
        return False

def main():
    import argparse
    parser = argparse.ArgumentParser(description="MC-RNN ENV2 Benchmark")
    parser.add_argument("--repo-path", default=DEFAULT_REPO, help="Path to CodeDB-E5620")
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT, help="Output dir for logs")
    args = parser.parse_args()
    
    repo_path = Path(args.repo_path)
    output_dir = Path(args.output_dir)
    
    print("=" * 60)
    print("  MC-RNN ENV2 Benchmark")
    print("=" * 60)
    print(f"  Repo: {repo_path}")
    print(f"  Logs: {output_dir}")
    print(f"  Date: {datetime.now().isoformat()}")
    print("=" * 60)
    
    # Verifications
    if not repo_path.exists():
        print(f"[FAIL] Repo non trouve: {repo_path}")
        sys.exit(1)
    
    git_dir = repo_path / ".git"
    if not git_dir.exists():
        print(f"[FAIL] Pas un repo git: {repo_path}")
        sys.exit(1)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if not check_zig():
        sys.exit(1)
    
    # Executer
    test_ok = run_zig_test(str(repo_path), str(output_dir))
    bench_ok = run_zig_bench(str(repo_path), str(output_dir))
    
    # Resume
    print("\n" + "=" * 60)
    print("  RESULTAT")
    print("=" * 60)
    print(f"  Tests:  {'PASS' if test_ok else 'FAIL'}")
    print(f"  Bench:  {'PASS' if bench_ok else 'FAIL'}")
    print(f"  Logs:   {output_dir}")
    print("=" * 60)
    
    sys.exit(0 if (test_ok and bench_ok) else 1)

if __name__ == "__main__":
    main()
