"""
Repository Contracts for Meta Coherence Validator.

Defines interfaces for reading PRD MOC documents and external references.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Set
from pathlib import Path
from ..entities.prd_moc_entity import PrdMoc
from ..value_objects.reference_vo import Reference


class PrdMocRepository(ABC):
    """Repository for reading PRD MOC documents."""

    @abstractmethod
    def find_all(self, paths: List[Path]) -> List[PrdMoc]:
        """Find all PRD MOC documents at given paths."""
        pass

    @abstractmethod
    def get_by_path(self, path: Path) -> Optional[PrdMoc]:
        """Get a single PRD MOC by path."""
        pass


class DesignRepository(ABC):
    """Repository for checking design existence."""

    @abstractmethod
    def exists(self, design_path: str) -> bool:
        """Check if a design file exists."""
        pass

    @abstractmethod
    def list_all(self) -> Set[str]:
        """List all available design paths."""
        pass


class OntologyRepository(ABC):
    """Repository for checking ontology concept existence."""

    @abstractmethod
    def concept_exists(self, concept_id: str) -> bool:
        """Check if a concept exists in ONTOLOGY."""
        pass

    @abstractmethod
    def citizen_exists(self, citizen_id: str) -> bool:
        """Check if a citizen exists in ONTOLOGY."""
        pass


class SkillRepository(ABC):
    """Repository for checking skill existence."""

    @abstractmethod
    def skill_exists(self, skill_path: str) -> bool:
        """Check if a skill directory exists."""
        pass

    @abstractmethod
    def is_registered(self, skill_name: str) -> bool:
        """Check if a skill is registered in REGISTRY.yaml."""
        pass


class BootSequenceRepository(ABC):
    """Repository for checking boot sequence steps."""

    @abstractmethod
    def step_exists(self, step_name: str) -> bool:
        """Check if a boot step exists in session-boot-sequence.md."""
        pass
