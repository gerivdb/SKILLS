---
type: SKILL
version: "1.0.0"
status: active
date: "2026-10-26"
intent_hash: 0xSKILL_KWO_20261026
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/kilo-worktree-operator/SKILL.md
---

# Skill — kilo-worktree-operator (6 super-pouvoirs)

## Objectif

Manipulateur headless de l'Agent Manager via CLI. Offre 6 commandes pour la gestion autonome des worktrees, sections, synchronisation, épinglage, instantiation et nettoyage des sessions orphelines. Couche CRUD — opérations Create, Read, Update, Delete sur l'écosystème worktree.

## Déclencheur

- `kilo-worktree-operator`, `wt:purge-merged`, `wt:organize-sections`, `wt:sync-all`, `wt:pin`, `wt:unpin`, `wt:spawn-clean`, `wt:ghost-buster`
- Manipulation headless de l'Agent Manager sans interface graphique

## Entrées

- `commande`: l'une des 6 commandes (obligatoire)
- `project_id`: `RAGX` ou `SKILLS` (optionnel, défaut SKILLS)
- `branch_name`: nom de la branche (pour `wt:spawn-clean`, `wt:pin`, `wt:unpin`)
- `worktree_id`: ID du worktree (pour `wt:pin`, `wt:unpin`)

## Sorties

- Rapport JSON structuré par commande avec statut, actions effectuées et éventuelles erreurs
- Mise à jour de `agent-manager.json` et du système de fichiers selon la commande

## Les 6 super-pouvoirs

### 1. `wt:purge-merged`

Détecte les branches mergées dans `main`, supprime les dossiers physiques de worktree associés et nettoie `agent-manager.json`.

```
wt:purge-merged --project <PROJECT_ID>
```

### 2. `wt:organize-sections`

Analyse les préfixes de branches, crée des sections thématiques dans `agent-manager.json` et sort les worktrees de l'état `ungrouped`.

```
wt:organize-sections --project <PROJECT_ID>
```

### 3. `wt:sync-all`

Exécute `git fetch` + `git merge origin/main` sur tous les worktrees en parallèle. Respecte le protocole BDCP (fetch avant merge).

```
wt:sync-all --project <PROJECT_ID>
```

### 4. `wt:pin` / `wt:unpin`

Gestion de priorité dynamique via la clé `pinnedWorktrees` de `agent-manager.json`.

```
wt:pin --worktree <WORKTREE_ID>
wt:unpin --worktree <WORKTREE_ID>
```

### 5. `wt:spawn-clean`

Instanciation atomique : crée une branche, pose un worktree, génère `metadata.json`, inscrit la session dans `agent-manager.json` sans clé `pending:`.

```
wt:spawn-clean --branch <BRANCH_NAME> --project <PROJECT_ID>
```

### 6. `wt:ghost-buster`

Détecte et élimine les sessions orphelines et les clés `pending:<uuid>` dans `tabOrder.local`.

```
wt:ghost-buster --project <PROJECT_ID>
```

## Script d'investigation

`scripts/wt_operator.py` — voir ci-dessous. Supporte les 6 commandes ci-dessus.

## Tests

- `tests/test_kilo_worktree_operator.py` — tester chaque commande sur un dépôt factice.
- `tests/test_wt_spawn_clean_atomic.py` — vérifier l'atomicité de `wt:spawn-clean`.

## Probes

- Zéro session orpheline non détectée par `wt:ghost-buster`
- Zéro worktree mergé non purgé par `wt:purge-merged`
- Zéro `pending:<uuid>` résiduel après `wt:ghost-buster`

## WAL NEXUS

```
[WAL_NEXUS] skill=kilo-worktree-operator action=<COMMANDE> timestamp=<ISO> project=<PROJECT> result=<OK|FAIL> details=<JSON>
```

## Référence ADR

- **ADR** : ADR-2026-06-28-001-LOGICAL-ARCHITECTURE-N1-N4
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed