---
name: skill-tester
description: "Skill testing, validation, trigger verification, matrix. Use when user mentions 'test skill', 'validation', 'déclenchement', 'matrice'."
version: "1.0.0"
changelog:
  - {v: "1.0.0", date: "2026-05-30", notes: "Version initiale"}
triggers: []
layer: "L0_UNKNOWN"
nexusTags: ["CONFORME_NEXUS"]
trit_primitive: TritRunTests
---
# Skill Tester

## Domaine et périmètre

Ce skill couvre le **test et la validation des skills** Perplexity :
- Vérification de la syntaxe (frontmatter YAML, `|`, structure Markdown)
- Test de déclenchement (les bons mots-clés activent-ils le bon skill ?)
- Matrice de test (couverture des cas : trigger, non-trigger, edge cases)
- Validation du contenu (le skill produit-il des réponses actionnables ?)

## Méthodologie

### Phase 1 : Test syntaxique
- Vérifier la présence du `|` après le second `---`.
- Valider le YAML frontmatter (name, description).
- Vérifier l'indentation Markdown (pas de code blocks involontaires).

### Phase 2 : Test de déclenchement
- Pour chaque mot-clé de la description, tester si le skill s'active.
- Tester les non-triggers (mots-clés qui ne doivent PAS activer le skill).
- Documenter les faux positifs et faux négatifs.

### Phase 3 : Test de contenu
- Évaluer la qualité des réponses produites.
- Vérifier que les règles de décision sont appliquées.
- Valider les formats de sortie.

## Règles de décision
- **Règle 1** : Un skill sans `|` est rejeté — test bloquant.
- **Règle 2** : Un skill doit se déclencher sur au moins 3 des mots-clés de sa description.
- **Règle 3** : Le contenu générique (template passe-partout) = échec du test de contenu.

## Format de sortie

```markdown
## Rapport de Test — [skill]
- Syntaxe : [OK | ERREUR]
- Déclenchement : [N]/[N] mots-clés OK
- Contenu : [spécifique | générique]
- Verdict : [VALIDE | À_CORRIGER | INVALIDE]
```

## Exemples d'utilisation
- "Teste le skill pruning-explainer" → Vérifier syntaxe + déclenchement.
- "Génère la matrice de test pour tous les skills" → Créer le tableau.
- "Ce skill est-il valide ?" → Test complet.

## Intégration avec l'écosystème
- Dépôts concernés : tous les skills Perplexity
- Couche EECS : L5_META
- Tags NEXUS : [CONFORME_NEXUS]
