"""
Application Ports (outbound) for Meta Coherence Validator.

Defines interfaces to external dependencies.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from pathlib import Path


class PrdMocReaderPort(ABC):
    """Port for reading PRD MOC documents."""

    @abstractmethod
    def read_prd_mocs(self, paths: List[Path]) -> List[Dict]:
        """Read PRD MOC documents from filesystem."""
        pass


class ReferenceCheckerPort(ABC):
    """Port for checking reference existence."""

    @abstractmethod
    def check_design_exists(self, design_path: str) -> bool:
        """Check if a design file exists."""
        pass

    @abstractmethod
    def check_concept_exists(self, concept_id: str) -> bool:
        """Check if a concept exists in ONTOLOGY."""
        pass

    @abstractmethod
    def check_skill_exists(self, skill_path: str) -> bool:
        """Check if a skill directory exists."""
        pass

    @abstractmethod
    def check_citizen_exists(self, citizen_id: str) -> bool:
        """Check if a citizen exists."""
        pass

    @abstractmethod
    def check_boot_step_exists(self, step_name: str) -> bool:
        """Check if a boot step exists."""
        pass

    @abstractmethod
    def check_prd_moc_exists(self, prd_moc_path: str) -> bool:
        """Check if a PRD MOC file exists."""
        pass

    @abstractmethod
    def check_adr_exists(self, adr_id: str) -> bool:
        """Check if an ADR exists."""
        pass

    @abstractmethod
    def check_ontology_file_exists(self, ontology_path: str) -> bool:
        """Check if an ontology YAML file exists."""
        pass
