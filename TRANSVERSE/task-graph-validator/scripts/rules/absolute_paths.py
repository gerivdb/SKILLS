#!/usr/bin/env python3
"""Rule: absolute_paths — Chemins absolus obligatoires."""

import os

def validate_absolute_paths(plan: dict) -> dict:
    errors = []
    warnings = []
    
    for step in plan.get("steps", []):
        step_id = step.get("id", "unknown")
        input_data = step.get("input")
        
        if not input_data:
            continue
        
        # Chercher des chemins dans input
        paths_to_check = []
        if isinstance(input_data, dict):
            for key, value in input_data.items():
                if isinstance(value, str) and ("path" in key.lower() or "file" in key.lower() or "dir" in key.lower()):
                    paths_to_check.append((key, value))
                elif isinstance(value, str) and (value.startswith("/") or value.startswith("\\") or ":" in value[:3]):
                    paths_to_check.append((key, value))
        
        for field_name, path in paths_to_check:
            if not path:
                continue
            
            # Vérifier si chemin absolu
            is_absolute = (
                path.startswith("/") or  # Unix
                (len(path) > 2 and path[1] == ":" and path[2] in ("\\", "/")) or  # Windows C:\
                path.startswith("\\\\")  # UNC
            )
            
            if not is_absolute:
                errors.append(f"[{step_id}] {field_name}: chemin relatif détecté: {path} (absolu requis)")
    
    return {"errors": errors, "warnings": warnings}
