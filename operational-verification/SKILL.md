---
name: operational-verification
description: Workflow standardisé de vérification opérationnelle pour GeriCode. Exécute compile → test → VSX bundle → packaging VSIX → rapport. Utilise ce skill quand tu dois valider un livrable, vérifier l'état opérationnel du repo, ou industrialiser la chaîne de validation.
version: 1.0.0
intent_hash: 0xOPERATIONAL_VERIFICATION_20260811
---

# Operational Verification

## Objectif
Standardiser et automatiser la chaîne de validation opérationnelle de GeriCode :
compile TypeScript → tests Jest → bundle VSX → package VSIX → rapport.
Réduit les cycles de correction/validation de ~60% en évitant les re-jeux manuels.

## Déclencheur
- Après modification de code source (`src/`, `tests/`)
- Avant création de PR ou merge
- Avant packaging VSX (`npm run bundle`, `npx vsce package`)
- Fin de session multi-repo touchant GeriCode
- Demande explicite de vérification opérationnelle

## Prérequis
- Node.js ≥ 18 installé
- `npm install` effectué dans `D:\DO\WEB\TOOLS\L2-PLATFORM\GeriCode`
- Remote `origin` configuré sur `https://github.com/gerivdb/GeriCode.git`
- Pas de processus zombies bloquant les fichiers (`git.exe`, `node.exe`)

## Workflow

### Étape 1 — Compile source (`compile:src`)

```powershell
npm run compile:src
```

**Vérification** : `tsc -p tsconfig.build.json` doit se terminer sans erreur.
**Échec bloquant** : toute erreur TypeScript stoppe le workflow et exige une correction avant de continuer.

### Étape 2 — Compile complet (`compile`)

```powershell
npm run compile
```

**Vérification** : `tsc -p ./` génère `out/extension.js` et `out/extension.d.ts` sans erreur.
**Note** : cette étape vérifie aussi les déclarations de type publiques.

### Étape 3 — Tests Jest

```powershell
npx jest --no-coverage
```

**Vérification** : tous les tests passent. Capture du résumé (pass/fail/skip).
**Échec bloquant** : tout test en échec stoppe le workflow.

### Étape 4 — Bundle VSX

```powershell
npm run bundle
```

**Vérification** : `out/extension.js` est généré/mis à jour. Aucune erreur esbuild.
**Sortie** : le bundle remplace le répertoire `out/` existant.

### Étape 5 — Package VSIX

```powershell
npx vsce package --no-yarn
```

**Vérification** : un fichier `.vsix` est créé dans la racine du repo.
**Contrôle taille** : le `.vsix` doit être < 1 Mo (sinon signaler).

### Étape 6 — Rapport

Le rapport d'exécution contient :

| Étape | Commande | Statut | Durée |
|-------|----------|--------|-------|
| 1 | `npm run compile:src` | `OK` / `FAIL` | `Xs` |
| 2 | `npm run compile` | `OK` / `FAIL` | `Xs` |
| 3 | `npx jest --no-coverage` | `OK` / `FAIL` | `Xs` |
| 4 | `npm run bundle` | `OK` / `FAIL` | `Xs` |
| 5 | `npx vsce package --no-yarn` | `OK` / `FAIL` | `Xs` |

**Verdict final** :
- `PASS` : toutes les étapes OK
- `FAIL` : au moins une étape en échec

## Anti-patterns bloquants
- Exécuter `npm run bundle` sans avoir compilé au préalable
- Ignorer les erreurs `compile:src` et poursuivre vers `bundle`
- Lancer `vsce package` sans vérifier la taille du `.vsix`
- Oublier de capturer les durées pour le rapport

## Formats HADMG (intégrés)

### Checkpoint de session

Format JSON à créer après chaque vérification opérationnelle :

```json
{
  "version": "1.0",
  "timestamp": "ISO8601",
  "session_id": "uuid",
  "mode": "real|plan|simulation",
  "identity": "0x...",
  "state": {
    "last_action": "...",
    "pending_actions": [],
    "completed_actions": []
  },
  "verifications": [
    {
      "command": "...",
      "expected": true,
      "actual": true,
      "status": "passed",
      "timestamp": "ISO8601"
    }
  ]
}
```

### Format de note standard

Template YAML frontmatter + sections pour les notes de travail :

```markdown
---
id: UUID v4
type: [project|goal|health|finance|idea|resource|proof|citizen|skill]
domain: [professional|personal|health|finance|learning|creative]
status: [draft|active|paused|completed|archived]
priority: [P0|P1|P2|P3]
created: ISO8601
updated: ISO8601
version: semver
mode: [real|plan|simulation]
verification_status: [pending|passed|failed]
---

# [TITLE]

## 📋 SUMMARY
## 🎯 SUCCESS CRITERIA
## 📊 METRICS
## 🧩 MILESTONES
## 📝 DECISIONS
## 🔗 DEPENDENCIES
## ⚠️ BLOCKERS
## ✅ NEXT ACTIONS
## 🔍 VERIFICATIONS (R16)
## 📎 SOURCES
## 🏷️ TAGS
## 📜 HISTORY
```

## Intégration
- Ce skill s'exécute **après** `session-boot-sequence` (BOOT-1 → BOOT-4).
- Il s'exécute **avant** `pr-lifecycle-gate` et `session-closeout`.
- Il peut être invoqué en standalone pour vérification rapide.
- Il applique le **format HADMG** : checkpoint JSON + notes standardisées.

## Référence ADR
- **ADR** : ADR-2026-08-09-PSL-PIANO-DIFF-Q243
- **IntentHash** : `0xPRD_MOC_OPERATIONAL_SKILLS_DEPENDENCIES_20260811`
- **Dépôt** : gerivdb/GeriCode
- **Statut ADR** : proposed
