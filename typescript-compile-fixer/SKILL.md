---
name: typescript-compile-fixer
description: Corrige les erreurs de compilation TypeScript récurrentes dans GeriCode : `as const`, `as any`, expected/actual, null checks. À utiliser quand `npm run compile` échoue, avant packaging VSX, ou pour nettoyer les TS errors bloquantes.
---

# TypeScript Compile Fixer

## Objectif

Réduire le temps de debug des erreurs TypeScript dans GeriCode en appliquant des corrections sûres et réutilisables sur les patterns récurrents : `as const`, `as any`, expected/actual, null checks.

## Déclencheur

- Échec de `npm run compile` ou `npm run compile:src`
- Erreurs TypeScript bloquant le packaging VSX
- Demande explicite de nettoyage TS
- Revue de code avec erreurs TS récurrentes

## Workflow

### Étape 1 — Capturer les erreurs

```bash
npm run compile:src
npm run compile
```

Collecter les chemins et codes d’erreur.

### Étape 2 — Classifier

Utiliser `references/common-ts-errors.md` pour mapper chaque erreur à un pattern de correction.

### Étape 3 — Appliquer les corrections

Pour chaque erreur :
1. Ouvrir le fichier concerné
2. Appliquer le pattern de correction documenté
3. Ne pas changer le comportement observable
4. Préférer `as const`, `unknown`, ou guards plutôt que `as any`

### Étape 4 — Vérifier

```bash
npm run compile
```

Toutes les erreurs ciblées doivent être résolues.

## Resources

### scripts/

- `scripts/fix_ts_errors.py` — Parse la sortie de compilation et propose des corrections automatiques pour les patterns connus.

### references/

- `references/common-ts-errors.md` — Catalogue des erreurs TS récurrentes et corrections associées.

### assets/

- `assets/tsconfig-template.json` — Configuration TypeScript de référence pour GeriCode.
