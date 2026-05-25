---
name: claude-optimizer
description: "18-step Claude optimization, custom instructions, projects, style cloning. Use when user mentions 'optimisation Claude', '18 étapes', 'custom instructions'."
---
|
# Claude Optimizer

## Domaine et périmètre

Ce skill couvre l'**optimisation de Claude** (Anthropic) via les 18 étapes connues :
- Custom Instructions (personnalité, style, ton)
- Projects (contexte persistant, fichiers de référence)
- Style cloning (reproduction d'un style d'écriture existant)
- Optimisation des prompts pour l'écosystème gerivdb

## Méthodologie

### Phase 1 : Audit de la configuration actuelle
- Vérifier les Custom Instructions existantes (Settings → Personalization).
- Lister les Projects actifs et leurs fichiers de contexte.
- Évaluer la cohérence du style avec la charte NEXUS.

### Phase 2 : Optimisation
- Appliquer les 18 étapes d'optimisation (personnalité, format, contraintes, exemples).
- Configurer les Custom Instructions pour le contexte gerivdb (terminologie, conventions).
- Créer/mettre à jour les Projects avec les fichiers de référence (ADR, PRD, ONTOLOGY).

### Phase 3 : Validation
- Tester les réponses de Claude sur des cas types.
- Ajuster les instructions incohérentes.
- Documenter la configuration finale.

## Règles de décision
- **Règle 1** : Les Custom Instructions doivent mentionner la terminologie NEXUS (IntentHash, φ-CPS, ECOS_ROOT).
- **Règle 2** : Chaque Project doit inclure les fichiers de contexte pertinents (max 10 fichiers).
- **Règle 3** : Le style de sortie doit être technique, direct, sans apologie ni remplissage.

## Format de sortie

```markdown
## Configuration Claude
- Custom Instructions : [résumé]
- Projects actifs : [liste]
- Fichiers de contexte : [liste]
- Score d'optimisation : [N]/18 étapes appliquées
```

## Exemples d'utilisation
- "Optimise Claude pour l'écosystème gerivdb" → Appliquer les 18 étapes.
- "Crée un Project pour NEXUS" → Configurer le contexte persistant.
- "Clone le style des ADR existants" → Analyser et reproduire.

## Intégration avec l'écosystème
- Dépôts concernés : NEXUS, ONTOLOGY, BRAIN
- Couche EECS : L5_META
- Tags NEXUS : [CONFORME_NEXUS]
