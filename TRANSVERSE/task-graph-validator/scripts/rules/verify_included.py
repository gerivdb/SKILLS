#!/usr/bin/env python3
"""Rule: verify_included — Chaque step a un champ verify non-vide."""

def validate_verify_included(plan: dict) -> dict:
    errors = []
    warnings = []
    
    for step in plan.get("steps", []):
        step_id = step.get("id", "unknown")
        verify = step.get("verify")
        
        if verify is None:
            errors.append(f"[{step_id}] champ verify manquant")
        elif not verify or (isinstance(verify, str) and not verify.strip()):
            errors.append(f"[{step_id}] verify vide")
        elif isinstance(verify, str) and len(verify) < 5:
            warnings.append(f"[{step_id}] verify très court: {verify[:50]}")
    
    return {"errors": errors, "warnings": warnings}
