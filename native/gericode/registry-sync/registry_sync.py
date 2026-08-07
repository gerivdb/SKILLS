"""
Registry Sync Engine
Synchronise REGISTRY.yaml ↔ registry.json ↔ citizens.yaml.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Literal

import yaml

logger = logging.getLogger(__name__)


class RegistrySyncError(Exception):
    """Erreur lors de la synchronisation des registres."""


class RegistrySyncEngine:
    def __init__(
        self,
        registry_yaml: Path,
        registry_json: Path,
        citizens_yaml: Path,
    ) -> None:
        self.registry_yaml = registry_yaml
        self.registry_json = registry_json
        self.citizens_yaml = citizens_yaml

    def sync(self, dry_run: bool = False) -> dict:
        """Synchronise tous les registres."""
        report: dict = {
            "registry_yaml_loaded": False,
            "registry_json_updated": False,
            "citizens_yaml_updated": False,
            "errors": [],
        }

        # Load REGISTRY.yaml
        try:
            yaml_data = yaml.safe_load(self.registry_yaml.read_text(encoding="utf-8")) or {}
            report["registry_yaml_loaded"] = True
            report["total_skills"] = len(yaml_data.get("skills", []))
        except Exception as exc:
            report["errors"].append(f"REGISTRY.yaml load failed: {exc}")
            return report

        # Sync registry.json
        json_errors = self._sync_json(yaml_data, dry_run=dry_run)
        report["registry_json_errors"] = json_errors
        report["registry_json_updated"] = len(json_errors) == 0

        # Sync citizens.yaml
        citizen_errors = self._sync_citizens(yaml_data, dry_run=dry_run)
        report["citizens_yaml_errors"] = citizen_errors
        report["citizens_yaml_updated"] = len(citizen_errors) == 0

        return report

    def _sync_json(self, yaml_data: dict, dry_run: bool = False) -> list[str]:
        """Regénère registry.json depuis REGISTRY.yaml."""
        errors: list[str] = []
        skills = yaml_data.get("skills", [])

        json_skills = []
        for skill in skills:
            try:
                json_skills.append(
                    {
                        "name": skill.get("name", ""),
                        "version": skill.get("version", "1.0.0"),
                        "description": skill.get("description", ""),
                        "author": skill.get("author", "gerivdb"),
                        "repository": skill.get("source_repo", ""),
                        "dependencies": skill.get("consumes_from", []),
                        "capabilities": skill.get("triggers", []),
                        "repos_served": [skill.get("source_repo", "")] if skill.get("source_repo") else [],
                    }
                )
            except Exception as exc:
                errors.append(f"Skill {skill.get('name')} failed: {exc}")

        if not dry_run and not errors:
            payload = {"skills": json_skills}
            self.registry_json.write_text(
                json.dumps(payload, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
            logger.info("registry.json synced: %d skills", len(json_skills))

        return errors

    def _sync_citizens(self, yaml_data: dict, dry_run: bool = False) -> list[str]:
        """Enrichit citizens.yaml avec les repo citizens de REGISTRY.yaml."""
        errors: list[str] = []
        skills = yaml_data.get("skills", [])

        try:
            citizens_data = yaml.safe_load(self.citizens_yaml.read_text(encoding="utf-8")) or {}
        except Exception as exc:
            errors.append(f"citizens.yaml load failed: {exc}")
            return errors

        if "citizens" not in citizens_data or citizens_data["citizens"] is None:
            citizens_data["citizens"] = []

        existing_ids = {c.get("id") for c in citizens_data["citizens"]}
        added = 0
        for skill in skills:
            source_repo = skill.get("source_repo")
            if not source_repo:
                continue
            repo_name = source_repo.replace("gerivdb/", "")
            citizen_id = repo_name.upper()
            if citizen_id in existing_ids:
                continue
            citizens_data["citizens"].append(
                {
                    "id": citizen_id,
                    "intent_hash": f"0x{citizen_id}_CITIZEN_20260807",
                    "role": f"Repo citoyen {repo_name}",
                    "responsibilities": [f"Maintenir les plans de {repo_name}"],
                    "goals": [f"Citoyennisation complète de {repo_name}"],
                    "stratum": skill.get("layer", "L4_TOOLS"),
                    "status": "active",
                }
            )
            existing_ids.add(citizen_id)
            added += 1

        if added > 0 and not dry_run:
            self.citizens_yaml.write_text(
                yaml.dump(citizens_data, allow_unicode=True, sort_keys=False),
                encoding="utf-8",
            )
            logger.info("citizens.yaml updated: %d repo citizens added", added)

        return errors
