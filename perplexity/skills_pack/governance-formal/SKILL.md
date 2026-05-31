---
name: governance-formal
description: "GOVERNANCE-HUB, REPO-STANDARDS, ONTOLOGY, RSS-v1 lifecycle. Use when user mentions 'GOVERNANCE-HUB', 'REPO-STANDARDS', 'ONTOLOGY', 'RSS-v1', 'lifecycle'."
version: "1.0.0"
changelog:
  - {v: "1.0.0", date: "2026-05-30", notes: "Version initiale"}
triggers: []
layer: "L0_UNKNOWN"
nexusTags: ["CONFORME_NEXUS"]
---
# Governance Formal

## Domaine et périmètre

Ce skill couvre la **gouvernance formelle** de l'écosystème gerivdb :
- GOVERNANCE-HUB (dépôt central des règles de gouvernance)
- REPO-STANDARDS (standards structurels pour tous les dépôts)
- ONTOLOGY (ontologie des termes, audit, définitions N/N+1/N+2)
- RSS-v1 (Resource Structure Standard v1 — lifecycle des ressources)

## Méthodologie

### Phase 1 : Identification
- Déterminer le type de gouvernance : structure, ontologie, ou lifecycle.
- Consulter les fichiers de référence dans GOVERNANCE-HUB et ONTOLOGY.
- Vérifier la conformité du dépôt ou fichier concerné.

### Phase 2 : Analyse
- Auditer la structure du dépôt contre REPO-STANDARDS.
- Vérifier les termes ontologiques (existent-ils dans ONTOLOGY ?).
- Contrôler le lifecycle RSS-v1 (draft → active → deprecated).

### Phase 3 : Action
- Proposer les corrections de conformité.
- Mettre à jour ONTOLOGY si des termes manquent.
- Documenter les décisions dans les ADR.

## Règles de décision
- **Règle 1** : Tout nouveau dépôt doit être conforme à RSS-v1 avant le premier commit.
- **Règle 2** : Les termes métier doivent être définis dans ONTOLOGY au format N/N+1/N+2.
- **Règle 3** : Les violations de REPO-STANDARDS sont bloquantes pour les dépôts P0.

## Format de sortie

```markdown
## Audit Gouvernance
- Dépôt : [nom]
- Conformité RSS-v1 : [conforme | violations]
- Termes ONTOLOGY : [N définis | N manquants]
- Statut lifecycle : [draft | active | deprecated]
```

## Exemples d'utilisation
- "Audite la conformité de FLUENCE" → Vérifier structure + ontologie.
- "Ajoute le terme X dans ONTOLOGY" → Définir au format N/N+1/N+2.
- "Quel est le lifecycle de ce dépôt ?" → Consulter RSS-v1.

## Intégration avec l'écosystème
- Dépôts concernés : GOVERNANCE-HUB, REPO-STANDARDS, ONTOLOGY, NEXUS
- Couche EECS : L1_CAUSALITY
- Tags NEXUS : [CONFORME_NEXUS], [À_VALIDER_NEXUS]
