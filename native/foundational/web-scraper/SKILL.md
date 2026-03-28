---
name: web-scraper
description: Skill for extracting structured data from websites and web pages
triggers:
  - web-scraper
  - scraping
  - extraction
  - web
  - data-collection
  - crawling
domain: foundational
version: "1.0.0"
author: gerivdb
license: MIT
status: active
created: 2026-03-28
updated: 2026-03-28
tags:
  - web-scraper
  - scraping
  - extraction
  - web
  - data-collection
  - crawling
  - automation
phi_weight: 0.005
biz_domains:
  - BIZ-FINANCE
  - BIZ-RECRUIT
  - BIZ-MEDIA
---

# Web Scraper — Extraction de Données Web

## Description

Ce skill fondamental extrait des données structurées depuis des sites web et des pages web. Il parse le HTML, gère le JavaScript, respecte les robots.txt et exporte les données dans différents formats.

## Usage

```
Quand [extraction de données web] OU [scraping de sites] OU [collecte d'informations en ligne]
→ Appliquer web-scraper pour:
  1. Analyser la structure HTML des pages
  2. Extraire les données avec sélecteurs CSS/XPath
  3. Gérer le contenu JavaScript (headless browser)
  4. Respecter les politiques robots.txt
  5. Exporter en JSON/CSV/Database
```

## Composants

### 1. WebScraper

```python
class WebScraper:
    """Scraper principal pour extraction web"""
    
    def __init__(self, config: ScraperConfig):
        self.config = config
        self.session = requests.Session()
        self.browser = None
    
    def scrape(self, url: str, selectors: dict) -> dict:
        """Scrape une page web avec les sélecteurs donnés"""
```

### 2. HTMLParser

```python
def parse_html(html: str, selectors: dict) -> dict:
    """Parse le HTML avec BeautifulSoup"""
    # Extraction avec sélecteurs CSS
```

### 3. JavaScriptRenderer

```python
class JavaScriptRenderer:
    """Rendu JavaScript pour contenu dynamique"""
    
    def __init__(self, headless: bool = True):
        self.browser = launch_browser(headless=headless)
    
    def render(self, url: str) -> str:
        """Rendu JavaScript d'une page"""
```

### 4. RateLimiter

```python
class RateLimiter:
    """Limiteur de requêtes pour respecter les sites"""
    
    def __init__(self, requests_per_second: float = 1.0):
        self.delay = 1.0 / requests_per_second
        self.last_request = 0
    
    def wait(self):
        """Attend entre les requêtes"""
```

## BIZ Domains

- **BIZ-FINANCE (BANK-BUSTER)**: Extraction de données financières et cours de marché
- **BIZ-RECRUIT (CANDIDATOR)**: Scraping d'offres d'emploi et profils LinkedIn
- **BIZ-MEDIA (FLUENCE)**: Collecte de contenu et articles pour génération

## Exemples

### Exemple 1: Scraping Offres d'Emploi

**Input:**
```python
scraper = WebScraper(config)
selectors = {
    "title": "h1.job-title",
    "company": "span.company-name",
    "location": "div.location",
    "description": "div.job-description"
}
data = scraper.scrape("https://example.com/jobs/123", selectors)
```

**Output:**
```json
{
  "url": "https://example.com/jobs/123",
  "title": "Développeur Python Senior",
  "company": "TechCorp",
  "location": "Paris, France",
  "description": "Nous recherchons un développeur Python...",
  "scraped_at": "2026-03-28T10:30:00Z"
}
```

### Exemple 2: Scraping avec JavaScript

**Input:**
```python
renderer = JavaScriptRenderer(headless=True)
html = renderer.render("https://example.com/dynamic")
data = parse_html(html, selectors)
```

**Output:**
```
Page rendue avec succès:
- 15 éléments extraits
- Contenu JavaScript chargé
- Temps de rendu: 2.3s
```

## Dépendances

### Dépend de
- Aucun (skill fondateur)

### Requis par
- `semantic-search` (pour indexation de contenu web)
- `recruitment` (domain)
- `content` (domain)

## Intégration

### CANDIDATOR
```python
from skills.web_scraper import WebScraper, ScraperConfig

config = ScraperConfig(
    user_agent="CANDIDATOR/1.0",
    respect_robots=True,
    rate_limit=2.0
)
scraper = WebScraper(config)

# Scraping d'offres d'emploi
jobs = scraper.scrape_listings("https://linkedin.com/jobs", max_pages=5)
```

### FLUENCE
```python
# Collecte de contenu pour génération
scraper = WebScraper(config)
articles = scraper.scrape_articles(
    urls=["https://news.example.com/tech"],
    selectors={"title": "h1", "content": "article"}
)
```

## Configuration

```yaml
web_scraper:
  user_agent: "SKILLS-WebScraper/1.0"
  respect_robots: true
  rate_limit: 1.0  # requêtes par seconde
  
  browser:
    headless: true
    timeout: 30
    wait_for: "networkidle"
  
  storage:
    format: json
    include_metadata: true
    deduplication: true
```

## Métriques

- **Temps de scraping**: < 5s par page
- **Extraction HTML**: 1000 éléments/seconde
- **Rendu JavaScript**: 2-5s par page
- **Respect robots.txt**: 100%

## Changelog

- 1.0.0 (2026-03-28) - Version initiale

---

*Skill fondamental gerivdb · Part du registre SKILLS ecosystem-1*
