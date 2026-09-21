---
type: skill
version: "1.0.0"
date: "2026-09-15"
status: draft
intent_hash: 0xTRIX_SDK_IMPORT_ALIGNER_20260915
---

# Skill: trix-sdk-import-aligner

## Purpose
Résout préventivement les erreurs d'import TRIX SDK (ERR-001 à ERR-004) en alignant
les imports avec le SDK TRIX réel (`TrixUnavailable`, `TrixHealth`, `ContainerSpec`).

## Context
Les erreurs suivantes sont fréquentes dans les repos utilisant TRIX :
- `NameError: ContainerSpec is not defined`
- `ImportError` sur `trix_sdk`
- Imports incohérents entre versions TRIX

Ce skill détecte et corrige automatiquement ces imports.

## Prerequisites
- TRIX SDK installé et accessible
- Accès en écriture au repo cible

## Workflow

### 1. Scanner les imports TRIX
```powershell
grep -r "trix_sdk" <repo>/src/
```

### 2. Vérifier la disponibilité des symbols
```powershell
# Vérifier que ContainerSpec, TrixUnavailable, TrixHealth existent
python -c "from trix_sdk import ContainerSpec, TrixUnavailable, TrixHealth; print('OK')"
```

### 3. Aligner les imports
- Remplacer `from trix_sdk import X` par les imports valides
- Ajouter les imports manquants
- Supprimer les imports inutilisés

### 4. Valider
```powershell
cargo check  # ou pytest selon le repo
```

## Anti-patterns
- ❌ Modifier les imports sans vérifier la disponibilité
- ❌ Supprimer des imports utilisés
- ❌ Ajouter des imports non nécessaires

## References
- **ADR** : ADR-2026-09-14-047-CTULU-tools-syntax-fix
- **Rule** : test-handler-first.md
- **Skill** : slm-micro-executor
