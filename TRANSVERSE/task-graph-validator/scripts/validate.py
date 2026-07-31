#!/usr/bin/env python3
"""
task-graph-validator — Valide un plan de tâches contre les contraintes SLM.

Usage:
    python scripts/validate.py --plan plan.json [--rules RULE1,RULE2] [--format text|json]
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


def main():
    parser = argparse.ArgumentParser(
        description="Valide un plan de tâches contre les contraintes SLM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  python scripts/validate.py --plan plan.json
  python scripts/validate.py --plan plan.json --rules max_tokens,single_tool
  python scripts/validate.py --plan plan.json --format json
        """
    )
    parser.add_argument("--plan", "-p", required=True, help="Fichier plan JSON")
    parser.add_argument("--rules", "-r", default="all", 
                        help="Regles a verifier (comma-separated, defaut: all)")
    parser.add_argument("--format", "-f", choices=["text", "json"], default="text",
                        help="Format de sortie")
    
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
        result = validate_plan(plan, rules)
        
        if args.format == "json":
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            # Format texte
            if result["valid"]:
                print(f"[OK] Plan valide ({result['steps_count']} steps, {len(rules)} regles)")
                if result["warnings"]:
                    for w in result["warnings"]:
                        print(f"[WARN] {w}")
            else:
                print(f"[ERROR] Plan invalide ({len(result['errors'])} erreurs)")
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
