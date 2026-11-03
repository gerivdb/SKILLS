---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_SSE_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/mcp-sse-keepalive-sentinel/SKILL.md
---

# Skill - mcp-sse-keepalive-sentinel

## Objectif

Detecte les deconnexions silencieuses sur les endpoints de streaming Server-Sent Events (SSE) du gateway. Garantit que les clients MCP restent informes de l'etat de leur connexion SSE.

## Declencheur

- Perte de connexion SSE sans notification explicite.
- Timeout de keepalive depasse sur un endpoint SSE.
- Frontend qui ne recoit plus d'evenements SSE depuis trop longtemps.

## Entrees

- Identifiant de l'endpoint SSE.
- URL de l'endpoint SSE (ex: /mcp/{backend_id}/sse).
- Intervalle de keepalive attendu (en secondes).

## Sorties

- Etat de connexion (actif / perdu / en attente).
- Rapport de deconnexion avec horodatage et cause probable.
- Code retour 0 si connexion active, 1 si deconnexion detectee, 2 si timeout de keepalive.

## Regles Operationnelles

### 1. Verification periodique du keepalive
Le gateway envoie un message de keepalive SSE a intervalles reguliers (par defaut : 30 secondes). Absence de reponse = deconnexion possiblement silencieuse.

### 2. Detection de deconnexion silencieuse
Si aucun evenement SSE n'est recu depuis plus de 2 fois l'intervalle de keepalive, la connexion est declaree perdue.

### 3. Alerting aux clients
Les clients connects sont notifies de la deconnexion et invites a se reconnecter.

### 4. Nettoyage des connexions zombie
Les connexions SSE declarees perdues sont fermee et leurs ressources liberees.

### 5. Journalisation
Chaque evenement de keepalive, deconnexion ou reconnexion est consigne dans les logs du gateway.
