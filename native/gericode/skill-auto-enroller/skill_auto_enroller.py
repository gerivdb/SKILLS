"""
Skill Auto Enroller
Pipeline 1-clic : repo → verse + citizen + bridge + REGISTRY + VERSES.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Literal

import yaml

logger = logging.getLogger(__name__)


class SkillAutoEnrollerError(Exception):
    """Erreur lors de l'enrôlement automatique de skill."""


class SkillAutoEnroller:
    def __init__(
        self,
        known_repositories_path: Path,
        citizens_yaml_path: Path,
        verses_dir: Path,
        bridges_path: Path,
        registry_yaml_path: Path,
        skills_dir: Path,
    ) -> None:
        self.known_repositories_path = known_repositories_path
        self.citizens_yaml_path = citizens_yaml_path
        self.verses_dir = verses_dir
        self.bridges_path = bridges_path
        self.registry_yaml_path = registry_yaml_path
        self.skills_dir = skills_dir

    def enroll(
        self,
        skill_name: str,
        repo_name: str,
        layer: str = "L4",
        local_path: Path | None = None,
        source_path: str = "",
        update_gitignore: bool = False,
    ) -> dict:
        """Exécute le pipeline complet d'enrôlement."""
        report: dict = {
            "skill_name": skill_name,
            "repo_name": repo_name,
            "steps": [],
            "errors": [],
            "warnings": [],
            "rolled_back": False,
        }

        # Étape 1: Vérifier le repo
        try:
            self._verify_repo(repo_name)
            report["steps"].append({"step": 1, "name": "verify_repo", "status": "OK"})
        except Exception as exc:
            report["errors"].append(f"Step 1 failed: {exc}")
            return report

        # Étape 2: Créer le verse
        verse_path = None
        try:
            verse_path = self._create_verse(repo_name)
            report["steps"].append({"step": 2, "name": "create_verse", "status": "OK", "path": str(verse_path)})
        except Exception as exc:
            report["errors"].append(f"Step 2 failed: {exc}")
            return report

        # Étape 3: Enregistrer le citizen
        try:
            self._register_citizen(repo_name, layer)
            report["steps"].append({"step": 3, "name": "register_citizen", "status": "OK"})
        except Exception as exc:
            report["errors"].append(f"Step 3 failed: {exc}")
            self._rollback_verse(repo_name)
            report["rolled_back"] = True
            return report

        # Étape 4: Créer le bridge
        try:
            self._create_bridge(repo_name, layer, local_path)
            report["steps"].append({"step": 4, "name": "create_bridge", "status": "OK"})
        except Exception as exc:
            report["errors"].append(f"Step 4 failed: {exc}")
            self._rollback_verse(repo_name)
            self._rollback_citizen(repo_name)
            report["rolled_back"] = True
            return report

        # Étape 5: Enregistrer le skill
        try:
            self._register_skill(skill_name, repo_name, source_path)
            report["steps"].append({"step": 5, "name": "register_skill", "status": "OK"})
        except Exception as exc:
            report["errors"].append(f"Step 5 failed: {exc}")
            self._rollback_verse(repo_name)
            self._rollback_citizen(repo_name)
            self._rollback_bridge(repo_name)
            report["rolled_back"] = True
            return report

        # Étape 6: Mettre à jour .gitignore
        if update_gitignore:
            try:
                self._update_gitignore(repo_name)
                report["steps"].append({"step": 6, "name": "update_gitignore", "status": "OK"})
            except Exception as exc:
                report["warnings"].append(f"Step 6 failed: {exc}")

        return report

    def _verify_repo(self, repo_name: str) -> None:
        """Vérifie que le repo existe dans known_repositories.yaml."""
        data = yaml.safe_load(self.known_repositories_path.read_text(encoding="utf-8")) or {}
        found = False
        for key, value in data.items():
            if isinstance(key, str) and key.endswith("_REPOS") and isinstance(value, list):
                for item in value:
                    if isinstance(item, dict) and item.get("name", "").upper() == repo_name.upper():
                        found = True
                        break
        if not found:
            raise SkillAutoEnrollerError(f"Repo {repo_name} not found in known_repositories.yaml")

    def _create_verse(self, repo_name: str) -> Path:
        """Crée le verse du repo citoyen."""
        from repo_citizen_manager import create_verse
        return create_verse(repo_name, self.verses_dir)

    def _register_citizen(self, repo_name: str, layer: str) -> None:
        """Enregistre le citizen."""
        from repo_citizen_manager import register_citizen
        register_citizen(repo_name, self.citizens_yaml_path, layer=layer)

    def _create_bridge(self, repo_name: str, layer: str, local_path: Path | None) -> None:
        """Crée le bridge."""
        from repo_citizen_manager import create_bridge
        full_name = f"gerivdb/{repo_name}"
        create_bridge(
            repo_name,
            self.bridges_path,
            full_name=full_name,
            layer=layer,
            local_path=str(local_path) if local_path else None,
        )

    def _register_skill(self, skill_name: str, repo_name: str, source_path: str) -> None:
        """Enregistre le skill dans REGISTRY.yaml."""
        from repo_citizen_manager import register_skill
        register_skill(
            skill_name,
            self.registry_yaml_path,
            source_repo=f"gerivdb/{repo_name}",
            description=f"Skill {skill_name} pour {repo_name}",
        )

    def _update_gitignore(self, repo_name: str) -> None:
        """Met à jour le .gitignore si nécessaire."""
        # Placeholder: implémenter la logique de mise à jour du .gitignore
        pass

    def _rollback_verse(self, repo_name: str) -> None:
        """Supprime le verse créé."""
        verse_path = self.verses_dir / f"{repo_name.lower()}-verse.md"
        if verse_path.exists():
            verse_path.unlink()

    def _rollback_citizen(self, repo_name: str) -> None:
        """Supprime le citizen créé."""
        # Placeholder: implémenter la suppression du citizen
        pass

    def _rollback_bridge(self, repo_name: str) -> None:
        """Supprime le bridge créé."""
        # Placeholder: implémenter la suppression du bridge
        pass
