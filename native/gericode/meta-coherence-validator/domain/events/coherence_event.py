"""
Domain Events for Meta Coherence Validator.

Events are emitted during validation to track state changes.
"""

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class ValidationStarted:
    """Event emitted when validation starts."""
    prd_moc_count: int


@dataclass
class PrdMocValidated:
    """Event emitted when a single PRD MOC is validated."""
    prd_moc_path: str
    score: float
    missing_count: int
    contradiction_count: int


@dataclass
class ContradictionDetected:
    """Event emitted when a contradiction is detected."""
    prd_moc_path: str
    reference: str
    details: str


@dataclass
class MissingReferenceDetected:
    """Event emitted when a missing reference is detected."""
    prd_moc_path: str
    reference: str
    reason: str


@dataclass
class ValidationCompleted:
    """Event emitted when validation completes."""
    global_score: float
    prd_moc_count: int
    total_missing: int
    total_contradictions: int
    blocked: bool
