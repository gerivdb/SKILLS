"""Tests pour verse-sync."""

from __future__ import annotations

from pathlib import Path
import pytest

from verse_sync import VerseSync, VerseSyncError


def test_sync_missing_verse(tmp_path):
    verses = tmp_path / "verses"
    verses.mkdir()
    ontology = tmp_path / "glossary.yaml"
    ontology.write_text(
        "terms:\n"
        "  - name: existing-concept\n"
        "    definition: An existing concept\n",
        encoding="utf-8",
    )
    sync = VerseSync(verses_dir=verses, ontology_path=ontology)
    report = sync.sync(dry_run=True)
    assert "missing_verses" in report


def test_sync_complete(tmp_path):
    verses = tmp_path / "verses"
    verses.mkdir()
    (verses / "existing-concept.md").write_text("---\nconcept: existing-concept\n---\n", encoding="utf-8")
    ontology = tmp_path / "glossary.yaml"
    ontology.write_text(
        "terms:\n"
        "  - name: existing-concept\n"
        "    definition: An existing concept\n",
        encoding="utf-8",
    )
    sync = VerseSync(verses_dir=verses, ontology_path=ontology)
    report = sync.sync(dry_run=True)
    assert report["missing_verses"] == []
