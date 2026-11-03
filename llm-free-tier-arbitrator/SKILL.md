---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_LFA_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/llm-free-tier-arbitrator/SKILL.md
---

# Skill - llm-free-tier-arbitrator

## Objectif

Route dynamiquement les requetes LLM prioritaires vers les 9 providers gratuits (Cerebras, Groq, Mistral, etc.). Garantit une utilisation optimale des quotas gratuits sans dependre d'un seul fournisseur.

## Declencheur

- Requete LLM entrante requiring un provider gratuit.
- Depassement de quota sur un provider gratuit.
- Erreur 429 (rate limit) sur un provider LLM gratuit.

## Entrees

- Requete LLM (prompt, parametres, priorite).
- Liste des providers gratuits disponibles (Cerebras, Groq, Mistral, etc.).
- Quotas restants par provider.

## Sorties

- Provider LLM selectionne pour la requete.
- Rapport de routage (provider choisi, raison, quota restant).
- Code retour 0 si routage reussi, 1 si aucun provider disponible, 2 si quota epuise sur tous.

## Regles Operationnelles

### 1. Routage dynamique par priorite
Les requetes prioritaires sont acheminees vers le provider gratuit avec le plus grand quota restant.

### 2. Respect des quotas journaliers
Chaque provider gratuit a un quota journalier. Une fois epuise, le trafic est redirige vers un autre provider.

### 3. Basculement automatique en cas d'erreur 429
Si un provider retourne une erreur 429 (trop de requetes), le trafic est immediatement redirige vers un provider alternatif.

### 4. Rotation equitable
Le trafic est reparti equitablement entre les providers pour eviter de concentrer la charge sur un seul.

### 5. Journalisation des choix
Chaque decision de routage est consignee avec le provider selectionne, la priorite de la requete et l'horodatage.
