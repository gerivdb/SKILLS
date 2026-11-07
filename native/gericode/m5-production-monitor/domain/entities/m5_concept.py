"""Domain entity for m5-production-monitor."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class M5ConceptEntity:
    """Domain entity representing an M5 concept."""

    concept_id: str
    phase: str
    maturity_score: float
    state: str
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Convert entity to dictionary."""
        return {
            "concept_id": self.concept_id,
            "phase": self.phase,
            "maturity_score": self.maturity_score,
            "state": self.state,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict) -> M5ConceptEntity:
        """Create entity from dictionary."""
        return cls(
            concept_id=data["concept_id"],
            phase=data["phase"],
            maturity_score=data["maturity_score"],
            state=data["state"],
            created_at=datetime.fromisoformat(data.get("created_at", datetime.now().isoformat())),
            updated_at=datetime.fromisoformat(data.get("updated_at", datetime.now().isoformat())),
            metadata=data.get("metadata", {}),
        )

    def is_embryo(self) -> bool:
        """Check if concept is an embryo."""
        return self.maturity_score < 0.3

    def is_developing(self) -> bool:
        """Check if concept is developing."""
        return 0.3 <= self.maturity_score < 0.6

    def is_stable(self) -> bool:
        """Check if concept is stable."""
        return 0.6 <= self.maturity_score < 0.8

    def is_mature(self) -> bool:
        """Check if concept is mature."""
        return self.maturity_score >= 0.8

    def get_target_phase(self) -> str:
        """Get next phase in the M5 cycle."""
        phase_order = ["detectBirth", "develop", "stabilize", "integrate", "lifecycle"]
        try:
            index = phase_order.index(self.phase)
            return phase_order[index + 1] if index + 1 < len(phase_order) else self.phase
        except ValueError:
            return self.phase
