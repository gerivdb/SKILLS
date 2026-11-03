---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_M3_FINOPS_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/m3-finops-guardian/SKILL.md
---

# Skill - m3-finops-guardian

## Objectif

Modele en continu le cout computationnel, la latence des endpoints proxy (port 18000) et l'utilisation des quotas pour arbitrer dynamiquement le routage des requetes entre les differents backends BYOK. Primitive M3-Tree de supervision FinOps predictive.

## Declencheur

- Depassement du seuil de cout computationnel journalier.
- Latence anormale sur un endpoint proxy (port 18000).
- Quota BYOK approche de sa limite quotidienne.
- Demande d'arbitrage de routage entre plusieurs backends LLM.

## Entrees

- Metriques de cout computationnel (CPU, RAM, temps d'execution).
- Latence mesuree sur chaque endpoint proxy.
- Quotas restants par backend BYOK.
- Trafic de requetes entrante par client/token.

## Sorties

- Decision de routage (backend cible ou rejet).
- Rapport de cout predit pour la requete.
- Code retour 0 si routage autorise, 1 si quota epuise, 2 si latence critique.

## Regles Operationnelles

### 1. Modelage du cout computationnel
Suivre en continu le cout CPU, RAM et temps d'execution de chaque requete LLM.

### 2. Surveillance de la latence proxy
Mesurer la latence de chaque endpoint proxy (port 18000) et detecter les anomalies.

### 3. Arbitrage dynamique
Routier chaque requete vers le backend BYOK offrant le meilleur compromis cout/latence/quota disponible.

### 4. Alerte de depassement de seuil
Si le cout computationnel journalier ou un quota BYOK approche de sa limite, alerter et rediriger le trafic.

### 5. Journalisation
Chaque decision de routage est consignee avec le backend cible, le cout predit, la latence mesuree et l'horodatage.
