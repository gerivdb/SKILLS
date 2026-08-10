---
name: kilo-rule-auditor
description: Audite et sanitize les règles Kilo dans C:\Users\GG\.kilocode\rules\ et .kilo/rules/. Vérifie la cohérence avec les ADRs, détecte les contradictions, et trace les modifications dans git. Utilise ce skill quand tu dois vérifier l'état des règles Kilo, corriger une règle, ou auditer la conformité avant une session.
version: 1.0.0
intent_hash: 0xKILO_RULE_AUDITOR_20260810
---

# Kilo Rule Auditor

## Objectif
Garantir que les règles Kilo sont complètes, cohérentes, tracées git, et conformes aux ADRs backing.

## Déclencheur
- Audit pré-session des règles Kilo
- Correction d'une règle après fail
- Vérification avant déploiement d'un workflow local
- Nettoyage de règles orphelines

## Périmètre
- `C:\Users\GG\.kilocode\rules\` (règles globales)
- `.kilo/rules/` (règles projet GeriCode)
- Toute règle avec impact architectural (ADR backing requis)

## Protocole

### Étape 1 — Inventaire
```powershell
$globalRules = Get-ChildItem "C:\Users\GG\.kilocode\rules\*.md" -ErrorAction SilentlyContinue
$projectRules = Get-ChildItem ".kilo\rules\*.md" -ErrorAction SilentlyContinue
```

### Étape 2 — Vérification ADR backing
Pour chaque règle avec impact architectural :
- Lire la section `## Référence ADR` en fin de fichier
- Vérifier que l'ADR existe dans `gerivdb/GOVERNANCE-HUB/ADR/`
- Vérifier que le statut n'est pas `deprecated` ou `superseded`

### Étape 3 — Détection contradictions
- `BDCP mode inviolable` : présent dans plusieurs règles ?
- `git-atomic-commit` : cohérent avec `git-hygiene` ?
- `agent-budget-check` : valeurs RAM identiques dans toutes les règles ?

### Étape 4 — Sanitization
- Reformulations mineures : pas d'ADR requis
- Changement de comportement par défaut : ADR backing obligatoire
- Nouvelle règle avec impact architectural : créer ADR d'abord

### Étape 5 — Traçabilité git
Toute modification de règle :
```powershell
git add "C:\Users\GG\.kilocode\rules\<rule>.md"
git commit -m "chore(kilo-rules): sanitize <rule> — <raison>"
```

## Anti-patterns bloquants
- Modifier une règle sans vérifier l'ADR backing
- Créer une règle avec impact architectural sans ADR
- Laisser des règles orphelines (sans ADR, sans référence)
- Corriger une règle dans la conversation sans commit git

## Référence ADR
- **ADR** : ADR-2026-08-10-004-KILO_RULE_AUDITOR
- **IntentHash** : 0xKILO_RULE_AUDITOR_20260810
- **Dépôt** : gerivdb/GeriCode
- **Statut ADR** : proposed
