"""
mox_validator — MOX document validation engine.

Processes:
  - classify_document
  - convert_prd_to_moc
  - validate_delivery_plan
  - validate_milestones
  - validate_tests
  - validate_dependencies
  - validate_risks
  - validate_frontmatter_schema
  - detect_cross_repo_contradictions
  - detect_gaps
  - detect_duplicates
  - validate_probes
  - log_wal
"""

from __future__ import annotations

import json
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Paths
REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
ONTOLOGY_FILE = REPO_ROOT / "D:/DO/WEB/ONTOLOGY/ONTOLOGY.yaml"
REPO_STANDARDS = REPO_ROOT / "D:/DO/WEB/TOOLS/L0-CANON/REPO-STANDARDS"
UNIFIED_DESIGN = REPO_ROOT / "D:/DO/WEB/TOOLS/L0-CANON/unified-design"
GOVERNANCE_HUB = REPO_ROOT / "D:/DO/WEB/TOOLS/L0-CANON/GOVERNANCE-HUB"
TOPOS = REPO_ROOT / "D:/DO/WEB/TOOLS/L1-INFRA/TOPOS"
NEXUS = REPO_ROOT / "D:/DO/WEB/TOOLS/L0-CANON/GOVERNANCE-HUB"


@dataclass
class ValidationIssue:
    severity: str  # ERROR, WARN, INFO
    process: str
    message: str
    location: str = ""
    fix: str = ""


@dataclass
class ValidationResult:
    valid: bool
    issues: List[ValidationIssue] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_issue(self, severity: str, process: str, message: str, location: str = "", fix: str = ""):
        self.issues.append(ValidationIssue(severity, process, message, location, fix))
        if severity == "ERROR":
            self.valid = False

    def summary(self) -> str:
        lines = [f"[MOX] valid={self.valid}"]
        for issue in self.issues:
            lines.append(f"  [{issue.severity}] {issue.process}: {issue.message}")
        return "\n".join(lines)


class MOXValidator:
    """MOX — Gardien de cohérence cross-repo."""

    def __init__(self):
        self.ontology_terms: set[str] = set()
        self._load_ontology()

    def _load_ontology(self):
        """Load declared terms from ONTOLOGY.yaml."""
        if not ONTOLOGY_FILE.exists():
            return
        content = ONTOLOGY_FILE.read_text(encoding="utf-8", errors="replace")
        in_terms = False
        base_indent = None
        for line in content.splitlines():
            stripped = line.strip()
            if stripped == "terms:":
                in_terms = True
                base_indent = len(line) - len(line.lstrip())
                continue
            if in_terms and base_indent is not None:
                current_indent = len(line) - len(line.lstrip())
                if stripped and current_indent <= base_indent:
                    in_terms = False
                    continue
                if ":" in stripped and not stripped.startswith("#"):
                    if current_indent == base_indent + 2:
                        term = stripped.split(":")[0].strip()
                        if term:
                            self.ontology_terms.add(term)
        # Also load entity names
        for line in content.splitlines():
            stripped = line.strip()
            if stripped and ":" in stripped and not stripped.startswith("#"):
                if line.startswith("  ") and not line.startswith("    ") and not stripped.startswith("terms") and not stripped.startswith("#"):
                    entity_name = stripped.split(":")[0].strip()
                    if entity_name and entity_name.isupper():
                        self.ontology_terms.add(entity_name)

    # ------------------------------------------------------------------
    # PROCESS 1: classify-document
    # ------------------------------------------------------------------
    def classify_document(self, document_path: Path) -> Dict[str, Any]:
        """Classify a document by type."""
        content = document_path.read_text(encoding="utf-8", errors="replace")
        frontmatter = self._extract_frontmatter(content)
        doc_type = frontmatter.get("type", "UNKNOWN")
        
        # Validate classification
        valid_types = ["PRD", "PRD_MOC", "ADR", "EPIC", "INTENT", "SPEC", "REPORT", "RPT", "GUI", "RUN", "INDEX"]
        classification = {
            "path": str(document_path),
            "type": doc_type,
            "valid": doc_type in valid_types,
            "sections_present": self._detect_sections(content),
            "frontmatter_complete": self._check_frontmatter_complete(frontmatter),
        }
        return classification

    def _detect_sections(self, content: str) -> List[str]:
        """Detect sections in document body."""
        sections = []
        for line in content.splitlines():
            if line.startswith("## "):
                section = line[3:].strip().lower().replace(" ", "_")
                # Strip leading numbering like "1. ", "2. ", etc.
                section = re.sub(r'^\d+\.\s*', '', section)
                # Normalize accents
                section = self._normalize_accents(section)
                sections.append(section)
        return sections

    @staticmethod
    def _normalize_accents(text: str) -> str:
        """Normalize accented characters to ASCII equivalents."""
        accents = {
            'à': 'a', 'á': 'a', 'â': 'a', 'ã': 'a', 'ä': 'a',
            'è': 'e', 'é': 'e', 'ê': 'e', 'ë': 'e',
            'ì': 'i', 'í': 'i', 'î': 'i', 'ï': 'i',
            'ò': 'o', 'ó': 'o', 'ô': 'o', 'õ': 'o', 'ö': 'o',
            'ù': 'u', 'ú': 'u', 'û': 'u', 'ü': 'u',
            'ý': 'y', 'ÿ': 'y',
            'ç': 'c',
            'ñ': 'n',
            'œ': 'oe', 'æ': 'ae',
        }
        result = []
        for char in text:
            result.append(accents.get(char, char))
        return ''.join(result)

    @staticmethod
    def _normalize_section_name(name: str) -> str:
        """Normalize section name for comparison: lowercase, strip accents, remove stop words, remove extra underscores."""
        # Lowercase and normalize accents
        name = name.lower()
        name = MOXValidator._normalize_accents(name)
        # Remove common French stop words
        stop_words = {'de', 'du', 'des', 'le', 'la', 'les', 'un', 'une', 'et', 'au', 'aux', 'par', 'pour', 'vers', 'avec', 'sans', 'sous', 'sur', 'dans', 'entre', 'contre', 'avant', 'apres', 'depuis', 'pendant', 'jusqua', 'chez'}
        words = name.split('_')
        words = [w for w in words if w not in stop_words]
        return '_'.join(words)

    def _check_frontmatter_complete(self, frontmatter: Dict[str, Any]) -> bool:
        """Check if all required frontmatter fields are present."""
        required = ["type", "version", "status", "date", "intent_hash", "citizen", "layer", "author", "source_repo", "source_path"]
        return all(field in frontmatter for field in required)

    # ------------------------------------------------------------------
    # PROCESS 2: convert-prd-to-moc
    # ------------------------------------------------------------------
    def convert_prd_to_moc(self, document_path: Path, output_path: Optional[Path] = None) -> Tuple[bool, str]:
        """Convert a PRD to PRD_MOC format."""
        content = document_path.read_text(encoding="utf-8", errors="replace")
        frontmatter_match = re.search(r'\A---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not frontmatter_match:
            return False, "No frontmatter found"
        
        # Update type
        new_content = content.replace('type: PRD', 'type: PRD_MOC')
        
        # Add operational sections if missing
        operational_sections = {
            "plan_livraison": "## Plan de livraison\n\n### Phase 1 — Fondations\n\n| Tâche | Livrable | Tests |\n|-------|----------|-------|\n| <Tâche> | <Livrable> | <Tests> |\n\n### Phase 2 — Skills & Citizens\n\n| Tâche | Livrable | Tests |\n|-------|----------|-------|\n| <Tâche> | <Livrable> | <Tests> |\n\n",
            "milestones": "## Milestones\n\n| Milestone | Date | Livrable | Validation |\n|-----------|------|----------|-------------|\n| M1 | Semaine 2 | Atoms + Schemas | MOX valide |\n| M2 | Semaine 4 | Skills + Citizens | Tests unitaires passent |\n| M3 | Semaine 6 | Workflows | Tests intégration passent |\n| M4 | Semaine 8 | N243 opérationnel | Critères d'acceptation atteints |\n\n",
            "tests": "## Tests par composant\n\n| Test | Description | Attend |\n|------|-------------|--------|\n| <test_name> | <description> | <attend> |\n\n",
            "dependances": "## Matrice de dépendances\n\n| Composant | Dépend de | Bloquant pour |\n|-----------|-----------|---------------|\n| <composant> | <dépendances> | <bloquants> |\n\n",
            "risques": "## Registre de risques\n\n| Risque | Impact | Probabilité | Mitigation |\n|--------|--------|-------------|------------|\n| <risque> | <impact> | <probabilité> | <mitigation> |\n\n",
        }
        
        for section_name, section_content in operational_sections.items():
            if f"## {section_name.replace('_', ' ').title()}" not in new_content and f"## {section_name}" not in new_content:
                # Insert before Rollback section
                rollback_match = re.search(r'\n## Rollback\n', new_content)
                if rollback_match:
                    new_content = new_content[:rollback_match.start()] + f"\n{section_content}\n" + new_content[rollback_match.start():]
                else:
                    new_content += f"\n{section_content}\n"
        
        if output_path:
            output_path.write_text(new_content, encoding="utf-8")
            return True, str(output_path)
        return True, "Conversion successful"

    # ------------------------------------------------------------------
    # PROCESS 3: validate-delivery-plan
    # ------------------------------------------------------------------
    def validate_delivery_plan(self, document_path: Path) -> ValidationResult:
        """Validate delivery plan section."""
        result = ValidationResult(valid=True)
        content = document_path.read_text(encoding="utf-8", errors="replace")
        
        # Check for plan_livraison section
        if "## Plan de livraison" not in content and "## plan_livraison" not in content.lower():
            result.add_issue("ERROR", "validate-delivery-plan", "Missing 'Plan de livraison' section", fix="Add plan_livraison section with phases")
        
        # Check for phases
        phases = re.findall(r'### Phase \d+', content)
        if not phases:
            result.add_issue("ERROR", "validate-delivery-plan", "No phases defined in delivery plan", fix="Add at least 2 phases")
        
        # Check for tasks
        tasks = re.findall(r'\| [^|]+ \| [^|]+ \| [^|]+ \|', content)
        if len(tasks) < 2:
            result.add_issue("WARN", "validate-delivery-plan", "Less than 2 tasks defined", fix="Add more tasks to delivery plan")
        
        return result

    # ------------------------------------------------------------------
    # PROCESS 4: validate-milestones
    # ------------------------------------------------------------------
    def validate_milestones(self, document_path: Path) -> ValidationResult:
        """Validate milestones section."""
        result = ValidationResult(valid=True)
        content = document_path.read_text(encoding="utf-8", errors="replace")
        
        if "## Milestones" not in content:
            result.add_issue("ERROR", "validate-milestones", "Missing 'Milestones' section", fix="Add milestones section")
            return result
        
        # Check for at least one milestone
        milestones = re.findall(r'\| M\d+ \|', content)
        if not milestones:
            result.add_issue("ERROR", "validate-milestones", "No milestones defined", fix="Add at least one milestone")
        
        # Check for dates
        dates = re.findall(r'\| Semaine \d+ \|', content)
        if not dates:
            result.add_issue("WARN", "validate-milestones", "No dates defined for milestones", fix="Add dates to milestones")
        
        return result

    # ------------------------------------------------------------------
    # PROCESS 5: validate-tests
    # ------------------------------------------------------------------
    def validate_tests(self, document_path: Path) -> ValidationResult:
        """Validate tests section."""
        result = ValidationResult(valid=True)
        content = document_path.read_text(encoding="utf-8", errors="replace")
        
        if "## Tests par composant" not in content and "## Tests" not in content:
            result.add_issue("ERROR", "validate-tests", "Missing 'Tests par composant' section", fix="Add tests section")
            return result
        
        # Check for test table
        test_rows = re.findall(r'\| test_\w+ \|', content)
        if not test_rows:
            result.add_issue("WARN", "validate-tests", "No test cases defined", fix="Add test cases")
        
        return result

    # ------------------------------------------------------------------
    # PROCESS 6: validate-dependencies
    # ------------------------------------------------------------------
    def validate_dependencies(self, document_path: Path) -> ValidationResult:
        """Validate dependencies matrix."""
        result = ValidationResult(valid=True)
        content = document_path.read_text(encoding="utf-8", errors="replace")
        
        if "## Matrice de dépendances" not in content and "## dependances" not in content.lower():
            result.add_issue("ERROR", "validate-dependencies", "Missing 'Matrice de dépendances' section", fix="Add dependencies matrix")
            return result
        
        return result

    # ------------------------------------------------------------------
    # PROCESS 7: validate-risks
    # ------------------------------------------------------------------
    def validate_risks(self, document_path: Path) -> ValidationResult:
        """Validate risk register."""
        result = ValidationResult(valid=True)
        content = document_path.read_text(encoding="utf-8", errors="replace")
        
        if "## Registre de risques" not in content and "## risques" not in content.lower():
            result.add_issue("ERROR", "validate-risks", "Missing 'Registre de risques' section", fix="Add risk register")
            return result
        
        return result

    # ------------------------------------------------------------------
    # PROCESS 8: validate-frontmatter-schema
    # ------------------------------------------------------------------
    def validate_frontmatter_schema(self, document_path: Path) -> ValidationResult:
        """Validate frontmatter against schema."""
        result = ValidationResult(valid=True)
        content = document_path.read_text(encoding="utf-8", errors="replace")
        frontmatter = self._extract_frontmatter_dict(content)
        
        required_fields = {
            "PRD": ["type", "version", "status", "date", "intent_hash", "citizen", "layer", "author", "source_repo", "source_path"],
            "PRD_MOC": ["type", "version", "status", "date", "intent_hash", "citizen", "layer", "author", "source_repo", "source_path"],
            "ADR": ["type", "version", "status", "date", "intent_hash", "author", "source_repo", "source_path"],
            "EPIC": ["type", "version", "status", "date", "intent_hash", "author", "source_repo", "source_path"],
            "INTENT": ["type", "version", "status", "date", "intent_hash", "author", "source_repo", "source_path"],
        }
        
        doc_type = frontmatter.get("type", "UNKNOWN")
        required = required_fields.get(doc_type, required_fields.get("PRD", []))
        
        for field in required:
            if field not in frontmatter:
                result.add_issue("ERROR", "validate-frontmatter-schema", f"Missing required field: {field}", location="frontmatter", fix=f"Add {field} to frontmatter")
        
        # Validate intent_hash format
        if "intent_hash" in frontmatter:
            intent_hash = str(frontmatter["intent_hash"])
            if not re.match(r'^0x[A-Z0-9_]{8,}$', intent_hash):
                result.add_issue("ERROR", "validate-frontmatter-schema", f"Invalid intent_hash format: {intent_hash}", location="frontmatter", fix="Use format 0xHASH_YYYYMMDD")
        
        return result

    def _extract_frontmatter(self, content: str) -> Dict[str, Any]:
        """Extract frontmatter from document."""
        match = re.search(r'\A---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not match:
            return {}
        try:
            import yaml
            return yaml.safe_load(match.group(1)) or {}
        except Exception:
            return {}

    def _extract_frontmatter_dict(self, content: str) -> Dict[str, Any]:
        """Extract frontmatter as dict."""
        return self._extract_frontmatter(content)

    # ------------------------------------------------------------------
    # PROCESS 9: detect-cross-repo-contradictions
    # ------------------------------------------------------------------
    def detect_cross_repo_contradictions(self, document_path: Path) -> ValidationResult:
        """Detect contradictions between documents."""
        result = ValidationResult(valid=True)
        content = document_path.read_text(encoding="utf-8", errors="replace")
        
        # Simple contradiction detection: check for conflicting statements
        # This is a placeholder for actual cross-repo analysis
        contradictions = []
        
        if contradictions:
            for contradiction in contradictions:
                result.add_issue("ERROR", "detect-cross-repo-contradictions", contradiction["message"], location=contradiction.get("location", ""))
        
        return result

    # ------------------------------------------------------------------
    # PROCESS 10: detect-gaps
    # ------------------------------------------------------------------
    def detect_gaps(self, document_path: Path) -> ValidationResult:
        """Detect gaps in document."""
        result = ValidationResult(valid=True)
        content = document_path.read_text(encoding="utf-8", errors="replace")
        frontmatter = self._extract_frontmatter(content)
        
        # Check for missing sections based on doc type
        doc_type = frontmatter.get("type", "PRD")
        required_sections = {
            "PRD": ["objectif", "contexte", "perimetre", "architecture", "regles", "roles", "processus", "probes", "criteres", "rollback", "references"],
            "PRD_MOC": ["objectif", "contexte", "perimetre", "architecture", "regles", "roles", "processus", "probes", "criteres", "rollback", "references", "plan_livraison", "milestones", "tests", "dependances", "risques"],
            "ADR": ["contexte", "decision", "consequences", "alternatives"],
            "EPIC": ["objectif", "contexte", "perimetre", "stories", "acceptance_criteria"],
            "INTENT": ["objectif", "contexte", "perimetre", "execution_plan"],
        }
        
        sections = [self._normalize_section_name(s) for s in self._detect_sections(content)]
        required = required_sections.get(doc_type, required_sections["PRD"])
        
        for section in required:
            # Normalize required section name too
            normalized_required = self._normalize_section_name(section)
            found = any(normalized_required == detected or normalized_required in detected or detected in normalized_required for detected in sections)
            if not found:
                result.add_issue("WARN", "detect-gaps", f"Missing section: {section}", fix=f"Add {section} section")
        
        return result

    # ------------------------------------------------------------------
    # PROCESS 11: detect-duplicates
    # ------------------------------------------------------------------
    def detect_duplicates(self, document_path: Path) -> ValidationResult:
        """Detect duplicate information in document."""
        result = ValidationResult(valid=True)
        content = document_path.read_text(encoding="utf-8", errors="replace")
        
        # Simple duplicate detection: check for repeated phrases
        # This is a placeholder for actual duplicate detection
        lines = content.splitlines()
        seen = set()
        for i, line in enumerate(lines, 1):
            if len(line) > 50 and line in seen:
                result.add_issue("WARN", "detect-duplicates", f"Possible duplicate content at line {i}", location=str(document_path))
            seen.add(line)
        
        return result

    # ------------------------------------------------------------------
    # PROCESS 12: validate-probes
    # ------------------------------------------------------------------
    def validate_probes(self, document_path: Path) -> ValidationResult:
        """Validate probes P-101..P-109."""
        result = ValidationResult(valid=True)
        content = document_path.read_text(encoding="utf-8", errors="replace")
        
        # Check for probes table
        if "| PROBE" not in content and "| P-" not in content:
            result.add_issue("WARN", "validate-probes", "No probes table found", fix="Add probes table")
        
        # Check for mandatory probes
        mandatory_probes = ["P-106", "P-107"]
        for probe in mandatory_probes:
            if probe not in content:
                result.add_issue("ERROR", "validate-probes", f"Missing mandatory probe: {probe}", fix=f"Add probe {probe}")
        
        return result

    # ------------------------------------------------------------------
    # PROCESS 13: log-wal
    # ------------------------------------------------------------------
    def log_wal(self, event_type: str, document_path: Path, result: ValidationResult) -> str:
        """Log validation event to WAL."""
        timestamp = datetime.now().isoformat()
        wal_entry = {
            "timestamp": timestamp,
            "event_type": event_type,
            "document": str(document_path),
            "valid": result.valid,
            "issues_count": len(result.issues),
            "issues": [
                {
                    "severity": issue.severity,
                    "process": issue.process,
                    "message": issue.message,
                    "location": issue.location,
                }
                for issue in result.issues
            ],
        }
        return json.dumps(wal_entry, ensure_ascii=False)

    # ------------------------------------------------------------------
    # MAIN VALIDATION PIPELINE
    # ------------------------------------------------------------------
    def validate(self, document_path: Path, strict: bool = False) -> ValidationResult:
        """Run full MOX validation pipeline."""
        result = ValidationResult(valid=True)
        
        # Step 1: classify
        classification = self.classify_document(document_path)
        result.metadata["classification"] = classification
        if not classification["valid"]:
            result.add_issue("ERROR", "classify-document", f"Invalid document type: {classification['type']}", fix="Set valid type in frontmatter")
        
        # Step 2: frontmatter schema
        fm_result = self.validate_frontmatter_schema(document_path)
        result.issues.extend(fm_result.issues)
        if not fm_result.valid:
            result.valid = False
        
        # Step 3: gaps
        gaps_result = self.detect_gaps(document_path)
        result.issues.extend(gaps_result.issues)
        
        # Step 4: duplicates
        dup_result = self.detect_duplicates(document_path)
        result.issues.extend(dup_result.issues)
        
        # Step 5: probes
        probes_result = self.validate_probes(document_path)
        result.issues.extend(probes_result.issues)
        if not probes_result.valid:
            result.valid = False
        
        # Step 6: contradictions
        contradictions_result = self.detect_cross_repo_contradictions(document_path)
        result.issues.extend(contradictions_result.issues)
        if not contradictions_result.valid:
            result.valid = False
        
        # Step 7: PRD_MOC specific validations
        if classification["type"] == "PRD_MOC":
            plan_result = self.validate_delivery_plan(document_path)
            result.issues.extend(plan_result.issues)
            if not plan_result.valid:
                result.valid = False
            
            milestones_result = self.validate_milestones(document_path)
            result.issues.extend(milestones_result.issues)
            if not milestones_result.valid:
                result.valid = False
            
            tests_result = self.validate_tests(document_path)
            result.issues.extend(tests_result.issues)
            if not tests_result.valid:
                result.valid = False
            
            deps_result = self.validate_dependencies(document_path)
            result.issues.extend(deps_result.issues)
            if not deps_result.valid:
                result.valid = False
            
            risks_result = self.validate_risks(document_path)
            result.issues.extend(risks_result.issues)
            if not risks_result.valid:
                result.valid = False
        
        # Step 8: WAL
        wal_entry = self.log_wal("mox-validation", document_path, result)
        result.metadata["wal_entry"] = wal_entry
        
        return result


def main():
    import argparse
    parser = argparse.ArgumentParser(description="MOX Validator")
    parser.add_argument("document", type=str, help="Document to validate")
    parser.add_argument("--strict", action="store_true", help="Strict mode")
    parser.add_argument("--classify", action="store_true", help="Classify document only")
    parser.add_argument("--convert", action="store_true", help="Convert PRD to PRD_MOC")
    parser.add_argument("--output", type=str, help="Output path for conversion")
    args = parser.parse_args()
    
    document_path = Path(args.document)
    if not document_path.exists():
        print(f"[ERROR] Document not found: {document_path}")
        sys.exit(1)
    
    mox = MOXValidator()
    
    if args.classify:
        classification = mox.classify_document(document_path)
        print(json.dumps(classification, indent=2, ensure_ascii=False))
        sys.exit(0 if classification["valid"] else 1)
    
    if args.convert:
        success, message = mox.convert_prd_to_moc(document_path, Path(args.output) if args.output else None)
        print(f"[MOX] Conversion: {success} - {message}")
        sys.exit(0 if success else 1)
    
    result = mox.validate(document_path, strict=args.strict)
    print(result.summary())
    sys.exit(0 if result.valid else 1)


if __name__ == "__main__":
    main()
