---
type: skill
version: "1.0.0"
date: "2026-09-15"
status: draft
intent_hash: 0xNEXUS_COMPLIANCE_RENAMER_20260915
---

# Skill: nexus-compliance-renamer

## Purpose
Automatise la conformité NEXUS en renommant les fichiers selon la convention :
`*-verse.md` → `*.verse.md`

## Context
Les fichiers VERSES doivent suivre la convention de nommage NEXUS.
Ce skill détecte les fichiers non conformes et les renomme automatiquement.

## Prerequisites
- Accès en écriture au repo cible
- Git configuré

## Workflow

### 1. Scanner les fichiers non conformes
```powershell
Get-ChildItem -Recurse -Filter "*-verse.md" | Select-Object FullName
```

### 2. Vérifier les dépendances
- Vérifier que les liens internes (markdown) sont mis à jour
- Vérifier que les références dans les documents de gouvernance sont cohérentes

### 3. Renommer
```powershell
git mv <old-name> <new-name>
```

### 4. Mettre à jour les références
```powershell
# grep -r "old-name" <repo>/
# Remplacer par "new-name"
```

### 5. Commit
```powershell
git add .
git commit -m "chore(nexus): rename *-verse.md to *.verse.md"
```

## Anti-patterns
- ❌ Renommer sans vérifier les liens internes
- ❌ Oublier de mettre à jour les références
- ❌ Renommer des fichiers déjà conformes

## References
- **Rule** : frontmatter-guardian
- **Skill** : git-atomic-push
- **Pattern** : Pattern D (edit atomique)
