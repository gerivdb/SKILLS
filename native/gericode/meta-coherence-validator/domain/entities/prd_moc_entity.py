"""
Entity: PrdMoc

Represents a PRD MOC document with its metadata and references.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from ..value_objects.reference_vo import Reference


@dataclass
class PrdMoc:
    """PRD MOC document entity."""
    path: str
    title: str
    intent_hash: str
    references: List[Reference] = field(default_factory=list)
    missing_references: List[Dict[str, str]] = field(default_factory=list)
    contradictions: List[Dict[str, Any]] = field(default_factory=list)
    score: float = 0.0

    def add_reference(self, reference: Reference) -> None:
        """Add a reference to this PRD MOC."""
        self.references.append(reference)

    def add_missing_reference(self, ref_string: str, reason: str) -> None:
        """Record a missing reference."""
        self.missing_references.append({
            "reference": ref_string,
            "reason": reason,
        })

    def add_contradiction(self, ref_string: str, details: str) -> None:
        """Record a contradiction."""
        self.contradictions.append({
            "reference": ref_string,
            "details": details,
        })

    def compute_score(self, total_references: int) -> float:
        """Compute coherence score for this PRD MOC."""
        if total_references == 0:
            return 1.0
        valid = total_references - len(self.missing_references)
        penalty = len(self.contradictions) * 0.1
        self.score = max(0.0, (valid / total_references) - penalty)
        return self.score
