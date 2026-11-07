---
name: traceability
description: Traçabilité systématique des décisions et des choix. Relie chaque proposition à un besoin identifié, une source documentée, et un indicateur mesurable. Utiliser avant de rédiger un rapport, PRD, ADR ou INTENT.
version: 1.0.0
intent_hash: 0xTRACEABILITY_SKILL_20260809
---

# Traceability — Skill KiloCode

## Objectif

Garantir que toute proposition, recommandation ou décision est rattachée à :
1. Un **besoin** identifié (utilisateur, système, contrainte)
2. Une **source** documentée (PRD, ADR, issue, SOT)
3. Un **indicateur** mesurable (métrique, seuil, test)

Évite les propositions "flottantes" non justifiées.

## Déclencheur

Avant toute rédaction de :
- Rapport d'ingénierie
- PRD / MOC
- ADR
- INTENT
- Proposition de nouveau composant
- Sélection de technologies / effets / patterns

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `proposals` | array | ✅ | Liste des propositions à tracer |
| `context` | object | ❌ | Contexte additionnel (repo, layer, contraintes) |
| `min_sources` | int | ❌ | Nombre minimum de sources par proposition (défaut: 1) |
| `min_indicators` | int | ❌ | Nombre minimum d'indicateurs par proposition (défaut: 1) |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `traceability_matrix` | array | Matrice [besoin → source → indicateur] pour chaque proposition |
| `gaps` | array | Propositions sans besoin, sans source, ou sans indicateur |
| `score` | float | % de propositions tracées (0.0 - 1.0) |
| `verdict` | enum | `ok` / `warning` / `blocked` |

## Template de Traçabilité

Pour chaque proposition, remplir :

```yaml
proposition:
  id: "PROP-001"
  description: "Implémenter 20 effets core"
  need:
    id: "NEED-042"
    description: "Détection de patterns dégradés dans les logs"
    source: "Issue #42 - Pattern Detection"
    priority: "high"
  source:
    type: "PRD|ADR|ISSUE|SOT|BENCHMARK"
    ref: "PRD-MOC-AGENT-MANAGER-V9.9-2026-08-08.md"
    excerpt: "Section 4.2 - Effets de filtrage"
  indicator:
    metric: "latency_per_effect"
    target: "< 100ms"
    measurement: "pytest benchmark on ENV2"
  evidence:
    - "benchmarks/test_effects.py::test_blur_latency"
    - "benchmarks/test_effects.py::test_glow_latency"
```

## Protocole Obligatoire

### Étape 1 — Identifier les besoins

```
Pour chaque proposition :
  → Quel problème résout-elle ?
  → Pour qui / pour quoi ?
  → Quelle est la priorité ?
```

### Étape 2 — Trouver les sources

```
Pour chaque besoin :
  → Existe-t-il un PRD / ADR / issue qui le documente ?
  → Si non → créer une issue ou un INTENT
  → Si oui → référencer précisément (fichier, section, ligne)
```

### Étape 3 — Définir les indicateurs

```
Pour chaque proposition :
  → Comment mesure-t-on le succès ?
  → Quel est le seuil acceptable ?
  → Comment vérifie-t-on la mesure ?
```

### Étape 4 — Vérifier la couverture

```
→ Toute proposition a un besoin ? (sinon: gap)
→ Toute proposition a une source ? (sinon: gap)
→ Toute proposition a un indicateur ? (sinon: gap)
→ Score = propositions_tracées / propositions_totales
```

## Seuils de Validation

| Score | Verdict | Action |
|-------|---------|--------|
| 1.0 | `ok` | Peut rédiger |
| 0.7 - 0.99 | `warning` | Peut rédiger avec gaps documentés |
| < 0.7 | `blocked` | Ne peut pas rédiger — compléter les gaps |

## Exemple d'Application

**Proposition** : "Implémenter 20 effets core"

| Élément | Valeur |
|---------|--------|
| Besoin | Détection de patterns dégradés (logs, code) |
| Source | Review V9.10-R1 + contraintes ENV2 |
| Indicateur | Latence < 100ms par effet sur Z600 |
| Évidence | Benchmarks pytest sur ENV2 |

## Anti-patterns

- ❌ Proposer sans besoin identifié
- ❌ Proposer sans source documentée
- ❌ Proposer sans indicateur mesurable
- ❌ Dire "c'est utile" sans preuve

## Référence ADR

- **ADR** : ADR-2026-08-09-001-TRACEABILITY-SKILL
- **IntentHash** : 0xTRACEABILITY_SKILL_20260809
- **Dépôt** : gerivdb/GeriCode
