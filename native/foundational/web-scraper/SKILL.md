---
id: web-scraper
label: Web Scraper Skill
family: foundational
rank: F0
biz_domains: ["BIZ-GENEALOGY", "BIZ-FINANCE", "BIZ-RECRUIT"]
owner: BIZ-3
ref: ISI-20260328-WEBSCRAPER
phi_weight: 0.005
rgpd_note: "Scraping de personnes vivantes interdit sans consentement — vérifier robots.txt et CGU"
alive_check_required: false
---

# WebScraperSkill

Extraction structurée de contenus web (HTML, JSON-LD, tableaux). Supporte Playwright pour le JS rendu côté client.
Classifié **Foundational** : utilisé dans ≥3 domaines BIZ-* (GENEALOGY + FINANCE + RECRUIT).

## Usage

```python
from skills.foundational.web_scraper import WebScraperSkill
scraper = WebScraperSkill(engine="playwright")
data = scraper.extract(url="https://source.example.com", selector="table.results")
```

## Champs requis

| Champ | Type | Description |
|-------|------|-------------|
| `url` | str | URL cible |
| `selector` | str | Sélecteur CSS ou XPath |
| `engine` | str | `requests` \| `playwright` \| `bs4` |

## Consommateurs

- `BIZ-GENEALOGY` (owner) — scraping archives, actes d'état civil
- `BIZ-FINANCE` (consumer) — scraping cours, données de marché
- `BIZ-RECRUIT` (consumer) — scraping offres d'emploi, profils publics

> ⚠️ Pour tout usage `BIZ-GENEALOGY` : combiner avec `alive-check` skill pour les personnes vivantes.
