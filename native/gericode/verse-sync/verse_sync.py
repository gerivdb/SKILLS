"""
Verse Sync
Synchronise VERSES/verses/ ↔ ONTOLOGY/glossary.yaml ↔ TQL.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Literal

import yaml

logger = logging.getLogger(__name__)


class VerseSyncError(Exception):
    """Erreur de synchronisation des verses."""


class VerseSync:
    def __init__(
        self,
        verses_dir: Path,
        ontology_path: Path,
        tql_path: Path | None = None,
    ) -> None:
        self.verses_dir = verses_dir
        self.ontology_path = ontology_path
        self.tql_path = tql_path

    def sync(self, dry_run: bool = False) -> dict:
        """Synchronise les verses avec l'ontologie."""
        report: dict = {
            "dry_run": dry_run,
            "verses_synced": 0,
            "ontology_synced": 0,
            "errors": [],
            "warnings": [],
        }

        try:
            verses = self._load_verses()
            ontology = self._load_ontology()

            # Sync: concepts in ontology → verses
            missing_verses = self._find_missing_verses(ontology, verses)
            report["missing_verses"] = missing_verses

            # Sync: verses in VERSES → ontology
            missing_concepts = self._find_missing_concepts(verses, ontology)
            report["missing_concepts"] = missing_concepts

            report["status"] = "OK"
        except Exception as exc:
            report["errors"].append(str(exc))
            report["status"] = "FAILED"

        return report

    def _load_verses(self) -> dict[str, dict]:
        """Charge tous les verses."""
        verses = {}
        if not self.verses_dir.exists():
            return verses
        for verse_file in self.verses_dir.glob("*.md"):
            try:
                content = verse_file.read_text(encoding="utf-8")
                verses[verse_file.stem] = {"path": verse_file, "content": content}
            except Exception:
                pass
        return verses

    def _load_ontology(self) -> dict:
        """Charge l'ontologie."""
        try:
            return yaml.safe_load(self.ontology_path.read_text(encoding="utf-8")) or {}
        except Exception:
            return {}

    def _find_missing_verses(self, ontology: dict, verses: dict[str, dict]) -> list[str]:
        """Trouve les concepts ontologiques sans verse."""
        concepts = set()
        for term in ontology.get("terms", []):
            if isinstance(term, dict) and "name" in term:
                concepts.add(term["name"].lower())

        verse_names = {k.lower().replace("-verse", "") for k in verses.keys()}
        return sorted(concepts - verse_names)

    def _find_missing_concepts(self, verses: dict[str, dict], ontology: dict) -> list[str]:
        """Trouve les verses sans concept ontologique."""
        concepts = set()
        for term in ontology.get("terms", []):
            if isinstance(term, dict) and "name" in term:
                concepts.add(term["name"].lower())

        verse_names = {k.lower().replace("-verse", "") for k in verses.keys()}
        return sorted(verse_names - concepts)
