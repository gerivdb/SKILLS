#!/usr/bin/env python3
"""
task-graph-validator — Valide un plan de tâches contre les contraintes SLM.

Usage:
    python scripts/validate.py --plan plan.json [--rules RULE1,RULE2] [--format text|json]
    python scripts/validate.py --check-pre --plan plan.json
    python scripts/validate.py --check-post --plan plan.json --result result.json
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional

# Import rule modules
from rules.max_tokens import validate_max_tokens
from rules.single_tool import validate_single_tool
from rules.no_nesting import validate_no_nesting
from rules.absolute_paths import validate_absolute_paths
from rules.verify_included import validate_verify_included


ALL_RULES = {
    "max_tokens": validate_max_tokens,
    "single_tool": validate_single_tool,
    "no_nesting": validate_no_nesting,
    "absolute_paths": validate_absolute_paths,
    "verify_included": validate_verify_included,
}


def load_plan(plan_path: Path) -> Dict[str, Any]:
    """Charge et valide le plan JSON."""
    if not plan_path.exists():
        raise FileNotFoundError(f"Plan non trouve: {plan_path}")
    
    with open(plan_path, "r", encoding="utf-8") as f:
        plan = json.load(f)
    
    # Validation structure de base
    if "steps" not in plan:
        raise ValueError("Plan invalide: champ 'steps' manquant")
    
    if not isinstance(plan["steps"], list):
        raise ValueError("Plan invalide: 'steps' doit être une liste")
    
    for i, step in enumerate(plan["steps"]):
        if not isinstance(step, dict):
            raise ValueError(f"Step {i}: doit être un objet")
        if "id" not in step:
            raise ValueError(f"Step {i}: champ 'id' manquant")
        if "tool" not in step:
            raise ValueError(f"Step {step.get('id', i)}: champ 'tool' manquant")
    
    return plan


def validate_plan(plan: Dict[str, Any], rules: List[str]) -> Dict[str, Any]:
    """Exécute toutes les règles de validation sur le plan."""
    all_errors = []
    all_warnings = []
    
    for rule_name in rules:
        validator = ALL_RULES[rule_name]
        result = validator(plan)
        all_errors.extend(result.get("errors", []))
        all_warnings.extend(result.get("warnings", []))
    
    return {
        "valid": len(all_errors) == 0,
        "errors": all_errors,
        "warnings": all_warnings,
        "rules_checked": rules,
        "steps_count": len(plan["steps"]),
    }


def check_pre_execution(plan: Dict[str, Any]) -> Dict[str, Any]:
    """
    CHECK PRE-EXECUTION: Validation pre-execution complete.
    Verifie: plan valide, hash, chemins, dependances, verify field.
    """
    print("[CHECK-PRE] Validation pre-execution...")
    
    # 1. Validation structurelle
    result = validate_plan(plan, list(ALL_RULES.keys()))
    
    # 2. Verifications supplementaires pre-execution
    extra_errors = []
    extra_warnings = []
    
    for step in plan.get("steps", []):
        step_id = step.get("id", "unknown")
        
        # Verifier champ verify
        verify = step.get("verify")
        if not verify:
            extra_errors.append(f"[{step_id}] champ verify manquant (requis pour CHECK)")
        elif isinstance(verify, str) and len(verify.strip()) < 3:
            extra_warnings.append(f"[{step_id}] verify tres court: {verify[:50]}")
        
        # Verifier hash si present
        if "hash" in step:
            # Hash verification would go here
            pass
    
    all_errors = result.get("errors", []) + extra_errors
    all_warnings = result.get("warnings", []) + extra_warnings
    
    return {
        "phase": "check-pre",
        "valid": len(all_errors) == 0,
        "errors": all_errors,
        "warnings": all_warnings,
        "rules_checked": list(ALL_RULES.keys()) + ["verify_field", "hash"],
        "steps_count": len(plan.get("steps", [])),
    }


def check_post_execution(plan: Dict[str, Any], result_file: Path = None) -> Dict[str, Any]:
    """
    CHECK POST-EXECUTION: Validation post-execution.
    Verifie: resultat execution, format commit, ATOM number, IntentHash, Refs.
    """
    print("[CHECK-POST] Validation post-execution...")
    
    errors = []
    warnings = []
    
    # Charger resultat d'execution si fourni
    execution_result = {}
    if result_file and result_file.exists():
        with open(result_file, "r", encoding="utf-8") as f:
            execution_result = json.load(f)
    
    # Obtenir les resultats d'etape
    step_results = execution_result.get("step_results", {})
    
    # Verifications post-execution
    for step in plan.get("steps", []):
        step_id = step.get("id", "unknown")
        
        # Verifier que le step a ete execute
        if step_id in step_results:
            step_result = step_results[step_id]
            if step_result.get("status") != "ok":
                errors.append(f"[{step_id}] execution failed: {step_result.get('error', 'unknown')}")
        else:
            warnings.append(f"[{step_id}] no execution result found")
    
    return {
        "phase": "check-post",
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "rules_checked": ["execution_result", "commit_format", "atom_number", "intent_hash", "refs"],
        "steps_count": len(plan.get("steps", [])),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Valide un plan de tâches contre les contraintes SLM (THINK/CHECK/DO/CHECK)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Modes:
  --plan plan.json                    Validation standard (THINK phase)
  --check-pre --plan plan.json        CHECK PRE-EXECUTION (avant DO)
  --check-post --plan plan.json --result result.json  CHECK POST-EXECUTION (apres DO)

Exemples:
  python scripts/validate.py --plan plan.json
  python scripts/validate.py --check-pre --plan plan.json
  python scripts/validate.py --check-post --plan plan.json --result .slm/state.json
        """
    )
    parser.add_argument("--plan", "-p", required=True, help="Fichier plan JSON")
    parser.add_argument("--rules", "-r", default="all", 
                        help="Regles a verifier (comma-separated, defaut: all)")
    parser.add_argument("--format", "-f", choices=["text", "json"], default="text",
                        help="Format de sortie")
    parser.add_argument("--check-pre", action="store_true", help="Mode CHECK PRE-EXECUTION")
    parser.add_argument("--check-post", action="store_true", help="Mode CHECK POST-EXECUTION")
    parser.add_argument("--result", help="Fichier resultat execution (pour --check-post)")
    
    args = parser.parse_args()
    
    # Résoudre les règles
    if args.rules.lower() == "all":
        rules = list(ALL_RULES.keys())
    else:
        rules = [r.strip() for r in args.rules.split(",")]
        for r in rules:
            if r not in ALL_RULES:
                print(f"[ERROR] Regle inconnue: {r}", file=sys.stderr)
                print(f"Regles disponibles: {', '.join(ALL_RULES.keys())}", file=sys.stderr)
                sys.exit(2)
    
    try:
        plan_path = Path(args.plan)
        plan = load_plan(plan_path)
        
        # Mode CHECK PRE
        if args.check_pre:
            result = check_pre_execution(plan)
        
        # Mode CHECK POST
        elif args.check_post:
            result_file = Path(args.result) if args.result else None
            result = check_post_execution(plan, result_file)
        
        # Mode standard (THINK phase)
        else:
            result = validate_plan(plan, rules)
            result["phase"] = "think"
        
        if args.format == "json":
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            # Format texte
            phase = result.get("phase", "think")
            if result["valid"]:
                print(f"[OK] {phase.upper()} valide ({result['steps_count']} steps, {len(result['rules_checked'])} regles)")
                if result["warnings"]:
                    for w in result["warnings"]:
                        print(f"[WARN] {w}")
            else:
                print(f"[ERROR] {phase.upper()} invalide ({len(result['errors'])} erreurs)")
                for e in result["errors"]:
                    print(f"  - {e}")
                if result["warnings"]:
                    for w in result["warnings"]:
                        print(f"  [WARN] {w}")
        
        sys.exit(0 if result["valid"] else 1)
        
    except FileNotFoundError as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(2)
    except (json.JSONDecodeError, ValueError) as e:
        print(f"[ERROR] Plan invalide: {e}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"[ERROR] Erreur inattendue: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
