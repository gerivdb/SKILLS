---
id: PRD-005
title: skill_loader.py → CTULUResolver — intégration
repo: gerivdb/SKILLS
status: READY
priority: P1
created: 2026-06-10
author: gerivdb
depends_on:
  - SKILLS/ctulu_resolver.py (implémenté 2026-06-10)
consumers:
  - Tout consommateur de skill_loader.py
---

# PRD-005 — skill_loader.py → CTULUResolver wiring

## Contexte

`skill_loader.py` (3 237 octets) charge des skills depuis des `SKILL.md` locaux via `SkillRegistry`. Mais il ne sait pas résoudre les tools CTULU qu'un skill déclare dans son manifest. `CTULUResolver` a été implémenté (2026-06-10) mais n'est pas encore importé dans `skill_loader.py`.

## Problème

- Un skill qui déclare `tools: [dag-navigator, cluster-importer]` dans son `SKILL.md` ne peut pas les résoudre automatiquement.
- L'utilisateur doit instancier `CTULUResolver` manuellement en dehors du pipeline.
- Le lien SKILLS → CTULU reste donc manuel et non standardisé.

## Objectif

Ajouter une méthode `load_with_tools(skill_name)` dans `skill_loader.py` :

```python
def load_with_tools(skill_name: str) -> Tuple[Skill, Dict[str, Optional[ToolEntry]]]:
    """
    Charge un skill + résout ses tools CTULU en une passe.
    Retourne (skill, {tool_id: ToolEntry|None})
    """
    skill = load(skill_name)
    tools = CTULU_RESOLVER.resolve_many(skill.tools if hasattr(skill, 'tools') else [])
    return skill, tools
```

Modifier aussi le champ `Skill` dans `skill_registry.py` pour inclure `tools: List[str]`.

## Critères d'acceptation

- [ ] `skill_loader.py` importe `CTULU_RESOLVER` depuis `ctulu_resolver.py`
- [ ] Méthode `load_with_tools()` implémentée
- [ ] Dataclass `Skill` a un champ `tools: List[str]`
- [ ] Champ `tools` parsé depuis le frontmatter `SKILL.md`
- [ ] Tests dans `tests/test_skill_loader_ctulu.py` ≥ 3 tests

## Effort estimé

~20 min
