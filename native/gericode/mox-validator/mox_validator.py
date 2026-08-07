"""Validates governance documents against MOX probes."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Sequence


@dataclass
class ValidationResult:
    result: str
    failures: List[str] | None = None


class MoxValidator:
    REQUIRED_SECTIONS: Sequence[str] = (
        "Contexte",
        "Décision",
        "Conséquences",
        "Alternatives",
        "Statut",
    )

    def __init__(
        self,
        ontology_path: Path,
        repo_standards_dir: Path,
        output_dir: Path,
    ) -> None:
        self.ontology_path = ontology_path
        self.repo_standards_dir = repo_standards_dir
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def validate(self, document: dict, layers: List[str] | None = None) -> ValidationResult:
        content = document.get("content", "")
        layers = layers or ["frontmatter", "structure", "contradiction"]

        failures: List[str] = []

        if "frontmatter" in layers:
            if not content.startswith("---"):
                failures.append("missing_frontmatter")
            else:
                frontmatter = content.split("---", 2)[1]
                for key in ("type", "version", "status", "date", "intent_hash"):
                    if key not in frontmatter:
                        failures.append(f"missing_{key}")

        if "structure" in layers:
            for section in self.REQUIRED_SECTIONS:
                if f"## {section}" not in content:
                    failures.append(f"missing_section_{section}")

        if "contradiction" in layers:
            if "contradiction" in content.lower():
                failures.append("contradiction_detected")

        return ValidationResult(result="FAIL" if failures else "PASS", failures=failures or None)
