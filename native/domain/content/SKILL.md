---
name: content
description: Génération de contenu intelligent pour marketing et communication
triggers:
  - content
  - generation
  - writing
  - copy
  -文案
  - rédaction
domain: content
version: "1.0.0"
author: gerivdb
license: MIT
status: active
created: 2026-03-17
updated: 2026-03-17
tags:
  - content
  - generation
  - marketing
  - copywriting
phi_weight: 0.005
deps:
  - product-context
  - ecosystem-principles
---

# Content — Génération de Contenu

## Description

Ce skill domaine gère la génération de contenu intelligent pour le marketing et la communication. Il est utilisé par FLUENCE et BRAIN pour créer des contenus variés.

## Fonctionnalités

### 1. Copy Generator

```python
def generate_copy(
    type: ContentType,
    context: ContentContext,
    tone: Tone
) -> Content:
    """
    Génère du copy marketing:
    - Headlines
    - Descriptions
    - CTAs
    - Emails
    """
```

### 2. Blog Post Writer

```python
def write_blog_post(
    topic: str,
    keywords: list[str],
    length: int
) -> BlogPost:
    """
    Rédige un article de blog:
    - Structure SEO
    - Contenu优化
    - Meta description
    """
```

### 3. Social Media Manager

```python
def create_social_post(
    platform: Platform,
    content_type: SocialType,
    context: dict
) -> SocialPost:
    """
    Crée un post réseaux sociaux:
    - Twitter/X
    - LinkedIn
    - Instagram
    """
```

## Usage

```
Quand [besoin de contenu]
→ Définir type (copy/blog/social)
→ Analyser contexte (product-context)
→ Appliquer principes (ecosystem-principles)
→ Générer contenu
→ Valider qualité
```

## Exemples

### Exemple 1: Email Commercial

**Input:**
```
Type: Cold email
Produit: CRM Startup
Audience: CTO Startup Series A
```

**Output:**
```
Subject: Centralisez vos clients dès le jour 1

Bonjour,

Félicitations pour votre levée! 🎉

75% des startups perdent des leads faute de suivi...
[body]

Découvrez comment [Product] peut vous aider →
```

### Exemple 2: LinkedIn Post

**Input:**
```
Type: Thought leadership
Topic: AI in sales
Length: Court
```

**Output:**
```
🚀 L'IA va-t-elle remplacer les commerciaux?

Après 100+ démos, voici mon avis 👇

1/ Le relationnel reste irremplaçable
2/ L'IA optimise, ne remplace pas
3/ La clé: Augmenter le temps humain

What's your take?
#Sales #AI #Startup
```

## Dépendances

### Dépend de
- `product-context` - Pour adapter au persona
- `ecosystem-principles` - Pour qualité DRY/KISS

### Requis par
- FLUENCE
- BRAIN

## Intégration

### FLUENCE
```python
from skills.content import (
    generate_copy,
    write_blog_post,
    create_social_post
)

# Usage
email = generate_copy(
    type="cold_email",
    context=product_context.analyze(crm_startup),
    tone="professional"
)
```

### BRAIN (Semantic Analysis)
```python
from skills.content import validate_quality

# Validation qualité
quality = validate_quality(generated_content)
# → {score: 0.85, issues: [], suggestions: [...]}
```

## Configuration

```yaml
content:
  types:
    - email
    - blog
    - social
    - landing
    - ad
  
  tones:
    - professional
    - casual
    - friendly
    - urgent
  
  languages:
    - fr
    - en
    - es
    - de
  
  seo:
    keywords_required: true
    meta_description: true
    readability_min: 60
```

## Templates

### Email Templates
```
welcome_email
newsletter
product_launch
re_engagement
follow_up
```

### Social Templates
```
announcement
thought_leadership
behind_scenes
testimonial
```

## Changelog

- 1.0.0 (2026-03-17) - Version initiale

---

*Skill domaine gerivdb · Part du registre SKILLS ecosystem-1*
