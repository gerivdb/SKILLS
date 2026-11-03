---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_RTB_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/rate-limiter-token-bucket/SKILL.md
---

# Skill - rate-limiter-token-bucket

## Objectif

Integre les quotas journaliers par token et par requete configures dans gateway.yaml. Garantit qu'aucun client ne depasse son allocation de requetes LLM par jour.

## Declencheur

- Requete LLM entrante avec un token d'authentification.
- Depassement du quota journalier d'un token.
- Verification du seau a tokens avant autorisation de requete.

## Entrees

- Identifiant du token client.
- Nombre de requetes deja effectuees aujourd'hui.
- Quota journalier configure dans gateway.yaml.
- Nombre de tokens disponibles dans le seau.

## Sorties

- Autorisation ou rejet de la requete.
- Nombre de tokens restants dans le seau.
- Code retour 0 si autorise, 1 si quota epuise, 2 si seau vide.

## Regles Operationnelles

### 1. Seau a tokens par client
Chaque token client possede son propre seau a tokens avec un quota journalier.

### 2. Consommation d'un token
Chaque requete autorisee consomme un token du seau. Si le seau est vide, la requete est rejetee.

### 3. Recharge journaliere
Le seau est recharge a minuit avec le quota journalier configure dans gateway.yaml.

### 4. Rejet en cas de depassement
Si un client depasse son quota journalier, la requete est rejetee avec un message d'erreur indiquant le quota restant.

### 5. Journalisation
Chaque autorisation ou rejet est consigne avec le token, le nombre de requetes et l'horodatage.
