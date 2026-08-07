"""Domain entity for m5-production-monitor."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class M5ConceptEntity:
    """Domain entity for m5-production-monitor."""

    concept_id: str
    phase: str
    maturity_score: float
    state: str

    def to_dict(self) -> dict:
        """Convert entity to dictionary."""
        return {
            "concept_id": self.concept_id,
            "phase": self.phase,
            "maturity_score": self.maturity_score,
            "state": self.state,
        }

    @classmethod
    def from_dict(cls, data: dict) -> M5ConceptEntity:
        """Create entity from dictionary."""
        return cls(
            concept_id=data["concept_id"],
            phase=data["phase"],
            maturity_score=data["maturity_score"],
            state=data["state"],
        )
