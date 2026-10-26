---
type: SKILL
version: "1.0.0"
status: active
date: "2026-10-26"
intent_hash: 0xSKILL_WGC_20261026
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/worktree-genetic-contractor/SKILL.md
---

# Skill — worktree-genetic-contractor

## Objectif

Injection du contrat de mission et de l'SSoT à la naissance du worktree. Le `setup-script.ps1` génère automatiquement à la racine du worktree un fichier `WORKTREE_MISSION.md` sur-mesure contenant le périmètre strict autorisé, les dépendances parentes, l'IntentHash de la session et la commande de test unitaire à faire passer. Couche Worktree Engineering — opération d'héritage génétique.

## Déclencheur

- `worktree-genetic-contractor`, `contrat mission worktree`, `WORKTREE_MISSION.md`, `génétique worktree`
- À chaque création de worktree via `wt:spawn-clean` ou `agent_manager worktree`

## Entrées

- `worktree_path`: chemin physique du nouveau worktree (défaut : `$env:WORKTREE_PATH`)
- `repo_path`: racine du dépôt maître parent (défaut : `$env:REPO_PATH`)
- `branch_name`: nom de la branche (ex: `feat/citizen-cluster-a`)
- `session_id`: ID de la session Agent Manager (optionnel)
- `intent_hash`: IntentHash de la session (optionnel)

## Sorties

- `WORKTREE_MISSION.md` à la racine du worktree
- Entrée WAL NEXUS horodatée

## Règles

### 1. Génération automatique

Le contrat est généré à partir du nom de branche :
- `feat/citizen-*` → périmètre : skills L4 + citizen L3
- `feat/gericode-*` → périmètre : GeriCode L2 + ACT Protocol
- `feat/worktree-*` → périmètre : worktree operator skills

### 2. Contenu du contrat

Chaque `WORKTREE_MISSION.md` contient :
- Périmètre strict (fichiers touchables vs interdits)
- Dépendances parentes et IntentHash
- Commande de test unitaire à faire passer
- Lien vers le registre des skills concernés

### 3. Interdiction d'agir hors périmètre

L'agent ne doit pas modifier de fichiers en dehors du périmètre défini dans le contrat.

## Script d'investigation

`scripts/contract.ps1` — voir ci-dessous.

## Tests

- `tests/test_worktree_genetic_contractor.ps1` — générer un contrat pour `feat/citizen-test`, vérifier le contenu.

## Probes

- Chaque worktree créé possède un `WORKTREE_MISSION.md`
- Aucun fichier hors périmètre n'est modifié par l'agent

## WAL NEXUS

```
[WAL_NEXUS] skill=worktree-genetic-contractor action=contract timestamp=<ISO> worktree=<PATH> branch=<BRANCH> intent_hash=<HASH>
```

## Référence ADR

- **ADR** : ADR-2026-06-28-001-LOGICAL-ARCHITECTURE-N1-N4
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed
