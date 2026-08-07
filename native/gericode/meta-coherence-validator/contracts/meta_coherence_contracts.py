"""
Contracts for Meta Coherence Validator.

Defines input/output contracts for the skill.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class ValidationInput:
    """Input contract for meta coherence validation."""
    prd_moc_paths: List[str]
    unified_design_path: str
    ontology_path: str
    skills_registry: str
    boot_sequence_path: str


@dataclass
class ValidationOutput:
    """Output contract for meta coherence validation."""
    global_score: float
    prd_mocs_validated: int
    contradictions_detected: int
    missing_references: List[Dict[str, str]]
    orphan_references: List[str]
    inconsistent_definitions: List[Dict[str, str]]
    recommendations: List[str]
    blocked: bool


@dataclass
class PrdMocValidationDetail:
    """Detail for a single PRD MOC validation."""
    prd_moc: str
    score: float
    missing: List[str]
    contradictions: List[str]
