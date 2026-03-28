---
name: template-render
description: Skill for rendering dynamic templates for CVs, cover letters, and recruitment documents
triggers:
  - template
  - render
  - cv
  - cover-letter
  - document-generation
  - recruitment
domain: recruitment
version: "1.0.0"
author: gerivdb
license: MIT
status: active
created: 2026-03-28
updated: 2026-03-28
tags:
  - template
  - render
  - cv
  - cover-letter
  - document-generation
  - recruitment
  - markdown
phi_weight: 0.005
biz_domains:
  - BIZ-RECRUIT
  - BIZ-BOOKING
---

# Template Render — Génération de Documents de Recrutement

## Description

Ce skill domaine rend des templates dynamiques pour les CV, lettres de motivation et documents de recrutement. Il utilise Jinja2 pour la génération, supporte plusieurs formats de sortie et permet la personnalisation avancée.

## Usage

```
Quand [génération de CV] OU [création de lettre de motivation] OU [rendu de template recrutement]
→ Appliquer template-render pour:
  1. Charger les templates de documents
  2. Injecter les données candidat
  3. Personnaliser le contenu selon le poste
  4. Générer en Markdown/HTML/PDF
  5. Valider la cohérence du document
```

## Composants

### 1. TemplateRenderer

```python
class TemplateRenderer:
    """Renderer principal de templates"""
    
    def __init__(self, config: TemplateConfig):
        self.config = config
        self.env = Environment(loader=FileSystemLoader(config.template_dir))
    
    def render(self, template_name: str, context: dict) -> str:
        """Rend un template avec le contexte"""
```

### 2. CVGenerator

```python
class CVGenerator:
    """Générateur de CV personnalisés"""
    
    def __init__(self, config: CVConfig):
        self.config = config
        self.renderer = TemplateRenderer(config.template)
    
    def generate(self, candidate: CandidateProfile, job: JobOffer) -> str:
        """Génère un CV personnalisé pour un poste"""
```

### 3. CoverLetterGenerator

```python
class CoverLetterGenerator:
    """Générateur de lettres de motivation"""
    
    def __init__(self, config: CoverLetterConfig):
        self.config = config
        self.renderer = TemplateRenderer(config.template)
    
    def generate(self, candidate: CandidateProfile, job: JobOffer) -> str:
        """Génère une lettre de motivation personnalisée"""
```

### 4. DocumentValidator

```python
class DocumentValidator:
    """Validateur de documents générés"""
    
    def __init__(self, config: ValidationConfig):
        self.config = config
    
    def validate(self, document: str) -> ValidationResult:
        """Valide la cohérence et complétude du document"""
```

## BIZ Domains

- **BIZ-RECRUIT (CANDIDATOR)**: Usage principal pour la génération de CV et lettres de motivation
- **BIZ-BOOKING (GERIBOOKING)**: Génération de documents de confirmation de réservation

## Exemples

### Exemple 1: Génération CV Personnalisé

**Input:**
```python
generator = CVGenerator(config)
cv = generator.generate(
    candidate=CandidateProfile(
        name="Jean Dupont",
        title="Développeur Python Senior",
        skills=["Python", "Django", "PostgreSQL"],
        experiences=[...]
    ),
    job=JobOffer(
        title="Développeur Python",
        company="TechCorp",
        requirements=["Python", "API REST", "Docker"]
    )
)
```

**Output:**
```markdown
# Jean Dupont
## Développeur Python Senior

### Compétences
- Python (Expert)
- Django (Avancé)
- PostgreSQL (Avancé)
- Docker (Intermédiaire)

### Expérience
**Développeur Python Senior** - StartupAI (2020-2024)
- Développement d'API REST avec Django REST Framework
- Optimisation de requêtes PostgreSQL
- Mise en place de CI/CD avec Docker
```

### Exemple 2: Lettre de Motivation

**Input:**
```python
generator = CoverLetterGenerator(config)
letter = generator.generate(
    candidate=candidate_profile,
    job=job_offer
)
```

**Output:**
```markdown
# Lettre de Motivation

Madame, Monsieur,

Je vous adresse ma candidature pour le poste de Développeur Python
au sein de TechCorp. Fort de 4 ans d'expérience en développement Python,
je suis particulièrement intéressé par votre projet de plateforme SaaS.

Mon expérience chez StartupAI m'a permis de développer des compétences
solides en Django et en optimisation de bases de données PostgreSQL,
des compétences directement applicables à votre poste.

Je serais ravi de discuter de ma candidature lors d'un entretien.

Cordialement,
Jean Dupont
```

## Dépendances

### Dépend de
- Aucun

### Requis par
- `recruitment` (domain)

## Intégration

### CANDIDATOR
```python
from skills.template_render import CVGenerator, CoverLetterGenerator, TemplateConfig

config = TemplateConfig(
    template_dir="./templates/recruitment",
    output_format="markdown",
    validate=True
)

cv_generator = CVGenerator(config)
letter_generator = CoverLetterGenerator(config)

# Génération pour une candidature
cv = cv_generator.generate(candidate, job)
letter = letter_generator.generate(candidate, job)
```

### GERIBOOKING
```python
# Génération de confirmation de réservation
from skills.template_render import TemplateRenderer

renderer = TemplateRenderer(config)
confirmation = renderer.render(
    template_name="booking_confirmation.md",
    context={
        "customer_name": customer.name,
        "booking_date": booking.date,
        "service": booking.service
    }
)
```

## Configuration

```yaml
template_render:
  templates:
    directory: ./templates/recruitment
    cv: cv_template.md
    cover_letter: cover_letter_template.md
  
  output:
    format: markdown
    validate: true
    include_metadata: true
  
  personalization:
    match_skills: true
    highlight_relevant: true
    customize_summary: true
  
  validation:
    check_completeness: true
    check_consistency: true
    max_length: 2000
```

## Métriques

- **Temps de génération**: < 1s par document
- **Personnalisation**: 95% de pertinence
- **Validation**: 100% des documents validés
- **Formats supportés**: Markdown, HTML, PDF

## Changelog

- 1.0.0 (2026-03-28) - Version initiale

---

*Skill domaine gerivdb · Part du registre SKILLS ecosystem-1*
