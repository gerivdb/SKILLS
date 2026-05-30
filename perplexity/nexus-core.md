---
name: nexus-core
description: "NEXUS governance, SOT conformity, ECOS_ROOT, EPIC, PRD, RSS-v1. Use when user mentions 'NEXUS', 'gouvernance', 'SOT', 'ECOS_ROOT', 'φ-CPS'."
version: "1.0.0"
changelog:
  - {v: "1.0.0", date: "2026-05-30", notes: "Version initiale"}
triggers: []
layer: "L0_UNKNOWN"
nexusTags: ["CONFORME_NEXUS"]---
|
# NEXUS Core

## Domaine et périmètre

NEXUS est le **SOT (Source of Truth)** de l'écosystème gerivdb. Ce skill couvre :
- La gouvernance constitutionnelle (ADR, EPIC, PRD)
- La validation φ-CPS et la conformité des couches L0-L5
- Le registre ECOS_ROOT et sa synchronisation
- Les workflows de propagation (WAL, BLO, miroirs)
- La politique RSS-v1 et les standards structurels

## Méthodologie

### Phase 1 : Lecture du contexte
1. Identifier le dépôt ou l'EPIC concerné.
2. Consulter `ECOS_ROOT.json` via `mcp_github get_file_contents`.
3. Vérifier l'existence d'ADR applicables.

### Phase 2 : Validation constitutionnelle
1. Contrôler le format IntentHash (`0x[A-Z_]+_φ[X.XXX]`).
2. Vérifier le seuil φ-CPS (≥ 4.559 pour les ADR constitutionnelles).
3. Appliquer les critères DDD : contexte borné, autonomie, cohésion.

### Phase 3 : Décision et propagation
1. Émettre un tag `[CONFORME_NEXUS]`, `[À_VALIDER_NEXUS]` ou `[HORS_NEXUS]`.
2. Si conforme, proposer la propagation vers les dépôts cibles.
3. Si non conforme, lister les violations et proposer des correctifs.

## Règles de décision
- **Règle 1** : Une EPIC > 10 Ko dans NEXUS est une spécification technique, pas un plan → doit être externalisée.
- **Règle 2** : Tout fichier `.py` à la racine de NEXUS est un agent égaré → doit migrer vers BRAIN.
- **Règle 3** : Les configs d'outillage (`.kilo`, `.mcp`, `.rules`) doivent résider dans DevTools.

## Format de sortie

```markdown
## Verdict : [CONFORME_NEXUS | À_VALIDER_NEXUS | HORS_NEXUS]

### Justification
- Critère 1 : ...
- Critère 2 : ...

### Actions recommandées
1. ...
2. ...
```

## Exemples d'utilisation
- "Vérifie la conformité du dépôt X" → Auditer la structure, les EPICs et les dépendances.
- "Quel est le statut de l'ADR-0020 ?" → Lire et valider l'ADR.
- "Propager la décision Y vers DevTools" → Vérifier le WAL et proposer les PRs.

## Intégration avec l'écosystème
- Dépôts concernés : NEXUS, ECOYSTEM, ONTOLOGY, DevTools
- Couche EECS : L1_CAUSALITY
- Citoyens liés : nexus_validate_v2, phi_cps_monitor, autonomous_sync
- Tags NEXUS : [CONFORME_NEXUS], [À_VALIDER_NEXUS], [HORS_NEXUS]
