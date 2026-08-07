"""Skill — yaml-debug-forensic

Diagnostique les erreurs YAML courantes sans modifier le fichier.
Génère un rapport de corruption.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

from ruamel.yaml import YAML

logger = logging.getLogger(__name__)


@dataclass
class YAMLCorruptionReport:
    path: Path
    parse_ok: bool = True
    parse_error: str = ""
    duplicate_keys: list[str] = field(default_factory=list)
    broken_quotes: list[str] = field(default_factory=list)
    invalid_anchors: list[str] = field(default_factory=list)
    issues: list[str] = field(default_factory=list)

    @property
    def is_clean(self) -> bool:
        return (
            self.parse_ok
            and not self.duplicate_keys
            and not self.broken_quotes
            and not self.invalid_anchors
            and not self.issues
        )


class YAMLDebugForensic:
    def __init__(self, yaml_path: Path) -> None:
        self.yaml_path = yaml_path
        self.report = YAMLCorruptionReport(path=yaml_path)

    def diagnose(self) -> YAMLCorruptionReport:
        """Analyse le fichier YAML et retourne un rapport de corruption."""
        text = self._read_text()
        if text:
            self._check_parse(text)
            self._check_duplicate_keys(text)
            self._check_broken_quotes(text)
            self._check_invalid_anchors(text)
        return self.report

    def _read_text(self) -> str:
        if not self.yaml_path.exists():
            self.report.parse_ok = False
            self.report.parse_error = f"Fichier introuvable: {self.yaml_path}"
            self.report.issues.append(self.report.parse_error)
            return ""
        return self.yaml_path.read_text(encoding="utf-8")

    def _check_parse(self, text: str) -> None:
        yaml = YAML()
        yaml.preserve_quotes = True
        yaml.width = 4096
        try:
            yaml.load(text)
        except Exception as exc:
            self.report.parse_ok = False
            self.report.parse_error = str(exc)
            self.report.issues.append(f"Parse error: {exc}")

    def _check_duplicate_keys(self, text: str) -> None:
        seen: dict[str, int] = {}
        for line_no, line in enumerate(text.splitlines(), start=1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if ":" in stripped:
                key = stripped.split(":", 1)[0].strip()
                if key in seen:
                    self.report.duplicate_keys.append(key)
                    self.report.issues.append(f"Clé dupliquée '{key}' ligne {line_no}")
                else:
                    seen[key] = line_no

    def _check_broken_quotes(self, text: str) -> None:
        for line_no, line in enumerate(text.splitlines(), start=1):
            if line.count('"') % 2 != 0:
                self.report.broken_quotes.append(line.strip())
                self.report.issues.append(f"Quote cassée ligne {line_no}: {line.strip()}")

    def _check_invalid_anchors(self, text: str) -> None:
        import re
        anchors = re.findall(r"&([A-Za-z0-9_]+)", text)
        aliases = re.findall(r"\*([A-Za-z0-9_]+)", text)
        anchor_set = set(anchors)
        for alias in aliases:
            if alias not in anchor_set:
                self.report.invalid_anchors.append(alias)
                self.report.issues.append(f"Ancre invalide '{alias}' (alias sans définition)")
