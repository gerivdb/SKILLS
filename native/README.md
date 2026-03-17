# Native Skills — Compétences Gerivdb

Ce répertoire contient les skills natifs développés et maintenus par gerivdb pour ecosystem-1.

## Structure

```
native/
├── README.md                    # Ce fichier
├── foundational/                 # Skills transversaux
│   ├── product-context/
│   │   └── SKILL.md
│   └── ecosystem-principles/
│       └── SKILL.md
└── domain/                      # Skills métier
    ├── booking/
    │   └── SKILL.md
    ├── recruitment/
    │   └── SKILL.md
    ├── finance/
    │   └── SKILL.md
    └── content/
        └── SKILL.md
```

## Types de Skills

### Foundational (Transversaux)

Skills applicables à tous les domaines :
- `product-context` : Contextualisation produit/audience
- `ecosystem-principles` : Principes architecturaux

### Domain (Métier)

Skills spécifiques à un domaine :
- `booking` : Réservations (GERIBOOKING)
- `recruitment` : Recrutement (CANDIDATOR)
- `finance` : Finance (BANK-BUSTER)
- `content` : Contenu (FLUENCE + BRAIN)

## Ajouter un Nouveau Skill

1. Créer le répertoire approprié (`foundational/` ou `domain/`)
2. Ajouter le fichier `SKILL.md` avec le template
3. Mettre à jour `REGISTRY.yaml`
4. Valider avec `tools/validate-skills.sh`

## Maintenance

- **Auteur** : gerivdb
- **Licence** : MIT
- **Version** : 1.0.0

---

*Part du registre SKILLS ecosystem-1*
