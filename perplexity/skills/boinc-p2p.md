---
name: boinc-p2p
description: "BOINC-LLM distributed inference, DHT Kademlia, swarm, P2P computing. Use when user mentions 'BOINC-LLM', 'P2P', 'distribué', 'swarm'."
version: "1.0.0"
changelog:
  - {v: "1.0.0", date: "2026-05-30", notes: "Version initiale"}
triggers: []
layer: "L0_UNKNOWN"
nexusTags: ["CONFORME_NEXUS"]---
|
# BOINC P2P

## Domaine et périmètre

Ce skill couvre l'inférence LLM distribuée en P2P via BOINC-LLM :
- Le réseau swarm de nœuds de calcul (Kademlia DHT)
- La distribution des modèles et des tâches d'inférence
- La coordination avec INTENT-ENCODER (nomic-embed-text, 768-dim)
- L'intégration avec le matériel Z600 (CPU-only, 24 GB RAM)

## Méthodologie

### Phase 1 : Découverte du réseau
- Scanner les nœuds disponibles via la DHT Kademlia.
- Évaluer les capacités de chaque nœud (CPU, RAM, bande passante).
- Construire la table de routage du swarm.

### Phase 2 : Distribution des tâches
- Partitionner le modèle LLM en shards compatibles avec chaque nœud.
- Assigner les tâches d'inférence selon les capacités.
- Gérer la redondance (réplication des shards critiques).

### Phase 3 : Agrégation
- Collecter les résultats partiels de chaque nœud.
- Fusionner les outputs (vote majoritaire, moyenne pondérée).
- Valider la cohérence du résultat final.

## Règles de décision
- **Règle 1** : Un nœud Z600 (E5620, pas d'AVX) ne peut traiter que des modèles quantisés (BitNet b1.58).
- **Règle 2** : Le swarm minimum pour une inférence fiable = 3 nœuds (tolérance 1 panne).
- **Règle 3** : Les shards > 500 Mo doivent être répliqués sur au moins 2 nœuds.

## Format de sortie

```markdown
## Statut Swarm
- Nœuds actifs : [N]
- Modèle chargé : [nom] ([taille])
- Tâches en cours : [N]
- Résultat : [output]
```

## Exemples d'utilisation
- "Lance une inférence distribuée sur le swarm" → Distribuer et agréger.
- "Quels nœuds sont disponibles ?" → Scanner la DHT.
- "Charge BitNet b1.58 sur le swarm" → Partitionner et distribuer.

## Intégration avec l'écosystème
- Dépôts concernés : INTENT-ENCODER, PLIX, NEXUS
- Couche EECS : L4_ORCHESTRATION
- Tags NEXUS : [CONFORME_NEXUS], [DÉRIVÉ]