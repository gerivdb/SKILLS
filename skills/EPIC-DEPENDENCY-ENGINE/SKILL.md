# Skill: EPIC-DEPENDENCY-ENGINE

## Contexte
Les EPICs forment un DAG de dépendances. Marquer un enfant `active`/`completed` alors que son parent est `planned` casse la cohérence du plan et expose à des exécutions prématurées.

## Règle
Avant toute mise à jour de statut d’un EPIC :
1. Lire le champ `parent_epic` (si présent)
2. Lire le parent et vérifier son `status`
3. Si parent != `completed` → refuser la mise à jour, émettre WAL `EPIC_DEPENDENCY_BLOCKED`
4. Si orphelin (pas de `parent_epic`) mais dépendances implicites détectées → alerter
5. Si tous les parents sont `completed` → autoriser la mise à jour

## Détection des orphelins
- EPIC avec `depends_on` implicite dans le résumé mais sans `parent_epic` déclaré
- EPIC enfant sans parent dans l’INDEX
- EPIC coordonnateur sans enfants déclarés

## Rapport
Générer `.kilo/epic-dependencies/EPIC_DAG.yaml` :
- `nodes` : liste des EPICs avec `id`, `status`, `parent_epic`
- `edges` : liste des dépendances `parent -> child`
- `blocked` : liste des EPICs bloqués avec raison
- `orphans` : liste des EPICs sans parent mais avec dépendances implicites

## Anti-pattern interdit
- Marquer `completed` sans vérifier les parents
- Créer un EPIC enfant sans déclarer `parent_epic`
- Ignorer un blocage et forcer le statut

## Exemple d'application
```
EPIC : diffscope-fork Phase B (BUILD)
→ parent_epic : EPIC-2026-06-05-A-DIFFSCOPE-FORK-PREP
→ parent status : completed
→ Autorisation : Phase B peut passer active/completed
---
EPIC : diffscope-fork Phase A (PREP)
→ Aucun parent déclaré
→ Résumé mentionne "Phase A bloquante pour B"
→ Détection orphelin → alerte pour ajouter parent_epic si nécessaire
```
