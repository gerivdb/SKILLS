---
id: semantic-search
label: Semantic Search Skill
family: foundational
rank: F0
biz_domains: ["BIZ-RECRUIT", "BIZ-GENEALOGY", "BIZ-DEV"]
owner: BIZ-1
ref: ISI-20260328-SEMANTICSEARCH
phi_weight: 0.005
rgpd_note: "Index peut contenir des noms de personnes — chiffrement au repos recommandé"
---

# SemanticSearchSkill

Recherche sémantique par similarité cosinus sur des corpus indexés.
Classifié **Foundational** : utilisé dans ≥3 domaines BIZ-* (RECRUIT + GENEALOGY + DEV).

## Usage

```python
from skills.foundational.semantic_search import SemanticSearchSkill
search = SemanticSearchSkill(index="candidates")
results = search.query("développeur Python senior Paris", top_k=10)
```

## Champs requis

| Champ | Type | Description |
|-------|------|-------------|
| `index` | str | Nom de l'index vectoriel |
| `query` | str | Requête en langage naturel |
| `top_k` | int | Nombre de résultats (défaut: 10) |

## Consommateurs

- `BIZ-RECRUIT` (owner) — matching CV/offres
- `BIZ-GENEALOGY` (consumer) — recherche d'ancêtres par description
- `BIZ-DEV` (consumer) — recherche dans documentation technique

## Dépendance

Requiert `EmbeddingSkill` pour la vectorisation des requêtes.
