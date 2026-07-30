# LLM Rate Limit Fallback Detector
# Part of skill: llm-rate-limit-fallback
# Detects Nemotron 3 Ultra (free) rate limit error and suggests fallback models

import re
import yaml
from pathlib import Path
from typing import Optional, List, Dict

# Pattern for the specific error
RATE_LIMIT_PATTERN = re.compile(
    r"Worker local total request limit reached \(\d+/32\)"
)

# Error signatures to detect
ERROR_SIGNATURES = [
    "ResourceExhausted: Worker local total request limit reached",
    "Upstream error from Nvidia: ResourceExhausted",
    "Worker local total request limit reached (32/32)",
]

DEFAULT_FALLBACK_MODELS = [
    {"id": "z.ai/glm-4.5", "provider": "openrouter", "free": True, "priority": 1, "reasoning": "high"},
    {"id": "qwen/qwen3-coder", "provider": "openrouter", "free": True, "priority": 2, "reasoning": "high"},
    {"id": "nvidia/nemotron-3-ultra-550b-a55b", "provider": "openrouter", "free": False, "priority": 3, "reasoning": "high"},
]


def detect_rate_limit_error(error_msg: str) -> bool:
    """Detect if error message matches Nemotron 3 Ultra free tier rate limit."""
    if not error_msg:
        return False
    for sig in ERROR_SIGNATURES:
        if sig in error_msg:
            return True
    return bool(RATE_LIMIT_PATTERN.search(error_msg))


def load_fallback_config(config_path: Path) -> List[Dict]:
    """Load fallback model configuration from YAML."""
    if not config_path.exists():
        return DEFAULT_FALLBACK_MODELS
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config.get("fallback_models", DEFAULT_FALLBACK_MODELS)


def get_fallback_model(config_path: Path, prefer_free: bool = True) -> Optional[str]:
    """Get the next fallback model based on priority and availability."""
    models = load_fallback_config(config_path)
    sorted_models = sorted(models, key=lambda m: m.get("priority", 999))
    
    for model in sorted_models:
        if prefer_free and not model.get("free", False):
            continue
        # TODO: Add budget check for paid models
        return model["id"]
    
    # Fallback to first available
    return sorted_models[0]["id"] if sorted_models else None


def suggest_fallback(error_msg: str, config_path: Path = None) -> Optional[str]:
    """Main entry point: given an error, suggest fallback model."""
    if not detect_rate_limit_error(error_msg):
        return None
    
    if config_path is None:
        config_path = Path(__file__).parent / "fallback.yaml"
    
    return get_fallback_model(config_path)


if __name__ == "__main__":
    # Test
    test_errors = [
        "Upstream error from Nvidia: ResourceExhausted: Worker local total request limit reached (32/32)",
        "ResourceExhausted: Worker local total request limit reached (15/32)",
        "Some other error",
    ]
    
    for err in test_errors:
        detected = detect_rate_limit_error(err)
        fallback = suggest_fallback(err) if detected else None
        print(f"Error: {err[:60]}...")
        print(f"  Detected: {detected}")
        print(f"  Fallback: {fallback}")
        print()
