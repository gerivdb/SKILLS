---
name: validation-checklist
description: Checklist de validation systématique avant production de tout document d'ingénierie (PRD, ADR, INTENT, rapport). Vérifie la présence des sections AUDIT, DESIGN, PROPOSITION, VALIDATION et la qualité de leur contenu.
version: 1.0.0
intent_hash: 0xVALIDATION_CHECKLIST_SKILL_20260809
---

# Validation Checklist — Skill KiloCode

## Objectif

Empêcher la production de documents d'ingénierie incomplets ou non justifiés.
Vérifie systématiquement la présence et la qualité de 4 sections : AUDIT, DESIGN, PROPOSITION, VALIDATION.

## Déclencheur

Avant tout :
- Commit d'un PRD / ADR / INTENT / rapport
- Merge vers `main` d'un document d'ingénierie
- Promotion d'un brouillon vers version `proposed`
- Fin de session KiloCode ayant produit un document technique

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `document_path` | string | ✅ | Chemin du document à valider |
| `document_type` | enum | ✅ | `PRD` / `ADR` / `INTENT` / `REPORT` / `DESIGN` |
| `strict_mode` | bool | ❌ | Si true, échoue sur tout warning (défaut: false) |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `passed` | bool | Toutes les sections obligatoires sont présentes et valides |
| `score` | float | % de checks passés (0.0 - 1.0) |
| `missing_sections` | array | Sections obligatoires absentes |
| `warnings` | array | Sections présentes mais incomplètes |
| `blockers` | array | Erreurs critiques empêchant la validation |
| `details` | object | Résultat détaillé par section |

## Checklist par Section

### Section AUDIT — État des Lieux

| Check | Requis | Description |
|-------|--------|-------------|
| AUDIT-01 | ✅ | Section `## 1. AUDIT` ou équivalent présente |
| AUDIT-02 | ✅ | Inventaire des composants existants (repos, modules, services) |
| AUDIT-03 | ✅ | Référence à `known_repositories.yaml` ou SOT équivalente |
| AUDIT-04 | ✅ | Contraintes identifiées (hardware, temps, budget, architecture) |
| AUDIT-05 | ⚠️ | Besoins utilisateurs identifiés et documentés |

**Validation** :
- Si AUDIT-01 à AUDIT-04 passent → `passed: true`
- Si AUDIT-05 échoue → `warning: "Besoins utilisateurs non documentés"`

### Section DESIGN — Cadrage

| Check | Requis | Description |
|-------|--------|-------------|
| DESIGN-01 | ✅ | Section `## 2. DESIGN` ou équivalent présente |
| DESIGN-02 | ✅ | Critères de sélection définis et pondérés |
| DESIGN-03 | ✅ | Options évaluées (au moins 2) avec avantages/inconvénients |
| DESIGN-04 | ✅ | Décision de design justifiée avec sources |
| DESIGN-05 | ⚠️ | Spécifications des modules/composants (entrée, sortie, fonction) |

**Validation** :
- Si DESIGN-01 à DESIGN-04 passent → `passed: true`
- Si DESIGN-05 échoue → `warning: "Spécifications modules manquantes"`

### Section PROPOSITION — Solution

| Check | Requis | Description |
|-------|--------|-------------|
| PROP-01 | ✅ | Section `## 3. PROPOSITION` ou équivalente présente |
| PROP-02 | ✅ | Architecture décrite (diagramme ASCII ou texte) |
| PROP-03 | ✅ | Composants listés avec rôles |
| PROP-04 | ✅ | Spécifications techniques (formats, seuils, contraintes) |
| PROP-05 | ✅ | Planning avec phases et dépendances |

**Validation** :
- Tous les checks sont requis → `passed: true/false`

### Section VALIDATION — Preuves

| Check | Requis | Description |
|-------|--------|-------------|
| VAL-01 | ✅ | Section `## 4. VALIDATION` ou équivalente présente |
| VAL-02 | ✅ | Checklist de validation complétée |
| VAL-03 | ✅ | Métriques de validation définies avec cibles |
| VAL-04 | ✅ | Preuves documentées (benchmarks, tests, issues) |
| VAL-05 | ✅ | Conclusion avec statut final |

**Validation** :
- Tous les checks sont requis → `passed: true/false`

## Scoring

| Section | Poids | Checks |
|---------|-------|--------|
| AUDIT | 25% | 5 checks (4 requis + 1 optionnel) |
| DESIGN | 25% | 5 checks (4 requis + 1 optionnel) |
| PROPOSITION | 25% | 5 checks (tous requis) |
| VALIDATION | 25% | 5 checks (tous requis) |
| **TOTAL** | **100%** | **20 checks** |

## Résultats Possibles

| Score | Verdict | Action |
|-------|---------|--------|
| 1.0 | `passed` | Document valide pour commit/merge |
| 0.8 - 0.99 | `passed_with_warnings` | Document valide, warnings à documenter |
| 0.6 - 0.79 | `failed` | Document incomplet, corriger avant commit |
| < 0.6 | `blocked` | Document bloqué, AUDIT manquant |

## Exemple d'Application

**Document** : `INTENT-V9_10-AE-SPECTRUM-REVIEW-CORRECTION-2026-08-09.md`

| Section | Présente | Checks passés | Score |
|---------|----------|---------------|-------|
| AUDIT | ✅ | 4/5 | 0.8 |
| DESIGN | ✅ | 3/5 | 0.6 |
| PROPOSITION | ✅ | 4/5 | 0.8 |
| VALIDATION | ✅ | 4/5 | 0.8 |
| **TOTAL** | | **15/20** | **0.75** |

**Verdict** : `passed_with_warnings`
**Warnings** :
- DESIGN-05 : Spécifications modules manquantes (ajoutées post-audit)
- AUDIT-05 : Besoins utilisateurs implicites (à formaliser)

## Formats HADMG (intégrés)

### Checklist HADMG

Pour tout document d'ingénierie soumis à validation, vérifier en plus des sections AUDIT/DESIGN/PROPOSITION/VALIDATION :

| Check HADMG | Requis | Description |
|-------------|--------|-------------|
| HADMG-01 | ✅ | Le document possède un frontmatter YAML valide (type, version, date, status, intent_hash) |
| HADMG-02 | ✅ | Le `intent_hash` est présent et formaté `0x...` |
| HADMG-03 | ✅ | Le `status` est valide selon le type de document |
| HADMG-04 | ✅ | Les sections standardisées sont présentes si applicable |
| HADMG-05 | ⚠️ | Le document contient une section de traçabilité (références ADR/PRD/INTENT) |

**Validation HADMG** :
- Si HADMG-01 à HADMG-04 passent → `hadmg_passed: true`
- Si HADMG-05 échoue → `hadmg_warning: "Traçabilité manquante"`

### Format de note standard HADMG

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

### Checkpoint de session HADMG

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

## Intégration Git

Cette checklist peut être ajoutée comme `pre-commit` hook :

```bash
#!/bin/bash
# .git/hooks/pre-commit
python -m skills.validation-checklist.cli --document "$1" --strict
```

## Anti-patterns

- ❌ Publier un document sans section AUDIT
- ❌ Publier un document sans section VALIDATION
- ❌ Dire "c'est évident" au lieu de documenter les sources
- ❌ Oublier les indicateurs mesurables

## Référence ADR

- **ADR** : ADR-2026-08-09-001-VALIDATION-CHECKLIST
- **IntentHash** : 0xVALIDATION_CHECKLIST_SKILL_20260809
- **Dépôt** : gerivdb/GeriCode
