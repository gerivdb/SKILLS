---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_BZTG_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/bdcp-zero-trust-traffic-guard/SKILL.md
---

# Skill - bdcp-zero-trust-traffic-guard

## Objectif

Valide les signatures IntentHash BDCP sur le trafic transitant par src/bdcp_enforcer.py. Garantit qu'aucun trafic non signe ne traverse le mode BDCP (Behind CDP).

## Declencheur

- Trafic transitant par bdcp_enforcer.py sans signature IntentHash valide.
- Verification de conformite BDCP avant envoi de requete externe.
- Detection de trafic sortant non autorise en mode BDCP.

## Entrees

- Paquet de trafic a verifier.
- Signature IntentHash attendue.
- Chemin vers bdcp_enforcer.py.
- Mode BDCP actif (true/false).

## Sorties

- Decision de validation (autorise / bloque).
- Rapport de validation avec la signature verifiee.
- Code retour 0 si trafic valide, 1 si signature invalide, 2 si trafic non signe.

## Regles Operationnelles

### 1. Verification de la signature IntentHash
Tout paquet de trafic doit posseder une signature IntentHash valide correspondant a un ADR ou un skill enregistre.

### 2. Blocage du trafic non signe
Tout trafic transitant par bdcp_enforcer.py sans signature IntentHash est bloque immediatement.

### 3. Mode BDCP actif
En mode BDCP, seul le trafic signe et autorise peut sortir. Tout trafic non signe est refuse.

### 4. Journalisation
Chaque validation de signature est consignee avec l'IntentHash, le statut et l'horodatage.

### 5. Escalade
En cas de trafic non signe repete, signaler pour intervention HITL.
