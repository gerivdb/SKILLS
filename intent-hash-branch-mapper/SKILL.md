---
type: SKILL
version: "1.0.0"
intent_hash: 0xINTENT_HASH_BRANCH_MAPPER_20260808
---

# Intent Hash Branch Mapper

## Objectif

Mapper IntentHash → branch_name et stocker dans KORX cache L1.

## Déclencheur

Avant toute création de branche pour une nouvelle conversation/problématique.

## Règles

### 1. Générer le slug depuis l IntentHash

```powershell
$intentHash = "0xPRD_MOC_RLM243_LAPLACE_OPTIMIZATION_20260808"
$slug = $intentHash.ToLower() -replace '0x', '' -replace '_', '-'
$branchName = "feat/$slug"
```

### 2. Vérifier l unicité

```powershell
git branch --list "feat/*"
```

→ Si branche existe → **STOP** : utiliser branche existante
→ Si branche n existe pas → créer

### 3. Stocker dans KORX cache L1

```powershell
# Mock KORX cache L1
$korxCache = @{
    intent_hash = $intentHash
    branch_name = $branchName
    created_at = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"
}
```

### 4. Logger dans WAL NEXUS

```
[INTENT_HASH_BRANCH_MAP] intent=<hash>, branch=<name>, timestamp=<iso>
```

## Référence ADR

- **ADR** : ADR-2026-08-08-AGENTIC-GIT-WORKFLOW
- **IntentHash** : 0xAGENTIC_GIT_WORKFLOW_20260808
- **Statut ADR** : proposed
