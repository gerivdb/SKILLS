---
name: vsx-packager
description: Automatise le packaging VSX pour GeriCode : bundle, .vscodeignore, package VSIX, vérification taille. À utiliser avant toute publication VSIX, après modifications de code, ou pour industrialiser la chaîne de validation.
---

# VSX Packager

## Objectif

Standardiser et automatiser le packaging VSX pour GeriCode :
`npm run bundle` → `.vscodeignore` validation → `npx vsce package` → vérification taille.
Réduit les cycles de packaging et évite les oublis de `.vscodeignore`.

## Déclencheur

- Après modification de code source (`src/`, `package.json`)
- Avant création d’une release ou d’un `.vsix`
- Lors de la vérification opérationnelle (`operational-verification`)
- Demande explicite de packaging VSX

## Workflow

### Étape 1 — Compiler le bundle

```bash
npm run bundle
```

Vérifier que le répertoire `out/` est généré et à jour.

### Étape 2 — Vérifier `.vscodeignore`

Utiliser `assets/vscodeignore-template` comme référence.
S’assurer que les artefacts de build, tests, sources et `.git` sont exclus.

### Étape 3 — Packager avec `vsce`

```bash
npx vsce package --no-yarn
```

### Étape 4 — Vérifier la taille

Le `.vsix` généré doit être inférieur à la limite définie dans `references/vsce-commands.md`.
Si la taille est excessive, ajuster `.vscodeignore` et re-packer.

## Resources

### scripts/

- `scripts/package_vsix.py` — Automatise les étapes 1 à 4 et génère un rapport.

### references/

- `references/vsce-commands.md` — Commandes `vsce`, limites de taille, bonnes pratiques.

### assets/

- `assets/vscodeignore-template` — Template `.vscodeignore` pour VSIX.
