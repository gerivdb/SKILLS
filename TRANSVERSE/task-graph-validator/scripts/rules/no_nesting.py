#!/usr/bin/env python3
"""Rule: no_nesting — Pas de conditionnels imbriqués > 1 niveau."""

def validate_no_nesting(plan: dict) -> dict:
    errors = []
    warnings = []
    
    for step in plan.get("steps", []):
        step_id = step.get("id", "unknown")
        
        # Détecter patterns de nesting dans input/verify
        for field in ["input", "verify", "output"]:
            value = step.get(field)
            if not value:
                continue
            
            # Convertir en string pour analyse
            if isinstance(value, dict):
                val_str = str(value)
            elif isinstance(value, list):
                val_str = " ".join(str(v) for v in value)
            else:
                val_str = str(value)
            
            # Patterns de nesting détectés
            nesting_indicators = [
                ("if.*else.*if", "if/else imbriqués"),
                ("for.*for", "boucles for imbriquées"),
                ("while.*while", "boucles while imbriquées"),
                ("if.*for", "if dans for"),
                ("for.*if", "for dans if"),
            ]
            
            val_lower = val_str.lower()
            for pattern, desc in nesting_indicators:
                import re
                if re.search(pattern, val_lower):
                    warnings.append(f"[{step_id}] {field}: {desc} détecté (risque nesting > 1 niveau)")
    
    return {"errors": errors, "warnings": warnings}
