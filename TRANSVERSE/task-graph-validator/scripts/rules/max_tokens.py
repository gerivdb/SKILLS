#!/usr/bin/env python3
"""Rule: max_tokens — tokens_est <= 150 par step."""

def validate_max_tokens(plan: dict) -> dict:
    errors = []
    warnings = []
    
    for step in plan.get("steps", []):
        step_id = step.get("id", "unknown")
        tokens = step.get("tokens_est")
        
        if tokens is None:
            errors.append(f"[{step_id}] tokens_est manquant")
        elif not isinstance(tokens, int):
            errors.append(f"[{step_id}] tokens_est doit être un entier (recu: {type(tokens).__name__})")
        elif tokens > 150:
            errors.append(f"[{step_id}] tokens_est={tokens} > 150 (max SLM)")
        elif tokens > 120:
            warnings.append(f"[{step_id}] tokens_est={tokens} proche limite 150")
    
    return {"errors": errors, "warnings": warnings}
