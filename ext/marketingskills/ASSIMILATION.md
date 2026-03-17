# ASSIMILATION — marketingskills → ecosystem-1

**Source** : `coreyhaines31/marketingskills`  
**Date** : 2026-03-17  
**Status** : Pending (Q2 2026)

## Vue d'Ensemble

Ce document documente le processus d'assimilation des skills marketing de `coreyhaines31/marketingskills` dans ecosystem-1.

## Source

| Attribut | Valeur |
|----------|--------|
| Repository | github.com/coreyhaines31/marketingskills |
| Licence | MIT |
| Stars | ~500 |
| Dernier commit | Actif |
| Langage | JavaScript/TypeScript |

## Skills Identifiés

Le repository source contient 8 skills marketing :

| # | Skill Original | Description | Mapping Ecosystem-1 | Status |
|---|----------------|-------------|---------------------|--------|
| 1 | `email-campaign` | Création de campagnes email | → `content` (native) | ✓ Mappé |
| 2 | `social-post` | Posts réseaux sociaux | → `content` (native) | ✓ Mappé |
| 3 | `ad-copy` | Rédaction publicitaire | → `content` (native) | ✓ Mappé |
| 4 | `landing-page` | Pages de destination | → `content` (native) | ✓ Mappé |
| 5 | `seo-analysis` | Analyse SEO | → `product-context` | ⚠ Gap |
| 6 | `market-research` | Étude de marché | → `product-context` | ⚠ Gap |
| 7 | `cold-outreach` | Prospection froide | → `content` | ⚠ Gap |
| 8 | `brand-voice` | Identité de marque | → `product-context` | ⚠ Gap |

## Mapping Détaillé

### Skills Complets (0 gaps)

#### 1. email-campaign → content

```javascript
// Source
import { createCampaign } from 'marketingskills/email'

// Ecosystem-1
import { generate_copy } from 'skills/content'
// Type: email, context: cold_email
```

**Adaptations** :
- Intégration dans le template `content` native
- Adaptation du format d'entrée

#### 2. social-post → content

**Mapping** :
- Twitter → platform: twitter
- LinkedIn → platform: linkedin
- Instagram → platform: instagram

#### 3. ad-copy → content

**Mapping** :
- Google Ads → type: google_ads
- Facebook Ads → type: facebook_ads

#### 4. landing-page → content

**Mapping** :
- Structure complète via `content` + `product-context`

### Skills avec Gaps (4)

| Skill | Gap Identifié | Solution Proposée |
|-------|---------------|-------------------|
| `seo-analysis` | Pas de skill natif equivalent | Créer `native/marketing/seo-analysis` |
| `market-research` | Pas de skill natif | Créer `native/marketing/market-research` |
| `cold-outreach` | Templates manquants | Enrichir `content` |
| `brand-voice` | Framework absent | Créer `native/marketing/brand-voice` |

## Plan d'Assimilation

### Phase 1 (Q2 2026) : Intégration

- [ ] Configurer submodule
- [ ] Mapper 4 skills complets
- [ ] Documenter dans REGISTRY.yaml

### Phase 2 (Q3 2026) : Enrichissement

- [ ] Créer skill `seo-analysis`
- [ ] Créer skill `market-research`
- [ ] Enrichir `cold-outreach` templates

### Phase 3 (Q4 2026) : Maturité

- [ ] Créer skill `brand-voice`
- [ ] Migration complète vers native
- [ ] Déprécier reference submodule

## Différences Clés

| Aspect | marketingskills | ecosystem-1 |
|--------|-----------------|--------------|
| Architecture | Monorepo | Registry distribué |
| Skills | Import direct | Declarative registry |
| Validation | Tests unitaires | CI + φ-CPS |
| Governance | Minimal | L2/L3 |

## Actions Requises

### Immediate

- [ ] Finaliser configuration submodule
- [ ] Valider licence MIT
- [ ] Tester compatibilité

### Court Terme

- [ ] Créer skills gap
- [ ] Migration content
- [ ] Tests d'intégration

## Conclusion

L'assimilation de `marketingskills` est **highly beneficial** pour ecosystem-1 :
- ✓ 4 skills可以直接 mapper
- ⚠ 4 skills nécessitent création
- ✓ License compatible MIT

**Recommandation** : Procéder à l'assimilation complète.

---

*Document généré par skills-registry · Part du registre SKILLS ecosystem-1*
