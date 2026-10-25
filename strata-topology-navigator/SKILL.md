---
type: SKILL
name: strata-topology-navigator
version: "1.0.0"
intent_hash: 0xSTRATA_TOPOLOGY_NAVIGATOR_20261025
date: "2026-10-25"
layer: L4-TOOLS
---

# Strata Topology Navigator

## Objectif
Creer une navigation spatiale deterministe pour localiser n'importe quel depot de l'ecosystème gerivdb sous D:\DO\WEB\TOOLS\L*. Ce skill interdit les balayages recursifs sauvages sur D:\DO\WEB\ et fournit une matrice de routage O(1) pour resoudre instantanément le chemin absolu d'un depot.

## Declencheur
- Un agent doit localiser un depot par son nom (ex: GATEWAY-MANAGER, SKILLS, RAGX)
- Un agent doit verifier la strate d'appartenance d'un depot
- Interdiction de lancer Get-ChildItem -Recurse sur D:\DO\WEB\

## Taxonomie canonique des strates (SSoT)

| Strate | Répertoire physique | Rôle architectural | Dépôts clés |
|--------|---------------------|---------------------|-------------|
| L0-CANON | D:\DO\WEB\TOOLS\L0-CANON\ | Socle inviolable, SSoT, Gouvernance | RAGX, BRAIN, ONTOLOGY, GOVERNANCE-HUB, NEXUS |
| L1-INFRA | D:\DO\WEB\TOOLS\L1-INFRA\ | Infrastructure, Clapet BDCP, Gateways | GATEWAY-MANAGER |
| L2-PLATFORM | D:\DO\WEB\TOOLS\L2-PLATFORM\ | Plateforme d'exécution, Runners, Overlays IDE | KIX, GeriCode |
| L3-CITIZENS | D:\DO\WEB\TOOLS\L3-CITIZENS\ | Citoyens autonomes, Daemons, Superviseurs | VEX |
| L4-TOOLS | D:\DO\WEB\TOOLS\L4-TOOLS\ | Outils transversaux, Registres de compétences | SKILLS, TRIX, INFX, FLEX, CodeDB-E5620 |
| L5-ARCHIVE | D:\DO\WEB\TOOLS\L5-ARCHIVE\ | Dépôts patrimoniaux gelés | Archives historiques |
| L6-WORK | D:\DO\WEB\TOOLS\L6-WORK\ | Chantiers temporaires, Espaces scratch | Worktrees jetables |

## Anti-pattern bloquant (regle absolue)
Interdiction formelle d'exécuter Get-ChildItem -Recurse D:\DO\WEB\ ou find /d/DO/WEB/. Toute résolution de depot DOIT passer par l'interrogation directe des sous-dossiers de D:\DO\WEB\TOOLS\L* ou par le script locate_stratum.ps1.

## Protocole de resolution
1. Recevoir le nom du depot cible (ex: SKILLS)
2. Tester l'existence de D:\DO\WEB\TOOLS\L0-CANON\<nom>, puis L1-INFRA\<nom>, etc. jusqu'à L6-WORK\<nom>
3. Retourner le chemin absolu, la strate et le role en JSON structuré
4. Si non trouvé dans les strates L*, tester D:\DO\WEB\TOOLS\<nom> (niveau 1 uniquement, sans récursion)

## Sortie standard (JSON)
```json
{
  "repo_name": "SKILLS",
  "stratum": "L4-TOOLS",
  "role": "Outils transversaux, Registres de compétences",
  "absolute_path": "D:\\DO\\WEB\\TOOLS\\L4-TOOLS\\SKILLS",
  "found": true
}
```

## WAL NEXUS
Chaque navigation réussie est consignée dans .kilo/strata_wal.jsonl avec horodatage UTC.

## Reference ADR
- **ADR** : ADR-2026-06-28-001-LOGICAL-ARCHITECTURE-N1-N4
- **IntentHash** : 0xSTRATA_TOPOLOGY_NAVIGATOR_20261025
- **Depot** : gerivdb/SKILLS
- **Statut ADR** : proposed

## Script cible
scripts/locate_stratum.ps1