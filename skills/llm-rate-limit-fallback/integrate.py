#!/usr/bin/env python3
"""
LLM Rate Limit Fallback - Post-Error Hook
Detects rate limit errors and outputs fallback model for KiloCode auto-switch.
"""

import sys
import json
from pathlib import Path

SKILL_DIR = Path(__file__).parent
sys.path.insert(0, str(SKILL_DIR))

from detector import detect_rate_limit_error, suggest_fallback

def main():
    # Read error from stdin or first argument
    if len(sys.argv) > 1:
        error_message = " ".join(sys.argv[1:])
    else:
        error_message = sys.stdin.read()
    
    if not error_message.strip():
        sys.exit(0)
    
    config_path = SKILL_DIR / 'fallback.yaml'
    
    detected = detect_rate_limit_error(error_message)
    
    if not detected:
        sys.exit(0)
    
    fallback = suggest_fallback(error_message, config_path)
    
    if fallback:
        # Output JSON for KiloCode hook parsing
        result = {
            "detected": True,
            "fallback_model": fallback,
            "error_type": "rate_limit_nemotron_free",
            "original_error": error_message[:200]
        }
        print(json.dumps(result))
        
        # Also print human-readable for logs
        print(f"[LLM_FALLBACK] Detected Nemotron 3 Ultra rate limit -> switching to {fallback}", file=sys.stderr)

if __name__ == '__main__':
    main()