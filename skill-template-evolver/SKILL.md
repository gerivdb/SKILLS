# Skill: skill-template-evolver

## Description
Fait évoluer le template canonique `SKILL.md` lorsqu'une nouvelle propriété est ajoutée à un skill existant. Garantit que tous les skills de l'écosystème respectent le même schéma de frontmatter et de métadonnées.

## Déclencheurs
- Mentions : "évoluer template", "mettre à jour template skill", "nouvelle propriété skill"

## Règles
- Lorsqu'une nouvelle propriété est ajoutée à un skill (ex: `phi_weight`, `assimilation_status`), le template est mis à jour
- Tous les skills existants sont scannés pour vérifier la présence de la nouvelle propriété
- Les skills sans la nouvelle propriété sont signalés pour mise à jour

## Invariants
- Tous les skills doivent avoir le même ensemble de propriétés de frontmatter
- Aucune propriété ne peut être ajoutée sans mise à jour du template canonique

## Statut
- Version : 1.0.0
- Statut : active
- Type : domain
- Dépendances : `skill-ecosystem-auditor`