---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_NSB_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/nim-saturation-backoff/SKILL.md
---

# Skill - nim-saturation-backoff

## Objectif

Intercepte les erreurs 429/ResourceExhausted sur Nemotron/OpenRouter et applique un backoff automatique de 60s. Garantit que le systeme ne sature pas un fournisseur LLM sous charge.

## Declencheur

- Erreur HTTP 429 (trop de requetes) sur Nemotron ou OpenRouter.
- Erreur ResourceExhausted sur un endpoint LLM.
- Saturation detectee sur un provider LLM distant.

## Entrees

- Nom du provider LLM (Nemotron, OpenRouter, etc.).
- Code d'erreur HTTP (429, ResourceExhausted).
- Temps d'attente recommande (par defaut 60 secondes).

## Sorties

- Decision de backoff (actif / inactif).
- Temps d'attente impose avant la prochaine requete.
- Code retour 0 si backoff applique, 1 si aucune erreur detectee.

## Regles Operationnelles

### 1. Detection d'erreur 429 ou ResourceExhausted
Toute reponse HTTP 429 ou erreur ResourceExhausted declenche immediatement le backoff.

### 2. Backoff automatique de 60 secondes
Une fois l'erreur detectee, aucune nouvelle requete n'est envoyee au provider pendant 60 secondes minimum.

### 3. Redirection vers provider alternatif
Pendant la periode de backoff, le trafic est redirige vers un provider LLM disponible.

### 4. Reprise progressive
Apres la periode de backoff, une requete de test est envoyee pour verifier que le provider est de nouveau disponible.

### 5. Journalisation
Chaque declenchement de backoff est consigne avec le provider, le code d'erreur et l'horodatage.
