#!/usr/bin/env python3
"""
LLM Rate Limit Fallback - Session Boot Hook
Runs at session start to check quota and warn user.
"""

import sys
from pathlib import Path

SKILL_DIR = Path(__file__).parent
sys.path.insert(0, str(SKILL_DIR))

from detector import load_fallback_config

def main():
    config_path = SKILL_DIR / 'fallback.yaml'
    config = load_fallback_config(config_path)
    
    print("=" * 60)
    print("LLM Rate Limit Fallback - Session Boot")
    print("=" * 60)
    print("Default model: nvidia/nemotron-3-ultra-550b-a55b:free")
    print("Hard limit: 32 requests/worker (OpenRouter free tier)")
    print()
    print("Configured fallback models:")
    for i, model in enumerate(config, 1):
        status = "FREE" if model.get('free') else "PAID"
        print(f"  {i}. {model['id']} ({status}) - priority {model['priority']}")
    print()
    print("WARNING: After ~32 requests, auto-fallback will trigger")
    print("   to next available model (GLM-4.5 -> Qwen3-Coder -> Nemotron paid)")
    print("=" * 60)
    print()

if __name__ == '__main__':
    main()