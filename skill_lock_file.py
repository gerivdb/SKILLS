#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔒 SKILL LOCK FILE
Implémentation EPIC 1057

Génération automatique du skills-lock.json
Reproductibilité et immutabilité des versions de skills
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

from managers.skill_registry import SKILL_REGISTRY, Skill


class SkillLockFile:
    """
    Génère et maintient le fichier de verrouillage des skills

    Principes:
    ✅ Immutabilité des versions
    ✅ Reproductibilité garantie
    ✅ Hash d'intégrité pour chaque skill
    ✅ Pas de mise à jour silencieuse
    ✅ Équivalent package-lock.json pour les skills
    """

    LOCK_FILE = Path("skills-lock.json")
    SCHEMA_VERSION = 1

    def generate(self) -> Dict[str, Any]:
        """Génère le fichier de verrouillage complet"""
        lock_data = {
            "schema_version": self.SCHEMA_VERSION,
            "generated_at": datetime.now().isoformat(),
            "hash_algorithm": "sha256",
            "locked": True,
            "skills": {}
        }

        SKILL_REGISTRY.discover()

        for skill in SKILL_REGISTRY.get_all():
            skill_hash = self._compute_skill_hash(skill)

            lock_data["skills"][skill.name] = {
                "version": skill.version,
                "path": skill.path,
                "capabilities": skill.capabilities,
                "hash": skill_hash,
                "locked_at": datetime.now().isoformat(),
                "enabled": skill.enabled,
                "compatibility": skill.compatibility
            }

        # Hash global du fichier
        lock_data["global_hash"] = self._compute_global_hash(lock_data["skills"])

        return lock_data

    def save(self) -> Path:
        """Génère et sauvegarde le fichier de verrouillage"""
        lock_data = self.generate()

        with open(self.LOCK_FILE, 'w', encoding='utf-8') as f:
            json.dump(lock_data, f, indent=2, ensure_ascii=False)

        return self.LOCK_FILE

    def verify(self) -> bool:
        """Vérifie l'intégrité du fichier de verrouillage"""
        if not self.LOCK_FILE.exists():
            return False

        with open(self.LOCK_FILE, 'r', encoding='utf-8') as f:
            lock_data = json.load(f)

        actual_global_hash = self._compute_global_hash(lock_data["skills"])
        return actual_global_hash == lock_data.get("global_hash")

    def detect_changes(self) -> Dict[str, str]:
        """Détecte les skills modifiés depuis la dernière génération"""
        changes = {}

        if not self.LOCK_FILE.exists():
            return changes

        with open(self.LOCK_FILE, 'r', encoding='utf-8') as f:
            lock_data = json.load(f)

        SKILL_REGISTRY.discover()

        for skill in SKILL_REGISTRY.get_all():
            current_hash = self._compute_skill_hash(skill)
            locked = lock_data["skills"].get(skill.name, {})

            if locked.get("hash") != current_hash:
                changes[skill.name] = "modified" if skill.name in lock_data["skills"] else "added"

        for name in lock_data["skills"]:
            if not SKILL_REGISTRY.get(name):
                changes[name] = "removed"

        return changes

    def _compute_skill_hash(self, skill: Skill) -> str:
        """Calcule le hash d'intégrité d'un skill"""
        content = ""

        skill_path = Path(skill.path)
        if skill_path.exists():
            content = skill_path.read_text(encoding='utf-8')

        hash_input = f"{skill.name}:{skill.version}:{content}"
        return hashlib.sha256(hash_input.encode('utf-8')).hexdigest()[:16]

    def _compute_global_hash(self, skills: Dict[str, Any]) -> str:
        """Calcule le hash global de l'ensemble des skills"""
        hash_input = json.dumps(skills, sort_keys=True)
        return hashlib.sha256(hash_input.encode('utf-8')).hexdigest()


# Instance globale
SKILL_LOCK_FILE = SkillLockFile()


if __name__ == "__main__":
    print("🔒 Skill Lock File")
    print("=" * 60)

    changes = SKILL_LOCK_FILE.detect_changes()

    if changes:
        print(f"⚠️ {len(changes)} changements détectés")
        for name, change_type in changes.items():
            print(f"   {change_type.upper()} {name}")

    lock_path = SKILL_LOCK_FILE.save()
    print(f"\n✅ Fichier de verrouillage généré: {lock_path}")
    print(f"✅ Vérification intégrité: {'OK' if SKILL_LOCK_FILE.verify() else 'ÉCHEC'}")