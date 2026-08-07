"""
CLI Adapter for Meta Coherence Validator.

Provides command-line interface for running meta coherence validation.
"""

import argparse
import sys
from pathlib import Path
from typing import List
from application.services.meta_coherence_service import MetaCoherenceService
from infrastructure.adapters.out.filesystem_adapter import (
    FilesystemPrdMocReader,
    FilesystemReferenceChecker,
)


def create_parser() -> argparse.ArgumentParser:
    """Create the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="meta-coherence-validator",
        description="Valide la meta-coherence entre PRD MOC documents.",
    )
    parser.add_argument(
        "paths",
        nargs="+",
        type=Path,
        help="Chemins vers les PRD MOC a valider",
    )
    parser.add_argument(
        "--designs",
        type=Path,
        default=Path("D:/DO/WEB/TOOLS/L0-CANON/unified-design/designs"),
        help="Chemin vers unified-design/designs/",
    )
    parser.add_argument(
        "--ontology",
        type=Path,
        default=Path("D:/DO/WEB/TOOLS/L0-CANON/ONTOLOGY"),
        help="Chemin vers ONTOLOGY/",
    )
    parser.add_argument(
        "--skills-registry",
        type=Path,
        default=Path("D:/DO/WEB/TOOLS/L4-TOOLS/SKILLS/REGISTRY.yaml"),
        help="Chemin vers SKILLS/REGISTRY.yaml",
    )
    parser.add_argument(
        "--boot-sequence",
        type=Path,
        default=Path(".kilo/workflows/session-boot-sequence.md"),
        help="Chemin vers session-boot-sequence.md",
    )
    parser.add_argument(
        "--base-path",
        type=Path,
        default=Path("D:/DO/WEB/TOOLS/L2-PLATFORM/GeriCode"),
        help="Chemin de base du repo GeriCode",
    )
    return parser


def main(argv: List[str] = None) -> int:
    """Main entry point for CLI."""
    parser = create_parser()
    args = parser.parse_args(argv)

    # Create adapter instances
    prd_moc_reader = FilesystemPrdMocReader(args.base_path)
    reference_checker = FilesystemReferenceChecker(
        unified_design_path=args.designs,
        ontology_path=args.ontology,
        skills_base_path=args.skills_registry.parent if args.skills_registry else Path("D:/DO/WEB/TOOLS/L4-TOOLS/SKILLS"),
        boot_sequence_path=args.boot_sequence,
        governance_hub_path=Path("D:/DO/WEB/TOOLS/L0-CANON/GOVERNANCE-HUB"),
    )

    # Create service
    service = MetaCoherenceService(
        prd_moc_reader=prd_moc_reader,
        reference_checker=reference_checker,
        base_path=args.base_path,
    )

    # Run validation
    report = service.validate(
        prd_moc_paths=args.paths,
        unified_design_path=args.designs,
        ontology_path=args.ontology,
        skills_registry=args.skills_registry,
        boot_sequence_path=args.boot_sequence,
    )

    # Output report
    print(f"Score global: {report['global_score']}")
    print(f"PRD MOC valides: {report['prd_mocs_validated']}")
    print(f"Contradictions: {report['contradictions_detected']}")
    print(f"References manquantes: {report['missing_references']}")

    if report["blocked"]:
        print("BLOCKED: Score < 0.8")
        return 1

    print("PASS: Score >= 0.8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
