---
name: kilo-rule-auditor
description: Audite et sanitize les regles Kilo dans C:\Users\GG\.kilocode\rules\ et .geri/rules/. Verifie la coherence avec les ADRs, detecte les contradictions, et trace les modifications dans git. Utilise ce skill quand tu dois verifier l'etat des regles Kilo, corriger une regle, ou auditer la conformite avant une session.
version: 1.0.0
intent_hash: 0xKILO_RULE_AUDITOR_20260810
---

# Kilo Rule Auditor

## Objectif
Garantir que les regles Kilo sont completes, coherentes, tracees git, et conformes aux ADRs backing.

## Declencheur
- Audit pre-session des regles Kilo
- Correction d'une regle apres fail
- Verification avant deploiement d'un workflow local
- Nettoyage de regles orphelines

## Perimetre
- `C:\Users\GG\.kilocode\rules\` (regles globales)
- `.geri/rules/` (regles projet GeriCode)
- Toute regle avec impact architectural (ADR backing requis)

## Protocole

### Etape 1 - Inventaire
```powershell
$globalRules = Get-ChildItem "C:\Users\GG\.kilocode\rules\*.md" -ErrorAction SilentlyContinue
$projectRules = Get-ChildItem ".geri\rules\*.md" -ErrorAction SilentlyContinue
```

### Etape 2 - Verification ADR backing
Pour chaque regle avec impact architectural :
- Lire la section `## Reference ADR` en fin de fichier
- Verifier que l'ADR existe dans `gerivdb/GOVERNANCE-HUB/ADR/`
- Verifier que le statut n'est pas `deprecated` ou `superseded`

### Etape 3 - Detection contradictions
- `BDCP mode inviolable` : present dans plusieurs regles ?
- `git-atomic-commit` : coherent avec `git-hygiene` ?
- `agent-budget-check` : valeurs RAM identiques dans toutes les regles ?

### Etape 4 - Sanitization
- Reformulations mineures : pas d'ADR requis
- Changement de comportement par defaut : ADR backing obligatoire
- Nouvelle regle avec impact architectural : creer ADR d'abord

### Etape 5 - Tracabilite git
Toute modification de regle :
```powershell
git add "C:\Users\GG\.kilocode\rules\<rule>.md"
git commit -m "chore(kilo-rules): sanitize <rule> - <raison>"
```

## Anti-patterns bloquants
- Modifier une regle sans verifier l'ADR backing
- Creer une regle avec impact architectural sans ADR
- Laisser des regles orphelines (sans ADR, sans reference)
- Corriger une regle dans la conversation sans commit git

## Reference ADR
- **ADR** : ADR-2026-08-10-004-KILO_RULE_AUDITOR
- **IntentHash** : 0xKILO_RULE_AUDITOR_20260810
- **Depot** : gerivdb/GeriCode
- **Statut ADR** : proposed
