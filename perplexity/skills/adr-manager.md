---
name: adr-manager
description: "Architecture Decision Records: validation, creation, lifecycle. Use when user mentions 'ADR', 'décision architecture', 'valider ADR', 'nexus jalon'."
version: "1.0.0"
changelog:
  - {v: "1.0.0", date: "2026-05-30", notes: "Version initiale"}
triggers: []
layer: "L0_UNKNOWN"
nexusTags: ["CONFORME_NEXUS"]
---
|
# ADR Manager

## Domaine et périmètre

Ce skill couvre la gestion des **Architecture Decision Records (ADR)** dans l'écosystème gerivdb :
- La création et validation d'ADR selon le format MADR
- Le cycle de vie : draft → proposed → accepted → deprecated → superseded
- La liaison ADR ↔ EPIC ↔ PRD dans NEXUS
- La validation constitutionnelle via φ-CPS

## Méthodologie

### Phase 1 : Identification
- Déterminer le type d'action : créer, valider, déprécier ou référencer un ADR.
- Vérifier l'existence d'ADR liés dans `NEXUS/governance/adr/`.
- Contrôler le format IntentHash (`0x[A-Z_]+_φ[X.XXX]`).

### Phase 2 : Analyse
- Évaluer le seuil φ-CPS (≥ 4.559 pour les ADR constitutionnelles).
- Vérifier la conformité DDD : contexte borné, autonomie, cohésion.
- Croiser avec les EPICs et PRD impactés.

### Phase 3 : Action
- Générer le fichier ADR au format MADR dans `NEXUS/governance/adr/`.
- Proposer la propagation vers les dépôts cibles via WAL.
- Tagger selon la conformité NEXUS.

## Règles de décision
- **Règle 1** : Tout ADR constitutionnel doit avoir un IntentHash et un score φ-CPS.
- **Règle 2** : Un ADR ne peut pas référencer un EPIC > 10 Ko (spécification technique à externaliser).
- **Règle 3** : Les ADR deprecated doivent pointer vers leur remplaçant (superseded by).

## Format de sortie

```markdown
## ADR-[NNN] : [Titre]
- **Statut** : [draft | proposed | accepted | deprecated]
- **IntentHash** : 0x...
- **φ-CPS** : X.XXX
- **Impact** : [dépôts concernés]
```

## Exemples d'utilisation
- "Crée un ADR pour la migration gateway GPU" → Générer le MADR.
- "Valide l'ADR-0020 selon φ-CPS" → Lire, scorer, taguer.
- "Quels ADRs sont liés à l'EPIC FLUENCE ?" → Lister les références croisées.

## Intégration avec l'écosystème
- Dépôts concernés : NEXUS, GOVERNANCE-HUB, ONTOLOGY
- Couche EECS : L1_CAUSALITY
- Tags NEXUS : [CONFORME_NEXUS], [À_VALIDER_NEXUS]