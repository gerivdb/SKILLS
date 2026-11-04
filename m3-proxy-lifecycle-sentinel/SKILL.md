---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_M3_PLS_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/m3-proxy-lifecycle-sentinel/SKILL.md
---

# Skill - m3-proxy-lifecycle-sentinel

## Objectif

Surveiller en temps reel le proxy synaptique local (port 18000) et assurer son redemarrage automatique en cas d'arret inopineux. Garantit la disponibilite permanente du canal BYOK et des flux inter-strates ENV2 <-> ENV3. Primitive M3-Tree de maintenance du proxy furtif.

## Declencheur

- Echec du test de connexion TCP sur 127.0.0.1:18000.
- Absence de processus python associe a local_stealth_proxy.py.
- Erreur de routage des requetes BYOK via le proxy local.
- Demande de verification periodique de la disponibilite du proxy.

## Entrees

- Port cible a surveiller (par defaut : 18000).
- Chemin vers le script local_stealth_proxy.py.
- Variable d'environnement BYOK_KEY requise pour le demarrage.
- Intervalle de sondage (en secondes, par defaut : 30).

## Sorties

- Etat du proxy (actif / inactif / redemarrage en cours).
- Rapport de relancement (PID du nouveau processus, horodatage).
- Code retour 0 si proxy actif, 1 si relancement reussi, 2 si echec de relancement.

## Regles Operationnelles

### 1. Verification periodique du port
Effectuer un test TCP sur 127.0.0.1:18000 a intervalles reguliers. Si le port ne repond pas, declencher la procedure de relancement.

### 2. Redemarrage automatique du proxy
Si le proxy est inactif, relancer le script local_stealth_proxy.py avec la variable d'environnement BYOK_KEY definie. Verifier que le processus Python est bien demarre.

### 3. Verification post-relancement
Attendre 3 secondes apres le lancement, puis refaire un test TCP sur le port 18000. Si le port repond, declarer le proxy actif. Sinon, signaler un echec.

### 4. Journalisation
Chaque verification et chaque relancement sont consignes avec l'etat du proxy, le PID du processus et l'horodatage.

### 5. Escalade
Si le relancement echoue trois fois consecutives, signaler pour intervention HITL sur la configuration BYOK_KEY ou le script proxy.
