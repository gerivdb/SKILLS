---
type: SKILL
version: "1.0.0"
intent_hash: 0xSWARM_GIT_COORDINATOR_20260808
---

# Swarm Git Coordinator

## Objectif

Coordonner les sessions parallèles : création, synchronisation, merge.

## Déclencheur

Avant toute session Agent Manager multi-tâches.

## Règles

### 1. Créer une branche par tâche

```powershell
# Pour chaque tâche du swarm
$tasks = @("task-a", "task-b", "task-c")
foreach ($task in $tasks) {
    $branchName = "feat/swarm-$task"
    git checkout -b $branchName
    git push origin $branchName
}
```

### 2. Isoler les sessions

- Session A → `feat/swarm-task-a`
- Session B → `feat/swarm-task-b`
- Pas de travail parallèle sur même branche

### 3. Synchroniser les branches

```powershell
# Fetch toutes les branches
git fetch origin

# Rebase chaque branche sur main
git rebase origin/main feat/swarm-task-a
git rebase origin/main feat/swarm-task-b
```

### 4. Détecter les conflits

```powershell
# Vérifier les conflits avant merge
git merge-base --is-ancestor origin/main feat/swarm-task-a
if ($LASTEXITCODE -ne 0) {
    # Conflit détecté
    Write-Output "[CONFLICT] feat/swarm-task-a"
}
```

### 5. Orchestrer le merge

```powershell
# Merge via KEEL
# 1. Valider PR via MOX (P-106/P-107)
# 2. Champion selection via KEEL META-LOOP
# 3. Merge automatique
# 4. Supprimer branche
```

## Anti-patterns bloquants

- Deux sessions sur même branche → BLOCKING
- Merge sans validation MOX → BLOCKING
- Suppression de branche avant merge PR → BLOCKING

## Référence ADR

- **ADR** : ADR-2026-08-08-AGENTIC-GIT-WORKFLOW
- **IntentHash** : 0xAGENTIC_GIT_WORKFLOW_20260808
- **Statut ADR** : proposed
