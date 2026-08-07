"""
Value Object: Reference

Represents a canonical reference in a PRD MOC document.
Format: [Type]:[Chemin]
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Reference:
    """Canonical reference in a PRD MOC."""
    type: str  # design, concept, skill, citizen, boot, prd-moc, adr, ontology
    path: str  # chemin ou identifiant

    # Types autorises
    ALLOWED_TYPES = {
        "design",
        "concept",
        "skill",
        "citizen",
        "boot",
        "prd-moc",
        "adr",
        "ontology",
    }

    def __post_init__(self):
        if self.type not in self.ALLOWED_TYPES:
            raise ValueError(
                f"Type de reference invalide: {self.type}. "
                f"Types autorises: {self.ALLOWED_TYPES}"
            )

    def __str__(self) -> str:
        return f"{self.type}:{self.path}"

    @classmethod
    def from_string(cls, ref_string: str) -> "Reference":
        """Parse a reference string like 'design:unified-design/designs/foo.yaml'."""
        if ":" not in ref_string:
            raise ValueError(f"Reference invalide (pas de ':'): {ref_string}")
        type_part, path_part = ref_string.split(":", 1)
        return cls(type=type_part.strip(), path=path_part.strip())
