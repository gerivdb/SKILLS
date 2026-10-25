---
type: skill
version: "1.0.0"
date: "2026-10-25"
intent_hash: 0xCOMBO_DEPENDENCY_RESOLVER_20261025
status: active
---

# Skill: combo-dependency-resolver

## Rôle
Calcule le graphe de dépendances (DAG) avant d'exécuter un Combo, afin de déterminer l'ordre d'exécution valide et de détecter les cycles.

## Objectif
Analyser les dépendances entre les skills d'un combo, construire le DAG associé, vérifier l'absence de cycle, et retourner un ordre d'exécution topologiquement trié.

## Script
`scripts/resolve.ps1` — résout les dépendances d'un combo

## Usage
```powershell
# Résoudre les dépendances d'un combo depuis un fichier JSON
.\scripts\resolve.ps1 -ComboFile "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\combos\combo-incident-triage.json"

# Valider un DAG sans exécuter
.\scripts\resolve.ps1 -Skills @("skill-a","skill-b","skill-c") -Dependencies @{ "skill-b"="skill-a"; "skill-c"="skill-b" }
```

## Format de définition des dépendances (JSON)
```json
{
  "comboId": "combo-incident-triage",
  "skills": [
    { "id": "skill-a", "dependsOn": [] },
    { "id": "skill-b", "dependsOn": ["skill-a"] },
    { "id": "skill-c", "dependsOn": ["skill-a", "skill-b"] }
  ]
}
```

## WAL NEXUS
- Entité : COMBO_DEPENDENCY_RESOLVER
- Action : resolve_dag
- WAL path : WAL/combo/dependency-resolver.wal
- Preuve : `[COMBO_DAG] comboId=<id> skills=<N> edges=<N> hasCycle=<true|false> order=<JSON> ts=<UTC>`
- Contrat : aucun cycle n'est toléré ; si un cycle est détecté, le code de sortie est 3 et l'exécution est bloquée.

## Algorithme
1. Lecture de la liste des skills et de leurs dépendances
2. Construction de la matrice d'adjacence
3. Détection de cycle (DFS avec marquage blanc/gris/noir)
4. Tri topologique (Kahn's algorithm)
5. Retour de l'ordre d'exécution et du graphe

## Anti-patterns
- Dépendance circulaire entre deux skills (cycle de longueur 2)
- Dépendance transitive implicite non déclarée
- Skill référencé mais absent de la liste des skills du combo

## Références
- ADR : PRD-MOC-GEN-012 DESIGN-D (graphe de dépendances DAG)
- INTENT : INTENT-COMBO-DEPENDENCY-RESOLVER (GOVERNANCE-HUB/INTENTS/)