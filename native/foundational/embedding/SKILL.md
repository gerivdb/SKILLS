---
id: embedding
label: Embedding Skill
family: foundational
rank: F0
biz_domains: ["BIZ-FINANCE", "BIZ-GENEALOGY"]
owner: BIZ-2
ref: ISI-20260328-EMBEDDING
phi_weight: 0.005
rgpd_note: "Embeddings may encode personal data — anonymise input when processing PII"
---

# EmbeddingSkill

Génère des vecteurs d'embedding à partir de texte brut via un modèle local (Ollama) ou distant.

## Usage

```python
from skills.foundational.embedding import EmbeddingSkill
emb = EmbeddingSkill(model="nomic-embed-text")
vector = emb.encode("Texte à encoder")
```

## Champs requis

| Champ | Type | Description |
|-------|------|-------------|
| `model` | str | Modèle d'embedding (défaut: `nomic-embed-text`) |
| `text` | str | Texte à encoder |

## Consommateurs

- `BIZ-FINANCE` (owner) — scoring transactions, détection anomalies
- `BIZ-GENEALOGY` (consumer) — recherche sémantique arbres généalogiques

> ⚠️ **Anti-duplication** : ce stub est le seul owner de EmbeddingSkill dans SKILLS.
> BIZ-3 (racines) consomme ce fichier par référence — ne pas créer de doublon.
