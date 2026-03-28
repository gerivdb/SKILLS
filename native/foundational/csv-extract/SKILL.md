---
id: csv-extract
label: CSV Extract Skill
family: foundational
rank: F0
biz_domains: ["BIZ-FINANCE", "BIZ-GENEALOGY"]
owner: BIZ-2
ref: ISI-20260328-CSVEXTRACT
phi_weight: 0.005
rgpd_note: "CSV peut contenir des données personnelles (IBAN, noms) — valider la source avant ingestion"
---

# CSVExtractSkill

Extraction, parsing et normalisation de fichiers CSV avec détection automatique de délimiteurs et d'encodages.

## Usage

```python
from skills.foundational.csv_extract import CSVExtractSkill
extractor = CSVExtractSkill()
df = extractor.load("transactions.csv", schema={"amount": float, "date": "ISO8601"})
```

## Champs requis

| Champ | Type | Description |
|-------|------|-------------|
| `path` | str | Chemin ou URL du fichier CSV |
| `schema` | dict | Schéma de validation optionnel |
| `encoding` | str | Encodage (défaut: auto-detect) |

## Consommateurs

- `BIZ-FINANCE` (owner) — import relevés bancaires, exports comptables
- `BIZ-GENEALOGY` (consumer) — import listes d'actes, exports GEDCOM tabulaires
