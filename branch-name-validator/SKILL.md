---
type: SKILL
version: "1.0.0"
intent_hash: 0xBRANCH_NAME_VALIDATOR_20260808
---

# Branch Name Validator

## Objectif

Valider le nommage kebab-case et le mapping IntentHash des branches.

## Déclencheur

Avant toute création de branche `feat/<slug>`.

## Règles

### 1. Valider le format kebab-case

```powershell
$branchName = "feat/rlm243-laplace-optimization"
$slug = $branchName -replace '^(feat|fix|chore|ops|hotfix|release)/', ''
$slug -match '^[a-z0-9]+(-[a-z0-9]+)*$'
```

→ Si match → format valide
→ Si no match → **STOP** : slug invalide

### 2. Valider la longueur

```powershell
$branchName.Length -le 72
```

→ Si true → longueur valide
→ Si false → **STOP** : branche trop longue

### 3. Valider le mapping IntentHash

```powershell
# Vérifier que l'IntentHash est référencé dans le message de commit
# ou dans le nom de la branche
$intentHash = "0xPRD_MOC_RLM243_LAPLACE_OPTIMIZATION_20260808"
$branchName -match $intentHash.ToLower()
```

→ Si match → mapping valide
→ Si no match → **STOP** : IntentHash manquant

## Anti-patterns bloquants

- Branche avec underscore → BLOCKING
- Branche avec espace → BLOCKING
- Branche > 72 caractères → BLOCKING
- Branche sans IntentHash mapping → BLOCKING

## Référence ADR

- **ADR** : ADR-2026-08-08-AGENTIC-GIT-WORKFLOW
- **IntentHash** : 0xAGENTIC_GIT_WORKFLOW_20260808
- **Statut ADR** : proposed
