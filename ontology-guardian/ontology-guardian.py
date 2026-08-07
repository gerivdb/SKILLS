#!/usr/bin/env python3
"""ontology-guardian.py — Active blocker for undeclared ontological terms.

Scans governing documents (PRD, INTENT, EPIC, ADR, README) and validates
that all stable identifiers (slugs, terms) are declared in ONTOLOGY/ONTOLOGY.yaml.

Usage:
    python ontology-guardian.py --check <document.md>
    python ontology-guardian.py --scan-dir <directory>
    python ontology-guardian.py --validate-term <term>
"""

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

REPO_ROOT = Path.cwd()
ONTOLOGY_FILE = Path(r"D:\DO\WEB\ONTOLOGY\ONTOLOGY.yaml")
GOVERNING_EXTENSIONS = {".md", ".yaml", ".yml"}


def load_ontology() -> Set[str]:
    """Load declared terms and entity names from ONTOLOGY/ONTOLOGY.yaml."""
    if not ONTOLOGY_FILE.exists():
        print(f"[ERROR] ONTOLOGY file not found: {ONTOLOGY_FILE}")
        return set()
    
    try:
        content = ONTOLOGY_FILE.read_text(encoding="utf-8", errors="replace")
        # Extract declared terms from entities.terms section
        terms = set()
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
                            terms.add(term)
        
        # Also extract entity names from entities section (e.g., NEXUS, ONTOLOGY, KIVA)
        for line in content.splitlines():
            stripped = line.strip()
            if stripped and ":" in stripped and not stripped.startswith("#"):
                # Entity entries are at 2-space indent under entities
                if line.startswith("  ") and not line.startswith("    ") and not stripped.startswith("terms") and not stripped.startswith("#"):
                    entity_name = stripped.split(":")[0].strip()
                    if entity_name and entity_name.isupper():
                        terms.add(entity_name)
        
        return terms
    except Exception as e:
        print(f"[ERROR] Cannot parse ONTOLOGY: {e}")
        return set()


def extract_terms_from_document(document_path: Path) -> Set[str]:
    """Extract potential ontological terms from a governing document.
    
    Only extracts terms that could be confused across contexts:
    - N* repo/concept identifiers (N243, N423, etc.)
    """
    terms = set()
    try:
        content = document_path.read_text(encoding="utf-8", errors="replace")
        
        # Pattern: N* pattern (N243, N423, etc.) - standalone
        pattern = re.findall(r'\bN\d+\b', content)
        terms.update(pattern)
        
    except Exception as e:
        print(f"[WARN] Cannot read {document_path}: {e}")
    
    return terms


def check_document(document_path: Path) -> Dict[str, Any]:
    """Check a single document for undeclared terms."""
    declared = load_ontology()
    doc_terms = extract_terms_from_document(document_path)
    
    undeclared = doc_terms - declared
    valid = len(undeclared) == 0
    
    return {
        "document": str(document_path),
        "valid": valid,
        "declared_terms_count": len(declared),
        "document_terms_count": len(doc_terms),
        "undeclared_terms": sorted(undeclared),
        "valid_terms": sorted(doc_terms - undeclared),
    }


def scan_directory(directory: Path) -> List[Dict[str, Any]]:
    """Scan all governing documents in a directory."""
    results = []
    if not directory.exists():
        return results
    
    for path in sorted(directory.rglob("*")):
        if path.is_file() and path.suffix in GOVERNING_EXTENSIONS:
            # Skip node_modules, .git, etc.
            if any(part in path.parts for part in [".git", "node_modules", "__pycache__", ".pytest_cache"]):
                continue
            result = check_document(path)
            if not result["valid"]:
                results.append(result)
    
    return results


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Ontology Guardian — validate ontological terms")
    parser.add_argument("--check", type=str, help="Check a single document")
    parser.add_argument("--scan-dir", type=str, help="Scan all governing documents in directory")
    parser.add_argument("--validate-term", type=str, help="Validate a single term against ONTOLOGY")
    args = parser.parse_args()
    
    if args.validate_term:
        declared = load_ontology()
        if args.validate_term in declared:
            print(f"[OK] Term '{args.validate_term}' is declared in ONTOLOGY")
            return 0
        else:
            print(f"[FAIL] Term '{args.validate_term}' is NOT declared in ONTOLOGY")
            return 1
    
    if args.check:
        path = Path(args.check)
        if not path.exists():
            print(f"[ERROR] Document not found: {path}")
            return 1
        result = check_document(path)
        print(f"[ONTOLOGY-GUARDIAN] Checking: {result['document']}")
        print(f"  Declared terms in ONTOLOGY: {result['declared_terms_count']}")
        print(f"  Terms in document: {result['document_terms_count']}")
        if result["valid"]:
            print(f"  [OK] All terms are declared")
            return 0
        else:
            print(f"  [FAIL] Undeclared terms: {', '.join(result['undeclared_terms'])}")
            return 1
    
    if args.scan_dir:
        directory = Path(args.scan_dir)
        results = scan_directory(directory)
        if not results:
            print(f"[ONTOLOGY-GUARDIAN] All documents in {directory} are valid")
            return 0
        else:
            print(f"[ONTOLOGY-GUARDIAN] Found {len(results)} documents with undeclared terms:")
            for result in results:
                print(f"  [FAIL] {result['document']}")
                print(f"    Undeclared: {', '.join(result['undeclared_terms'])}")
            return 1
    
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
