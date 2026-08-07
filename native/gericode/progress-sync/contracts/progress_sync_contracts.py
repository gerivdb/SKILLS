"""DbC contracts for progress-sync."""

from __future__ import annotations


def validate_input(data: dict) -> bool:
    """Validate input data contract."""
    if not isinstance(data, dict):
        raise TypeError("Input must be a dictionary")
    return True


def validate_output(result: dict) -> bool:
    """Validate output data contract."""
    if not isinstance(result, dict):
        raise TypeError("Output must be a dictionary")
    return True
