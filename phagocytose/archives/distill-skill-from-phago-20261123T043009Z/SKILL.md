---
name: distill-skill-from-phago
version: "0.1.0"
status: draft
type: procedural
category: phagocytose
intent_hash: 0xDISTILL-SKILL-FROM-PHAGO_20261123
provenance: phagocytose
source_shard: ENV2
created_at: "2026-11-23T04:30:03.0017831Z"
updated_at: "2026-11-23T04:30:03.0017831Z"
author: auto
triggers:
  - "distill"
  - "skill"
  - "from"
  - "phago"
  - "chromium"
  - "cdp"
  - "profile"
  - "git"
  - "python"
  - "9222"
anti_triggers:
  - "headless"
  - "profil temporaire"
weight:
  - 5
  - 4
  - 3
  - 2
  - 1
  - 0
  - -1
  - -2
  - -3
  - -4
prerequisites:
  - "PowerShell 7+"
verification:
  command: "TODO - à définir après validation"
  expected_exit_code: 0
  expected_output_contains: "TODO"
hash_sha256_evidence: "9ed776e269e8a0c773f6094182c81c18d5cd389bfcd9e7254f8f267fc4a5f8e4"
supersedes: []
superseded_by: null
tags:
  - "phagocytose"
  - "shard-ENV2"
---

# Skill : distill-skill-from-phago — Phagocytose depuis D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\distill\distill-skill.ps1

## Objectif
Skill produit par phagocytose profonde de la source : D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\distill\distill-skill.ps1

## Localisation
$skillDir

## Fichiers du skill
- SKILL.md — ce document (généré par phagocytose.ps1).
- EVIDENCE.md — preuve d'exécution (créée après première utilisation).
- HISTORY.md — journal des versions.

## Prérequis
- PowerShell 7+

## Procédure
Ce skill a été produit par phagocytose profonde. Les étapes ci-dessous sont extraites de la déconstruction.

### Étapes reproductibles identifiées
- versioning v0.1.0, merge au lieu de duplication).
- Shard d'origine (ENV2, ENV3, ...). Défaut: ENV2.
- $lines += 'version: "0.1.0"'
- $lines += "Les étapes ci-dessous doivent être vérifiées et complétées manuellement avant promotion."
- $lines += "- v0.1.0 : Distillé depuis $TranscriptPath le $nowUtc (statut: draft)."
- $historyLines += "## v0.1.0 — $nowUtc"
- Write-Output "Prochaine étape : valider avec validate-skill.ps1, puis promouvoir vers skills/"

## Règles de bonne pratique
- Valider chaque étape extraite avant promotion.
- Ne pas committer un skill phagocyté sans vérification manuelle.
- Respecter la règle Explicit Path Compliance pour tous les chemins.

## Vérification
- Exécuter alidate-skill.ps1 sur ce candidat avant promotion.
- Tester la procédure décrite dans un shard cible (ENV2 ou ENV3).

## Historique
- v0.1.0 : Phagocytose depuis D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\distill\distill-skill.ps1 le 2026-11-23T04:30:03.0017831Z (statut: draft).
- Voir HISTORY.md après promotion vers ctive.

