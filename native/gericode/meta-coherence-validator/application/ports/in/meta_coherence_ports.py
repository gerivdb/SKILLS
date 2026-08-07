"""
Application Ports (inbound) for Meta Coherence Validator.

Defines the use case interface for validating PRD MOC coherence.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from pathlib import Path


class MetaCoherenceValidatorPort(ABC):
    """Inbound port for validating meta coherence."""

    @abstractmethod
    def validate(
        self,
        prd_moc_paths: List[Path],
        unified_design_path: Path,
        ontology_path: Path,
        skills_registry: Path,
        boot_sequence_path: Path,
    ) -> Dict:
        """Validate coherence across all PRD MOC documents."""
        pass
