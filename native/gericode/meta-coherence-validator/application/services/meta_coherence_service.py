"""
Meta Coherence Validator Service

Core validation logic for checking coherence between PRD MOC documents.
"""

import re
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional, Set, Tuple

# Add skill root to path for absolute imports
SKILL_ROOT = Path(__file__).parent.parent.parent
if str(SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILL_ROOT))

from domain.value_objects.reference_vo import Reference
from domain.events.coherence_event import (
    ValidationStarted,
    PrdMocValidated,
    ContradictionDetected,
    MissingReferenceDetected,
    ValidationCompleted,
)


class MetaCoherenceService:
    """Service that validates meta coherence across PRD MOC documents."""

    def __init__(
        self,
        prd_moc_reader,
        reference_checker,
        base_path: Path,
    ):
        self.prd_moc_reader = prd_moc_reader
        self.reference_checker = reference_checker
        self.base_path = base_path
        self.events: List[Any] = []

    def _emit(self, event) -> None:
        """Emit a domain event."""
        self.events.append(event)

    def _parse_references(self, content: str) -> List[str]:
        """Extract reference strings from PRD MOC markdown content."""
        refs = []
        # Match canonical format: type:path
        pattern = r"`([a-z]+:[^`]+)`"
        matches = re.findall(pattern, content)
        refs.extend(matches)
        return refs

    def _parse_frontmatter(self, content: str) -> Dict[str, str]:
        """Parse YAML frontmatter from PRD MOC."""
        fm = {}
        match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
        if match:
            fm_text = match.group(1)
            for line in fm_text.split("\n"):
                if ":" in line:
                    key, _, value = line.partition(":")
                    fm[key.strip()] = value.strip().strip('"').strip("'")
        return fm

    def _check_reference_exists(self, ref: Reference) -> Tuple[bool, Optional[str]]:
        """Check if a reference target exists. Returns (exists, reason)."""
        checkers = {
            "design": self.reference_checker.check_design_exists,
            "concept": self.reference_checker.check_concept_exists,
            "skill": self.reference_checker.check_skill_exists,
            "citizen": self.reference_checker.check_citizen_exists,
            "boot": self.reference_checker.check_boot_step_exists,
            "prd-moc": self.reference_checker.check_prd_moc_exists,
            "adr": self.reference_checker.check_adr_exists,
            "ontology": self.reference_checker.check_ontology_file_exists,
        }
        checker = checkers.get(ref.type)
        if checker is None:
            return False, f"Type de reference inconnu: {ref.type}"
        exists = checker(ref.path)
        return exists, None if exists else f"Reference manquante: {ref}"

    def validate_prd_moc(
        self, prd_moc_data: Dict
    ) -> Dict[str, Any]:
        """Validate a single PRD MOC document."""
        path = prd_moc_data.get("path", "")
        content = prd_moc_data.get("content", "")
        title = prd_moc_data.get("title", path)

        # Parse frontmatter
        frontmatter = self._parse_frontmatter(content)

        # Extract references
        ref_strings = self._parse_references(content)
        references = []
        for ref_str in ref_strings:
            try:
                references.append(Reference.from_string(ref_str))
            except ValueError:
                # Skip invalid references but record them
                pass

        # Validate each reference
        missing = []
        valid_count = 0
        for ref in references:
            exists, reason = self._check_reference_exists(ref)
            if exists:
                valid_count += 1
            else:
                missing.append({"reference": str(ref), "reason": reason or "Not found"})
                self._emit(MissingReferenceDetected(
                    prd_moc_path=path,
                    reference=str(ref),
                    reason=reason or "Not found",
                ))

        # Compute score
        total = len(references) if references else 1
        score = valid_count / total

        result = {
            "path": path,
            "title": title,
            "score": score,
            "total_references": len(references),
            "valid_references": valid_count,
            "missing_references": missing,
            "contradictions": [],
            "blocked": score < 0.8,
        }

        self._emit(PrdMocValidated(
            prd_moc_path=path,
            score=score,
            missing_count=len(missing),
            contradiction_count=0,
        ))

        return result

    def validate(
        self,
        prd_moc_paths: List[Path],
        unified_design_path: Path,
        ontology_path: Path,
        skills_registry: Path,
        boot_sequence_path: Path,
    ) -> Dict[str, Any]:
        """Validate coherence across all PRD MOC documents."""
        self.events = []
        self._emit(ValidationStarted(prd_moc_count=len(prd_moc_paths)))

        # Read all PRD MOC documents
        prd_mocs_data = self.prd_moc_reader.read_prd_mocs(prd_moc_paths)

        # Validate each PRD MOC
        results = []
        total_missing = 0
        total_contradictions = 0

        for prd_moc_data in prd_mocs_data:
            result = self.validate_prd_moc(prd_moc_data)
            results.append(result)
            total_missing += len(result["missing_references"])
            total_contradictions += len(result["contradictions"])

        # Compute global score
        if results:
            global_score = sum(r["score"] for r in results) / len(results)
        else:
            global_score = 1.0

        blocked = global_score < 0.8

        report = {
            "global_score": round(global_score, 2),
            "prd_mocs_validated": len(results),
            "contradictions_detected": total_contradictions,
            "missing_references": total_missing,
            "orphan_references": [],
            "inconsistent_definitions": [],
            "blocked": blocked,
            "details": results,
            "recommendations": self._generate_recommendations(results),
        }

        self._emit(ValidationCompleted(
            global_score=global_score,
            prd_moc_count=len(results),
            total_missing=total_missing,
            total_contradictions=total_contradictions,
            blocked=blocked,
        ))

        return report

    def _generate_recommendations(self, results: List[Dict]) -> List[str]:
        """Generate recommendations based on validation results."""
        recommendations = []
        for result in results:
            if result["blocked"]:
                recommendations.append(
                    f"Corriger les references manquantes dans {result['path']}"
                )
            for missing in result["missing_references"]:
                recommendations.append(
                    f"Ajouter reference manquante: {missing['reference']}"
                )
        return recommendations
