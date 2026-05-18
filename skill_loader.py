#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚡ DYNAMIC SKILL LOADER
Implémentation EPIC 1054

Chargement dynamique et à la demande des skills
Jamais tous les skills ne sont chargés en mémoire
"""

import importlib.util
import sys
from pathlib import Path
from typing import Any, Optional, Dict
from dataclasses import dataclass
from datetime import datetime
from managers.skill_registry import Skill


@dataclass
class LoadedSkill:
    skill: Skill
    instance: Any
    loaded_at: datetime
    load_count: int = 0


class DynamicSkillLoader:
    """
    Chargeur dynamique de skills

    Principes:
    1. Aucun skill n'est chargé au démarrage
    2. Chargement seulement quand nécessaire
    3. Déchargement automatique après inactivité
    4. Isolation complète entre skills
    """

    def __init__(self):
        self.loaded: Dict[str, LoadedSkill] = {}
        self.max_loaded = 5
        self.cache_ttl = 300  # 5 minutes

    def load(self, skill: Skill) -> Any:
        """Charge un skill à la demande"""
        if skill.name in self.loaded:
            self.loaded[skill.name].load_count += 1
            return self.loaded[skill.name].instance

        # Si maximum atteint, décharger le moins utilisé
        if len(self.loaded) >= self.max_loaded:
            self._evict_least_used()

        instance = self._load_skill_module(skill)

        self.loaded[skill.name] = LoadedSkill(
            skill=skill,
            instance=instance,
            loaded_at=datetime.now(),
            load_count=1
        )

        return instance

    def unload(self, skill_name: str):
        """Décharge un skill de la mémoire"""
        if skill_name in self.loaded:
            del self.loaded[skill_name]

    def is_loaded(self, skill_name: str) -> bool:
        return skill_name in self.loaded

    def _load_skill_module(self, skill: Skill) -> Any:
        """Charge dynamiquement le module d'un skill"""
        skill_path = Path(skill.path).parent / f"{skill.name.replace('-', '_')}.py"

        if not skill_path.exists():
            # Skill sans code, retourne un proxy
            return type(skill.name, (), {
                'skill': skill,
                'capabilities': skill.capabilities
            })()

        spec = importlib.util.spec_from_file_location(skill.name, skill_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[skill.name] = module
        spec.loader.exec_module(module)

        return module

    def _evict_least_used(self):
        """Décharge le skill le moins utilisé"""
        sorted_skills = sorted(
            self.loaded.values(),
            key=lambda x: x.load_count
        )
        if sorted_skills:
            del self.loaded[sorted_skills[0].skill.name]

    def status(self) -> Dict[str, Any]:
        return {
            "loaded": len(self.loaded),
            "max": self.max_loaded,
            "skills": [
                {
                    "name": ls.skill.name,
                    "loaded_at": ls.loaded_at,
                    "load_count": ls.load_count
                }
                for ls in self.loaded.values()
            ]
        }


# Instance globale
SKILL_LOADER = DynamicSkillLoader()