# Skill: EPIC-DEPENDENCY-ENGINE

## Contexte
Les EPICs forment un DAG de dependances. Marquer un enfant `active`/`completed` alors que son parent est `planned` casse la coherence du plan et expose a des executions prematurees.

## Regle
Avant toute mise a jour de statut d'un EPIC :
1. Lire le champ `parent_epic` (si present)
2. Lire le parent et verifier son `status`
3. Si parent != `completed` -> refuser la mise a jour, emettre WAL `EPIC_DEPENDENCY_BLOCKED`
4. Si orphelin (pas de `parent_epic`) mais dependances implicites detectees -> alerter
5. Si tous les parents sont `completed` -> autoriser la mise a jour

## Detection des orphelins
- EPIC avec `depends_on` implicite dans le resume mais sans `parent_epic` declare
- EPIC enfant sans parent dans l'INDEX
- EPIC coordonnateur sans enfants declares

## Rapport
Generer `.kilo/epic-dependencies/EPIC_DAG.yaml` :
- `nodes` : liste des EPICs avec `id`, `status`, `parent_epic`
- `edges` : liste des dependances `parent -> child`
- `blocked` : liste des EPICs bloques avec raison
- `orphans` : liste des EPICs sans parent mais avec dependances implicites

## Anti-pattern interdit
- Marquer `completed` sans verifier les parents
- Creer un EPIC enfant sans declarer `parent_epic`
- Ignorer un blocage et forcer le statut

## Exemple d'application
```
EPIC : diffscope-fork Phase B (BUILD)
-> parent_epic : EPIC-2026-06-05-A-DIFFSCOPE-FORK-PREP
-> parent status : completed
-> Autorisation : Phase B peut passer active/completed
---
EPIC : diffscope-fork Phase A (PREP)
-> Aucun parent declare
-> Resume mentionne "Phase A bloquante pour B"
-> Detection orphelin -> alerte pour ajouter parent_epic si necessaire
```
