"""Skill — repo-citizen-manager

Gère la citoyennisation des repos de l'écosystème gerivdb.
Transforme chaque repo en citoyen doté d'une identité ontologique,
d'un verse VERSES, de bridges cross-repo et de plans consultables par MOX.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Literal

logger = logging.getLogger(__name__)


class RepoCitizenError(Exception):
    """Erreur lors de la citoyennisation d'un repo."""


def verify_repo(repo_name: str, known_repositories_path: Path) -> bool:
    """Vérifie qu'un repo existe dans known_repositories.yaml."""
    import yaml

    data = yaml.safe_load(known_repositories_path.read_text(encoding="utf-8")) or {}
    for key, value in data.items():
        if isinstance(key, str) and key.endswith("_REPOS") and isinstance(value, list):
            for item in value:
                if item.get("name") == repo_name:
                    return True
    return False


def check_citizen(repo_name: str, citizens_path: Path) -> bool:
    """Vérifie qu'un repo n'est pas déjà un citoyen."""
    import yaml

    data = yaml.safe_load(citizens_path.read_text(encoding="utf-8")) or {}
    for citizen in data.get("citizens", []):
        if citizen.get("id") == repo_name.upper():
            return True
    return False


def create_verse(repo_name: str, verses_dir: Path, layer: str = "L4") -> Path:
    """Crée le verse VERSES pour un repo citoyen."""
    verse_path = verses_dir / f"{repo_name.lower()}-verse.md"
    if verse_path.exists():
        raise RepoCitizenError(f"Verse existe déjà: {verse_path}")

    content = f"""---
type: VERSE
version: "1.0.0"
status: active
intent_hash: 0x{repo_name.upper()}_VERSE_20260807
citizen: {repo_name}
layer: {layer}
author: gerivdb
source_repo: gerivdb/{repo_name}
source_path: VERSES/verses/{repo_name.lower()}-verse.md
---

# {repo_name} Verse

> **Verdict** : **VERSE** — Instance narrative du repo {repo_name}.
> **Rôle** : À définir.

---

## Ontologie

- **Concepts** : À définir
- **Relations** : À définir

## Plans

- **PRD** : À définir
- **ADR** : À définir
- **INTENTS** : À définir

## Bridges

- **ONTOLOGY** : À définir
- **VERSES** : À définir
- **TOPOS** : À définir
"""
    verse_path.write_text(content, encoding="utf-8")
    logger.info("Verse créé: %s", verse_path)
    return verse_path


def register_citizen(repo_name: str, citizens_path: Path, layer: str = "L4") -> None:
    """Déclare un repo comme citoyen dans citizens.yaml."""
    import yaml

    data = yaml.safe_load(citizens_path.read_text(encoding="utf-8")) or {}
    if "citizens" not in data or data["citizens"] is None:
        data["citizens"] = []

    citizen_id = repo_name.upper()
    if any(c.get("id") == citizen_id for c in data["citizens"]):
        raise RepoCitizenError(f"Citoyen déjà déclaré: {citizen_id}")

    data["citizens"].append(
        {
            "id": citizen_id,
            "intent_hash": f"0x{citizen_id}_CITIZEN_20260807",
            "role": f"Repo citoyen {repo_name}",
            "responsibilities": [f"Maintenir les plans de {repo_name}"],
            "goals": [f"Citoyennisation complète de {repo_name}"],
            "stratum": layer,
            "status": "active",
        }
    )

    citizens_path.write_text(
        yaml.dump(data, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    logger.info("Citoyen déclaré: %s", citizen_id)


def create_bridge(repo_name: str, bridges_path: Path, full_name: str | None = None, layer: str | None = None, local_path: str | None = None) -> dict:
    """Crée un bridge cross-repo pour un repo citoyen."""
    import yaml

    data = yaml.safe_load(bridges_path.read_text(encoding="utf-8")) or {}
    if "repos" not in data or data["repos"] is None:
        data["repos"] = {}

    repo_id = repo_name.upper()
    if repo_id in data["repos"]:
        logger.info("Bridge existe déjà pour %s", repo_id)
        return data["repos"][repo_id]

    entry = {
        "full_name": full_name or f"gerivdb/{repo_name}",
        "local_path": local_path or f"D:\\DO\\WEB\\TOOLS\\{layer}\\{repo_name}" if layer else None,
        "layer": layer or "L4_TOOLS",
        "bridges": ["ONTOLOGY", "VERSES", "TOPOS"],
    }

    data["repos"][repo_id] = entry
    bridges_path.write_text(
        yaml.dump(data, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    logger.info("Bridge créé pour %s", repo_id)
    return entry


def register_skill(
    skill_name: str,
    skills_registry_path: Path,
    source_repo: str,
    skill_type: Literal["foundational", "domain", "external"] = "foundational",
    domain: str = "ecosystem-tools",
    description: str = "",
) -> None:
    """Enregistre un skill dans SKILLS/REGISTRY.yaml."""
    import yaml

    data = yaml.safe_load(skills_registry_path.read_text(encoding="utf-8")) or {}
    if "skills" not in data or data["skills"] is None:
        data["skills"] = []

    if any(s.get("name") == skill_name for s in data["skills"]):
        raise RepoCitizenError(f"Skill déjà enregistré: {skill_name}")

    skill_entry = {
        "name": skill_name,
        "description": description or f"Skill {skill_name} pour {source_repo}",
        "type": skill_type,
        "triggers": [skill_name.replace("-", " ")],
        "domain": domain,
        "version": "1.0.0",
        "author": "gerivdb",
        "license": "MIT",
        "status": "active",
        "created": "2026-08-07",
        "updated": "2026-08-07",
        "phi_weight": 0.005,
        "path": f"..\\{source_repo.replace('gerivdb/', '')}\\.kilo\\skills\\{skill_name}\\SKILL.md",
        "source": "native",
        "assimilation_status": "N/A",
        "source_repo": source_repo,
        "consumes_from": [],
    }

    data["skills"].append(skill_entry)

    if "registry" not in data:
        data["registry"] = {}
    data["registry"]["total_skills"] = len(data["skills"])
    data["registry"]["last_updated"] = "2026-08-07"

    skills_registry_path.write_text(
        yaml.dump(data, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    logger.info("Skill enregistré: %s dans %s", skill_name, skills_registry_path)
