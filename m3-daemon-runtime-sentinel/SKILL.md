---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_M3_DRS_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/m3-daemon-runtime-sentinel/SKILL.md
---

# Skill - m3-daemon-runtime-sentinel

## Objectif

Surveiller les demons Python et node en temps reel sur ENV2 et intervenir immediatement en cas d'echec (processus mort, port non repondant, exception bloquante). Complete le pre-vol statique de daemon-preflight-import-sentinel par une surveillance runtime. Primitive M3-Tree de sentinelle de demon.

## Declencheur

- Processus Python ou node associe a un daemon mort ou injoignable.
- Exception bloquante sur un daemon en cours d'execution.
- Port associe a un demon ne repondant plus.
- Demande de surveillance runtime d'un demon specifique.

## Entrees

- Nom du demon a surveiller.
- Chemin vers le script principal du demon.
- Port associe au demon (si applicable).
- Intervalle de sondage (en secondes, par defaut : 10).
- Variable d'environnement requise (ex: BYOK_KEY).

## Sorties

- Etat du demon (actif / inactif / redemarrage en cours).
- Rapport de redemarrage (PID du nouveau processus, horodatage).
- Code retour 0 si demon actif, 1 si redemarrage reussi, 2 si echec de redemarrage.

## Regles Operationnelles

### 1. Surveillance periodique du demon
Verifier a intervalles reguliers que le processus du demon est toujours actif et repond sur son port associe.

### 2. Redemarrage automatique
Si le demon est inactif, relancer le script principal avec les variables d'environnement necessaires. Verifier que le processus est bien demarre.

### 3. Verification post-redemarrage
Attendre quelques secondes, puis verifier que le demon repond sur son port. Si le port ne repond pas, declarer un echec.

### 4. Journalisation
Chaque verification et chaque redemarrage est consigne avec le nom du demon, le PID et l'horodatage.

### 5. Escalade
Si le redemarrage echoue trois fois consecutives, signaler pour intervention HITL sur la configuration du demon.
