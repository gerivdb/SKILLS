#!/usr/bin/env python3
"""
atomic-task-planner -- Decompose une tache en micro-steps SLM atomiques.

Usage:
    python scripts/plan.py --task "..." --context "..." [--output plan.json]
    python scripts/plan.py --spec spec.yaml --output plan.json
    python scripts/plan.py --list-templates
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
import re


# Templates de decomposition
TEMPLATES = {
    "A": {
        "name": "file_creation",
        "description": "Creer un fichier (read -> write -> verify)",
        "steps": [
            {"tool": "read", "desc": "Lire fichier existant ou template", "tokens": 80},
            {"tool": "write", "desc": "Creer nouveau fichier", "tokens": 120},
            {"tool": "bash", "desc": "Verifier creation", "tokens": 50},
        ]
    },
    "B": {
        "name": "batch_patch",
        "description": "Modifier plusieurs fichiers (read -> edit x N -> verify)",
        "steps": [
            {"tool": "read", "desc": "Lister fichiers cibles", "tokens": 80},
            {"tool": "edit", "desc": "Appliquer patch fichier 1", "tokens": 120},
            {"tool": "edit", "desc": "Appliquer patch fichier 2", "tokens": 120},
            {"tool": "bash", "desc": "Verifier tous patches", "tokens": 60},
        ]
    },
    "C": {
        "name": "gap_resolution",
        "description": "Resoudre gap SGR (read gap -> analyze -> implement -> test -> verify)",
        "steps": [
            {"tool": "read", "desc": "Lire rapport gap", "tokens": 80},
            {"tool": "bash", "desc": "Analyser cause racine", "tokens": 100},
            {"tool": "edit", "desc": "Implementer correction", "tokens": 130},
            {"tool": "bash", "desc": "Tester correction", "tokens": 80},
            {"tool": "bash", "desc": "Verifier gap resolu", "tokens": 60},
        ]
    },
    "D": {
        "name": "cli_command",
        "description": "Executer commande CLI (bash -> verify)",
        "steps": [
            {"tool": "bash", "desc": "Executer commande", "tokens": 100},
            {"tool": "bash", "desc": "Verifier resultat", "tokens": 50},
        ]
    },
}


def estimate_tokens(text: str) -> int:
    """Estimation grossiere: ~4 chars = 1 token."""
    return max(50, len(text) // 4)


def select_template(task: str, context: str) -> str:
    """Selection auto du template base sur mots-cles."""
    text = (task + " " + context).lower()
    
    if any(kw in text for kw in ["creer", "create", "nouveau", "new", "generate", "generer", "fichier", "file"]):
        return "A"
    elif any(kw in text for kw in ["patch", "modifier", "modify", "edit", "appliquer", "appliquer", "fichiers", "multiple"]):
        return "B"
    elif any(kw in text for kw in ["gap", "resoudre", "resolve", "corriger", "fix", "erreur", "error"]):
        return "C"
    elif any(kw in text for kw in ["executer", "run", "commande", "command", "cli", "script", "bash"]):
        return "D"
    
    return "A"  # Default


def generate_plan(task: str, context: str, template_id: str, base_path: str = "D:/DO/WEB/TOOLS/L1-INFRA/ECOS-CLI") -> Dict[str, Any]:
    """Genere un plan JSON a partir du template."""
    template = TEMPLATES[template_id]
    
    steps = []
    for i, step_tpl in enumerate(template["steps"], 1):
        step_id = f"step-{i}"
        
        # Construire input selon tool
        input_data = {}
        if step_tpl["tool"] == "read":
            input_data = {"path": f"{base_path}/TODO"}  # Placeholder
        elif step_tpl["tool"] == "write":
            input_data = {"path": f"{base_path}/NEW_FILE.py", "content": "# TODO"}
        elif step_tpl["tool"] == "edit":
            input_data = {"path": f"{base_path}/TODO.py", "old": "TODO", "new": "IMPLEMENTED"}
        elif step_tpl["tool"] == "bash":
            input_data = {"command": "echo 'TODO: implement verification'"}
        
        # Construire verify selon tool
        verify_map = {
            "read": f"Test-Path {base_path}/TODO",
            "write": f"Test-Path {base_path}/NEW_FILE.py",
            "edit": f"Select-String 'IMPLEMENTED' {base_path}/TODO.py",
            "bash": "echo 'Verification complete'",
        }
        
        step = {
            "id": step_id,
            "tool": step_tpl["tool"],
            "input": input_data,
            "output": step_tpl["desc"],
            "verify": verify_map.get(step_tpl["tool"], "echo 'verify'"),
            "tokens_est": step_tpl["tokens"],
        }
        steps.append(step)
    
    # Dependencies: lineaire par defaut
    deps = []
    for i in range(1, len(steps)):
        deps.append({"from": f"step-{i}", "to": f"step-{i+1}"})
    
    return {
        "steps": steps,
        "deps": deps,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Decompose une tache en micro-steps SLM atomiques",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--task", "-t", help="Description de la tache")
    parser.add_argument("--context", "-c", default="", help="Contexte additionnel")
    parser.add_argument("--spec", "-s", help="Fichier spec YAML")
    parser.add_argument("--output", "-o", help="Fichier sortie plan JSON")
    parser.add_argument("--template", choices=["A", "B", "C", "D"], help="Template force")
    parser.add_argument("--list-templates", action="store_true", help="Lister templates")
    parser.add_argument("--base-path", default="D:/DO/WEB/TOOLS/L1-INFRA/ECOS-CLI", help="Chemin de base repo")
    
    args = parser.parse_args()
    
    if args.list_templates:
        print("Templates disponibles:")
        for tid, tpl in TEMPLATES.items():
            print(f"  {tid} - {tpl['name']}: {tpl['description']}")
            print(f"     Steps: {len(tpl['steps'])}")
        return
    
    if args.spec:
        # Charger spec YAML
        import yaml
        spec_path = Path(args.spec)
        if not spec_path.exists():
            print(f"[ERROR] Spec non trouvee: {spec_path}", file=sys.stderr)
            sys.exit(2)
        with open(spec_path, "r", encoding="utf-8") as f:
            spec = yaml.safe_load(f)
        task = spec.get("task", "")
        context = spec.get("context", "")
        template_id = spec.get("template", None)
    elif args.task:
        task = args.task
        context = args.context
        template_id = args.template
    else:
        print("[ERROR] --task ou --spec requis", file=sys.stderr)
        sys.exit(2)
    
    if not template_id:
        template_id = select_template(task, context)
        print(f"[INFO] Template auto-selecte: {template_id} ({TEMPLATES[template_id]['name']})", file=sys.stderr)
    
    if template_id not in TEMPLATES:
        print(f"[ERROR] Template inconnu: {template_id}", file=sys.stderr)
        sys.exit(2)
    
    plan = generate_plan(task, context, template_id, args.base_path)
    
    # Output
    if args.output:
        Path(args.output).write_text(json.dumps(plan, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[OK] Plan genere -> {args.output}", file=sys.stderr)
    else:
        print(json.dumps(plan, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
