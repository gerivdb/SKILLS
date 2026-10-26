---
type: SKILL
version: "1.0.0"
status: active
date: "2026-10-26"
intent_hash: 0xSKILL_AUSM_20261026
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/agent-manager-ui-semantic-map/SKILL.md
---

# Skill — agent-manager-ui-semantic-map

## Objectif

Empêcher les hallucinations d'interprétation des boutons graphiques Kilo Code / Agent Manager. Fournit un dictionnaire sémantique qui lie chaque libellé d'UI à son action Git sous-jacente. Couche CRUD — opération Read (référence).

## Déclencheur

- `agent-manager-ui-semantic-map`, `dictionnaire UI Kilo`, `bouton supprimer worktree`, `bouton mettre à jour`, `interprétation menu contextuel`

## Entrées

- `ui_label`: libellé du bouton ou menu à interpréter (optionnel)
- `action_git`: action Git à vérifier (optionnel)

## Sorties

- Dictionnaire sémantique complet : libellé UI → action Git réel → effet sur l'UI → effet sur agent-manager.json
- Avertissement si un libellé est ambigu ou trompeur

## Règles

### 1. Table de vérité obligatoire

| Libellé UI | Icône | Action Git réelle | Effet sur worktree | Effet sur agent-manager.json | Nettoie ? |
|------------|-------|-------------------|-------------------|------------------------------|-----------|
| Supprimer le Worktree | 🗑️ Poubelle | `git worktree remove --force` + `git branch -D` | Supprimé | Entrée retirée | ✅ Oui |
| Mettre à jour depuis la base | 🔀 Fusion Git | `git fetch` + `git merge origin/main` | Mis à jour | Aucun changement | ❌ Non |
| Nouvelle section | ➕ Plus | Crée clé "sections" dans JSON | Aucun | Entrée déplacée vers section | ⚠️ Partiel |
| Épingler | 📌 Épingle | Modifie "pinnedWorktrees" | Aucun | Priorité modifiée | ❌ Non |

### 2. Interdiction d'interprétation

Jamais déduire la fonction d'un bouton à partir de son libellé seul. Toujours consulter le dictionnaire avant d'agir.

### 3. "ungrouped" n'est pas un fantôme

Un worktree dans `ungrouped` est un worktree valide sans section dédiée. Ce n'est pas une entrée orpheline à supprimer automatiquement.

## Script d'investigation

`scripts/ui_semantic_map.ps1` — voir ci-dessous.

## Tests

- `tests/test_agent_manager_ui_semantic_map.ps1` — vérifier que chaque libellé est associé à la bonne action Git.

## Probes

- Zéro confusion entre "Mettre à jour depuis la base" et "Supprimer le Worktree"
- Zéro worktree "ungrouped" traité comme orphelin par erreur

## WAL NEXUS

```
[WAL_NEXUS] skill=agent-manager-ui-semantic-map action=lookup timestamp=<ISO> ui_label=<LABEL> action_git=<ACTION>
```

## Référence ADR

- **ADR** : ADR-2026-06-28-001-LOGICAL-ARCHITECTURE-N1-N4
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed
