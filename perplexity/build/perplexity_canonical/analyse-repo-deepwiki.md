---
name: analyse-repo-deepwiki
description: Constitutional ECOS analysis of a public GitHub repo via DeepWiki
  + ENV2 scoring + GH issues coverage. Use when user mentions
  "/analyse-repo", "évalue dépôt", "DeepWiki", "scoring ECOS", "citoyennisation".
---
|


# Analyse Repo DeepWiki

## Instructions

1. **Phase 0 – DeepWiki prioritaire** : Interroger `https://deepwiki.com/[owner]/[repo]`. Extraire architecture, modules clés, dépendances, complexité. Si 404, fallback GitHub direct.
2. **Phase 1 – Collecte automatique** : Récupérer README, stars, licence, langage. Rechercher alternatives et usage RAM. Lister les issues ECOS liées.
3. **Phase 2 – Grille scoring ENV2** : Noter de 0 à 5 les critères techniques (sémantique, patterns, compatibilité ENV2 <8 Go RAM), stratégiques (citoyennisation, gap issues, synergie ≥3 repos, souveraineté), et coût (effort, dette). Score global = (A×0.4 + B×0.4 + C×0.2)×10 → /10.
4. **Phase 3 – Couverture GitHub** : État (totale/partielle/absente), recommandation (EPIC/issue/P0/P1/pool/ADR/rien).
5. **Phase 4 – Alternatives** : Tableau comparatif avec stars, compatibilité ENV2, licence, score ECOS.
6. **Générer le YAML de sortie** structuré + tableau d’alternatives + recommandation finale.
7. **Appliquer les tags NEXUS** et citer TOUTE source inline.

## Règles

- Score < 4/10 → recommandation automatique « ignorer/surveiller ».
- ENV2 KO → alternative légère obligatoire.
- Tout fait doit être cité inline `[source:N]`.
- 600–900 mots total.
- Terminer par « **Prêt pour intent magistral → [titre proposé]** ».

## Format

- YAML structuré (DEEPWIKI_ENRICHMENT, REPO_ANALYSE, VALEUR_ECOS, ENV2_COMPLIANCE, COUVERTURE_GH, ALTERNATIVES, RECOMMANDATION_FINALE).
- Tableau des alternatives en Markdown.
- Citations inline obligatoires.

## Exemples

- "[/analyse-repo https://github.com/owner/repo]" → Lancer DeepWiki, scorer, générer le YAML et la recommandation finale.

