---
name: worktree-hygiene-auditor
description: Détecte et nettoie les worktrees orphelins dans un repo git. Utilise ce skill quand tu dois auditer les worktrees, supprimer les worktrees fermés, ou pruner les worktrees stagnants.
version: 1.0.0
intent_hash: 0xWORKTREE_HYGIENE_AUDITOR_20260809
---

# Worktree Hygiene Auditor

## Objectif
Maintenir la propreté des worktrees git et kilo worktrees en détectant et supprimant les worktrees orphelins, fermés ou stagnants.

## Déclencheur
- Fin de session KiloCode
- Audit quotidien
- Avant toute création de nouveau worktree
- Après chaque merge de branche feature

## Prérequis
- Repo git valide
- Accès en écriture au repo
- Git >= 2.5 (worktree support)
- **ONTOLOGY** : définitions `worktree`, `kilo_worktree`, `working_tree`

## Définitions ontologiques (ONTOLOGY)

| Terme | Définition | Registre |
|-------|------------|----------|
| **Git worktree** | Instance Git d'un même dépôt sur une branche différente, partageant le même `.git`. | `git worktree list` |
| **Kilo worktree** | Espace de travail isolé géré par Agent Manager, enregistré dans `.kilo/agent-manager.json`. | `.kilo/agent-manager.json` |
| **Répertoire simple** | Fichiers sans gestionnaire, ni git worktree ni Agent Manager. | Filesystem only |

**Règle de discrimination** : avant toute action, déterminer le type de worktree via les registres ontologiques.

## Protocole

### Étape 0 — Déterminer le type de worktree (OBLIGATOIRE)

```powershell
# 1. Vérifier agent-manager.json
$am = Get-Content .kilo/agent-manager.json -Raw | ConvertFrom-Json
$isKiloWorktree = $am.worktrees.PSObject.Properties.Name -contains $worktreeId

# 2. Vérifier git worktree list
$isGitWorktree = git worktree list --porcelain | Select-String $path

# 3. Déterminer le type
if ($isKiloWorktree) {
    $type = "kilo_worktree"
} elseif ($isGitWorktree) {
    $type = "git_worktree"
} else {
    $type = "plain_directory"
}
```

| Type | Action de nettoyage |
|------|---------------------|
| `kilo_worktree` | Utiliser Agent Manager API / `agent-manager-reconcile.ps1` |
| `git_worktree` | Utiliser `git worktree remove` |
| `plain_directory` | **STOP** — demander HITL avant suppression |

### Étape 1 — Lister tous les worktrees
```powershell
git worktree list
```

### Étape 2 — Vérifier l'état de chaque worktree

Pour chaque worktree :
1. Vérifier que le chemin existe physiquement
2. Vérifier que la branche associée existe encore
3. Vérifier le dernier commit sur la branche
4. Vérifier s'il y a des modifications non commitées

### Étape 3 — Vérifier le contenu unique (GATE-4) — OBLIGATOIRE

Pour chaque worktree, **AVANT toute suppression** :

```powershell
# Dans le worktree
git log origin/main..HEAD
git diff origin/main...HEAD
```

| Résultat | Action |
|----------|--------|
| `git log origin/main..HEAD` = vide + `git diff origin/main...HEAD` = vide | Continuer vers Étape 4 |
| `git log origin/main..HEAD` non vide | **BLOCAGE** — commits uniques détectés |
| `git diff origin/main...HEAD` non vide | **BLOCAGE** — fichiers uniques détectés |

**Si BLOCAGE** :
- Ne PAS supprimer le worktree
- Créer une PR pour intégrer les commits, ou
- Sauvegarder les commits (rebase/cherry-pick) avant suppression
- Logger l'alerte dans WAL NEXUS

### Étape 4 — Décider pour chaque worktree

| Cas | Action |
|-----|--------|
| Worktree sur branche mergée + contenu unique vide | `git worktree remove <path>` |
| Worktree sur branche supprimée + contenu unique vide | `git worktree remove <path>` |
| Worktree avec modifications non commitées | Sauvegarder les modifications, puis supprimer |
| Worktree inactif > 7 jours + contenu unique vide | `git worktree remove <path>` |
| Worktree avec contenu unique NON VIDE | **CONSERVER** — créer une PR ou sauvegarder |
| Worktree actif et nécessaire | Conserver |

### Étape 5 — Supprimer les worktrees orphelins
```powershell
git worktree remove <path>
```

### Étape 6 — Pruner les worktrees supprimés
```powershell
git worktree prune
```

### Étape 7 — Vérification finale
```powershell
git worktree list
```

## Sortie standard

```yaml
worktrees_active: []
worktrees_removed: []
worktrees_pruned: []
worktrees_at_risk: []  # ← NOUVEAU: worktrees avec contenu unique non sur main
recommendations: []
```

## Anti-patterns bloquants
- Supprimer un worktree avec des modifications non commitées sans sauvegarde
- Supprimer le worktree principal (racine du repo)
- Supprimer un worktree dont la branche est encore active
- Oublier de pruner après suppression manuelle
- **Supprimer un worktree sans exécuter `git log origin/main..HEAD` et `git diff origin/main...HEAD`**
- **Utiliser `git worktree remove --force` sans vérification GATE-4**
- **Supprimer un worktree contenant des commits uniques non présents sur `origin/main`**
- **Confondre `git worktree`, `kilo_worktree` et répertoire simple** — toujours discriminer via Étape 0

## Référence ADR
- **ADR** : ADR-2026-08-09-001-WORKTREE-CLOSURE-PROTOCOL
- **IntentHash** : 0xWORKTREE_HYGIENE_AUDITOR_20260809
- **Dépôt** : gerivdb/GeriCode
- **Statut ADR** : proposed
- **Màj requise si** : GATE-4 n'est pas respecté lors d'une suppression

## Références
- **IntentHash parent** : `0xPRD_MOC_GIT_HYGIENE_MECHANISMS_20260809`
- **IntentHash review fixes** : `0xPRD_MOC_GIT_HYGIENE_REVIEW_FIXES_20260809`
- **IntentHash incohérences** : `0xPRD_MOC_GIT_HYGIENE_INCOHERENCE_FIXES_20260809`
- **PRD MOC correctif** : `PRD-MOC-AGENT-MANAGER-V9.9-WORKTREE-CLEANUP-SAFETY-2026-08-10.md`
- **ONTOLOGY** : `ONTOLOGY.yaml` (`worktree`, `kilo_worktree`), `concepts/kilo-worktree.md`
