#!/usr/bin/env python3
"""
slm-micro-executor -- Execute UNE micro-tache atomique (1 step = 1 tool call).

Usage:
    python scripts/execute.py --plan plan.json [--step step-1] [--resume] [--list-steps] [--reset]
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, Any, List, Optional


class StateManager:
    """Gestionnaire d etat persistant (.slm/state.json)."""
    
    def __init__(self, state_dir: Path):
        self.state_dir = state_dir
        self.state_file = state_dir / "state.json"
        self.state_dir.mkdir(exist_ok=True)
    
    def load(self) -> Optional[Dict[str, Any]]:
        if self.state_file.exists():
            with open(self.state_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return None
    
    def save(self, state: Dict[str, Any]) -> None:
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
    
    def reset(self) -> None:
        if self.state_file.exists():
            self.state_file.unlink()
    
    def plan_hash(self, plan: Dict[str, Any]) -> str:
        """Hash stable du plan pour verification coherence."""
        plan_str = json.dumps(plan, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(plan_str.encode()).hexdigest()[:16]


class StepExecutor:
    """Execute un step atomique (1 tool call)."""
    
    def __init__(self, base_path: Path):
        self.base_path = base_path
    
    def execute(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """Execute un step et retourne resultat."""
        tool = step.get("tool")
        input_data = step.get("input", {})
        verify = step.get("verify", "")
        
        start = time.time()
        
        try:
            if tool == "read":
                output = self._exec_read(input_data)
            elif tool == "write":
                output = self._exec_write(input_data)
            elif tool == "edit":
                output = self._exec_edit(input_data)
            elif tool == "bash":
                output = self._exec_bash(input_data)
            else:
                raise ValueError(f"Tool inconnu: {tool}")
            
            duration_ms = int((time.time() - start) * 1000)
            
            # Verification
            verify_ok = True
            verify_output = ""
            if verify:
                verify_ok, verify_output = self._run_verify(verify)
            
            return {
                "status": "ok" if verify_ok else "verify_failed",
                "output": output,
                "verify_output": verify_output,
                "verify_ok": verify_ok,
                "duration_ms": duration_ms,
            }
            
        except Exception as e:
            duration_ms = int((time.time() - start) * 1000)
            return {
                "status": "error",
                "error": str(e),
                "duration_ms": duration_ms,
            }
    
    def _exec_read(self, input_data: Dict[str, Any]) -> str:
        path = Path(input_data.get("path", ""))
        if not path.is_absolute():
            path = self.base_path / path
        return path.read_text(encoding="utf-8")
    
    def _exec_write(self, input_data: Dict[str, Any]) -> str:
        path = Path(input_data.get("path", ""))
        if not path.is_absolute():
            path = self.base_path / path
        content = input_data.get("content", "")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return f"Written {len(content)} chars to {path}"
    
    def _exec_edit(self, input_data: Dict[str, Any]) -> str:
        path = Path(input_data.get("path", ""))
        if not path.is_absolute():
            path = self.base_path / path
        old = input_data.get("old", "")
        new = input_data.get("new", "")
        content = path.read_text(encoding="utf-8")
        if old not in content:
            raise ValueError(f"Pattern non trouve: {old[:50]}...")
        content = content.replace(old, new)
        path.write_text(content, encoding="utf-8")
        return f"Replaced in {path}"
    
    def _exec_bash(self, input_data: Dict[str, Any]) -> str:
        command = input_data.get("command", "")
        cwd = input_data.get("cwd", str(self.base_path))
        result = subprocess.run(
            command, shell=True, cwd=cwd,
            capture_output=True, text=True, timeout=60
        )
        if result.returncode != 0:
            raise RuntimeError(f"Bash failed ({result.returncode}): {result.stderr}")
        return result.stdout
    
    def _run_verify(self, verify_cmd: str) -> tuple[bool, str]:
        try:
            result = subprocess.run(
                verify_cmd, shell=True, cwd=str(self.base_path),
                capture_output=True, text=True, timeout=30
            )
            return result.returncode == 0, result.stdout
        except Exception as e:
            return False, str(e)


def load_plan(plan_path: Path) -> Dict[str, Any]:
    with open(plan_path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(
        description="Execute micro-steps SLM (1 step = 1 tool call)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--plan", "-p", required=True, help="Fichier plan JSON")
    parser.add_argument("--step", "-s", help="Executer seulement ce step (ex: step-1)")
    parser.add_argument("--resume", "-r", action="store_true", help="Reprendre depuis etat")
    parser.add_argument("--list-steps", "-l", action="store_true", help="Lister steps sans executer")
    parser.add_argument("--reset", action="store_true", help="Reset etat .slm/state.json")
    parser.add_argument("--state-dir", default=".slm", help="Repertoire etat")
    parser.add_argument("--base-path", default="D:/DO/WEB/TOOLS/L1-INFRA/ECOS-CLI", help="Chemin base repo")
    
    args = parser.parse_args()
    
    plan_path = Path(args.plan)
    if not plan_path.exists():
        print(f"[ERROR] Plan non trouve: {plan_path}", file=sys.stderr)
        sys.exit(2)
    
    plan = load_plan(plan_path)
    base_path = Path(args.base_path)
    state_mgr = StateManager(Path(args.state_dir))
    executor = StepExecutor(base_path)
    
    # Reset si demande
    if args.reset:
        state_mgr.reset()
        print("[OK] Etat reset")
    
    # Charger etat si resume
    state = state_mgr.load() if args.resume else None
    plan_hash = state_mgr.plan_hash(plan)
    
    if state and state.get("plan_hash") != plan_hash:
        print("[WARN] Plan change depuis dernier run, reset etat", file=sys.stderr)
        state = None
        state_mgr.reset()
    
    # Liste steps
    if args.list_steps:
        for i, step in enumerate(plan.get("steps", []), 1):
            status = "pending"
            if state and step["id"] in state.get("completed_steps", []):
                status = "done"
            print(f"  {i}. {step["id"]}: {step["tool"]} - {status}")
        return
    
    # Filtrer steps a executer
    steps = plan.get("steps", [])
    if args.step:
        steps = [s for s in steps if s["id"] == args.step]
        if not steps:
            print(f"[ERROR] Step non trouve: {args.step}", file=sys.stderr)
            sys.exit(2)
    
    # Initialiser etat si nouveau
    if not state:
        state = {
            "plan_hash": plan_hash,
            "current_step": 0,
            "completed_steps": [],
            "step_results": {},
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
    
    # Executer steps
    all_ok = True
    for step in steps:
        step_id = step["id"]
        
        # Skip si deja fait (resume)
        if args.resume and step_id in state.get("completed_steps", []):
            print(f"[SKIP] {step_id} (deja execute)")
            continue
        
        print(f"[EXEC] {step_id}: {step["tool"]} - {step.get("output", "")[:60]}")
        
        result = executor.execute(step)
        state["step_results"][step_id] = result
        state["current_step"] = state["current_step"] + 1
        
        if result["status"] == "ok":
            state["completed_steps"].append(step_id)
            print(f"  [OK] {step_id} ({result["duration_ms"]}ms)")
        else:
            print(f"  [ERROR] {step_id}: {result.get("error", result["status"])}")
            if result.get("verify_output"):
                print(f"  Verify: {result["verify_output"][:200]}")
            all_ok = False
            break
        
        # Sauver etat apres chaque step
        state_mgr.save(state)
    
    # Final save
    state_mgr.save(state)
    
    if all_ok:
        print("[OK] Tous steps executes avec succes")
        sys.exit(0)
    else:
        print("[ERROR] Execution arretee sur erreur", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    import time
    main()
