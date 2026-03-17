# SKILLS — Skills Registry Ecosystem-1

**Version** : 1.0.0 · **Date** : 2026-03-17 · **Status** : 🟡 GENESIS

## 🎯 Purpose

This repository is the **canonical registry** of all Skills in ecosystem-1. It serves as the single source of truth for:

- **Native Skills**: Skills developed and maintained by gerivdb
- **Assimilated Skills**: External skills integrated into ecosystem-1
- **External Skills**: Third-party skills (e.g., from marketingskills)

## 🏗️ Architecture

### Repository Type

This is a **Registry Repository** (dépôt registre) per the ecosystem-1 taxonomy:

| Type | Definition | Rule |
|------|------------|------|
| **Dépôt Fédérateur** | Orchestrates all others via submodules | `ECOYSTEM` |
| **Dépôt Registre** | Declarative directory of transversal entities | `SKILLS` (this repo) |
| **Dépôt Domaine** | Implements a coherent business domain | `FLUENCE`, `BRAIN`, etc. |

### Taxonomie des Types de Skills

See [`TAXONOMY.md`](TAXONOMY.md) for the canonical definition of skill types:

- **Foundational Skills**: Cross-cutting skills applicable to all domains
- **Domain Skills**: Skills specific to a business domain
- **External Skills**: Third-party skills assimilated into ecosystem-1

## 📁 Structure

```
SKILLS/
├── README.md                 # This file
├── TAXONOMY.md              # Skill type definitions
├── REGISTRY.yaml            # Index of all registered skills
├── MANIFEST.json            # agentskills.io spec compatibility
├── CITIZENS.md              # Citizenship in ecosystem-1
├── CONTRIBUTING.md          # Contribution guidelines
├── CHANGELOG.md             # Version history
├── .gitmodules              # Submodule declarations
├── native/                  # Native skills (gerivdb)
│   ├── foundational/
│   │   ├── product-context/
│   │   └── ecosystem-principles/
│   └── domain/
│       ├── booking/
│       ├── recruitment/
│       ├── finance/
│       └── content/
├── ext/                     # External assimilated skills
│   └── marketingskills/     # Submodule: coreyhaines31/marketingskills
└── tools/                   # Validation and generation scripts
    ├── validate-skills.sh
    └── registry-gen.py
```

## 🔗 Integration with ECOYSTEM

This registry is integrated into [`ECOYSTEM`](https://github.com/gerivdb/ECOYSTEM) as a submodule at `.skills-hub/`.

```bash
# In ECOYSTEM
git submodule add https://github.com/gerivdb/SKILLS.git .skills-hub
```

## 📋 Registered Skills

See [`REGISTRY.yaml`](REGISTRY.yaml) for the complete index of all skills.

### Foundational Skills

| Skill | Description | Version |
|-------|-------------|---------|
| `product-context` | Product and audience contextualization | 1.0.0 |
| `ecosystem-principles` | ONTOLOGY, DRY, KISS, φ-CPS principles | 1.0.0 |

### Domain Skills

| Skill | Description | Domain | Version |
|-------|-------------|--------|---------|
| `booking` | Booking orchestration | GERIBOOKING | 1.0.0 |
| `recruitment` | Candidate matching | CANDIDATOR | 1.0.0 |
| `finance` | Banking analysis | BANK-BUSTER | 1.0.0 |
| `content` | Content generation | FLUENCE + BRAIN | 1.0.0 |

## 🤝 Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for contribution guidelines.

### Quick Start

1. Fork this repository
2. Create a branch: `feat/skills-[name]`
3. Add your skill following the SKILL.md template
4. Ensure CI validation passes
5. Submit a PR

### Validation Requirements

All skills must include:
- YAML frontmatter with `name`, `description`, `triggers`, `domain`, `version`
- Valid YAML syntax
- No broken links
- No duplicate skills

## 🔒 Governance

This repository follows ecosystem-1 governance:

- **Citizen**: `skills-registry` (L2)
- **Lifecycle**: GENESIS → ACTIVE
- **φ-CPS Weight**: 0.008

## 📜 License

Unless otherwise specified:
- Native skills: MIT License
- External skills: See respective repositories

---

*Maintained by gerivdb · Part of ecosystem-1*
