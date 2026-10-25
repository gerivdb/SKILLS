---
type: skill
version: "1.0.0"
date: "2026-10-25"
intent_hash: 0xCOMBO_PIPELINE_EXECUTOR_20261025
status: active
---

# Skill: combo-pipeline-executor

## Rôle
Moteur d'exécution synaptique qui enchaîne une série de skills unitaires avec passage déterministe de contexte via mémoire partagée (JSON-RPC/stdin).

## Objectif
Exécuter un pipeline de skills en séquence, où la sortie JSON-RPC de chaque skill devient l'entrée déterministe du suivant, avec isolation de contexte et traçabilité WAL à chaque étape.

## Script
`scripts/execute.ps1` — exécute un pipeline de skills en séquence

## Usage
```powershell
# Exécuter un combo depuis un fichier de définition
.\scripts\execute.ps1 -ComboFile "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\combos\combo-incident-triage.json" -Context @{"sessionId"="sess-001"}

# Exécuter avec contexte inline
.\scripts\execute.ps1 -Skills @("skill-a","skill-b") -Context @{"userId"="u42"}
```

## Format de définition de combo (JSON)
```json
{
  "comboId": "combo-incident-triage",
  "version": "1.0.0",
  "skills": [
    { "id": "skill-a", "input": {} },
    { "id": "skill-b", "input": { "dependsOn": "skill-a" } }
  ],
  "context": { "sessionId": "sess-001" }
}
```

## WAL NEXUS
- Entité : COMBO_PIPELINE_EXECUTOR
- Action : execute_pipeline
- WAL path : WAL/combo/pipeline-executor.wal
- Preuve : `[COMBO_EXEC] comboId=<id> skill=<id> status=OK|FAIL contextHash=<SHA256> ts=<UTC>`
- Contrat : chaque compétence du pipeline écrit son propre enregistrement WAL avant de passer le contexte au suivant.

## Anti-patterns
- Ne jamais exécuter deux compétences en parallèle sans isolation de contexte
- Ne jamais modifier le contexte intermédiaire entre deux compétences du même pipeline
- Ne pas omettre l'enregistrement WAL avant le passage de contexte

## Références
- ADR : PRD-MOC-GEN-012 DESIGN-C (pipelines synaptiques)
- INTENT : INTENT-COMBO-PIPELINE-EXECUTOR (GOVERNANCE-HUB/INTENTS/)