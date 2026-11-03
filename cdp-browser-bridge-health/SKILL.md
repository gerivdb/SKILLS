---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_CBH_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/cdp-browser-bridge-health/SKILL.md
---

# Skill - cdp-browser-bridge-health

## Objectif

Teste la reactivite des ponts Chrome CDP (port 9223) et Lightpanda (port 19222) sur ENV5. Garantit que les ponts navigateur IA sont operationnels avant tout routage de trafic.

## Declencheur

- Verification de sante des ponts CDP avant demarrage du gateway.
- Erreur de connexion au port 9223 (Chrome CDP) ou 19222 (Lightpanda).
- Demande de test de reactivite des navigateurs headless sur ENV5.

## Entrees

- Port du pont CDP a tester (9223 pour Chrome, 19222 pour Lightpanda).
- Timeout de reponse attendu (en secondes, par defaut 5).
- Endpoint de health check du pont.

## Sorties

- Etat du pont (actif / inactif / injoignable).
- Temps de reponse du health check en millisecondes.
- Code retour 0 si pont actif, 1 si pont inactif, 2 si timeout.

## Regles Operationnelles

### 1. Test de sante du pont CDP
Tente une connexion TCP sur le port cible (9223 ou 19222) avec un timeout de 5 secondes.

### 2. Verification de reponse HTTP
Si le port est ouvert, envoie une requete GET sur l'endpoint de health check du pont et verifie le code de reponse.

### 3. Alerting en cas d'indisponibilite
Si le pont ne repond pas, alerte le gateway pour arreter le routage de trafic vers ce pont.

### 4. Surveillance periodique
Le test de sante est execute periodiquement (par defaut : toutes les 30 secondes) pour detecter toute degradation.

### 5. Journalisation
Chaque test de sante est consigne avec le port, le temps de reponse et le statut.
