#!/usr/bin/env python3
"""Rule: single_tool — 1 seul outil par step."""

VALID_TOOLS = {"read", "write", "edit", "bash", "glob", "grep", "task"}

def validate_single_tool(plan: dict) -> dict:
    errors = []
    warnings = []
    
    for step in plan.get("steps", []):
        step_id = step.get("id", "unknown")
        tool = step.get("tool")
        
        if not tool:
            errors.append(f"[{step_id}] champ tool manquant")
        elif tool not in VALID_TOOLS:
            warnings.append(f"[{step_id}] tool non standard: {tool} (attendu: {VALID_TOOLS})")
        # Vérifier qu'il n'y a pas de clés tool_* multiples
        tool_keys = [k for k in step.keys() if k.startswith("tool")]
        if len(tool_keys) > 1:
            errors.append(f"[{step_id}] multiples clés tool-like: {tool_keys}")
    
    return {"errors": errors, "warnings": warnings}
