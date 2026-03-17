# CHANGELOG — Skills Registry

Tous les changements notables de ce projet seront documentés dans ce fichier.

Le format est basé sur [Conventional Commits](https://www.conventionalcommits.org/).

## [1.0.0] - 2026-03-17

### 🎉 Features

- **feat**: Création initiale du dépôt SKILLS
- **feat(registry)**: Ajout du REGISTRY.yaml avec 6 skills initiaux
- **feat(manifest)**: Ajout du MANIFEST.json pour compatibilité agentskills.io
- **feat(taxonomy)**: Définition de la taxonomie des types de skills
- **feat(citizens)**: Création du citoyen skills-registry L2

### 📦 Skills Ajoutés

- **foundational/product-context**: Contextualisation produit/audience
- **foundational/ecosystem-principles**: Principes ONTOLOGY, DRY, KISS, φ-CPS
- **domain/booking**: Orchestration réservation (GERIBOOKING)
- **domain/recruitment**: Matching candidats (CANDIDATOR)
- **domain/finance**: Analyse bancaire (BANK-BUSTER)
- **domain/content**: Génération contenu (FLUENCE + BRAIN)

### 🛠️ Infrastructure

- **ci**: Ajout de `.github/workflows/validate-skills.yml`
- **ci**: Ajout de `.github/workflows/registry-sync.yml`
- **tools**: Ajout de `tools/validate-skills.sh`
- **tools**: Ajout de `tools/registry-gen.py`

### 📚 Documentation

- **docs**: README.md avec présentation du registre
- **docs**: CONTRIBUTING.md avec guide de contribution
- **docs**: TAXONOMY.md avec définitions canoniques
- **docs**: CITIZENS.md avec informations de gouvernance

### 🔗 Intégration

- **integration**: Préparation submodule pour marketingskills
- **integration**: Préparation intégration ECOYSTEM

---

## À Venir

### Prévu pour Q2 2026

- [ ] Assimilation de `coreyhaines31/marketingskills`
- [ ] Intégration submodule dans ECOYSTEM
- [ ] Activation daemon registry-sync
- [ ] Premiere skill consumption par FLUENCE/BRAIN

---

## Guide de Lecture

Le format suit [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### Types

| Type | Description |
|------|-------------|
| `feat` | Nouvelle feature |
| `fix` | Bug fix |
| `docs` | Documentation |
| `ci` | Changes to CI configuration |
| `refactor` | Code refactoring |
| `test` | Tests |
| `chore` | Maintenance |

### Footer

- `IntentHash: <hash>` - Référence l'intent associé
- `Closes #<number>` - Ferme une issue

---

*Généré automatiquement par ecosystem-1 SKILLS registry*
