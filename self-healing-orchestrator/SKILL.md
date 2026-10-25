---
type: SKILL
name: self-healing-orchestrator
version: "1.0.0"
status: active
date: "2026-10-25"
intent_hash: 0xSKILL_SELF_HEALING_ORCHESTRATOR_20261025
citizen: L4-TOOLS
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/self-healing-orchestrator/SKILL.md
---

# Skill — self-healing-orchestrator

## Objectif
Combo maître de plus haut niveau : détecte un freeze, révoque le bail, purge la base SQLite, redémarre l'UI et consigne l'incident dans le WAL. Assure la reprise automatique après une panne ou un blocage du système.

## Declencheur
- Un freeze du système est détecté (absence de réponse heartbeat)
- Un bail est expiré ou bloqué
- Une base SQLite est corrompue ou verrouillée
- L'UI ne répond plus et doit être redémarrée
- Un incident de niveau critique nécessite une récupération automatisée

## Entrees
- `incident_id`: identifiant de l'incident détecté
- `freeze_detected`: boolean indiquant un gel du système
- `lease_id`: identifiant du bail à révoquer
- `sqlite_path`: chemin de la base SQLite à purger
- `ui_process`: nom du processus UI à redémarrer
- `wal_path`: chemin du journal WAL pour consignation

## Sorties
- `heal_status`: statut de l'auto-guérison (success, partial, failed)
- `lease_revoked`: boolean indiquant la révocation du bail
- `sqlite_purged`: boolean indiquant la purge de la base
- `ui_restarted`: boolean indiquant le redémarrage de l'UI
- `wal_entry_id`: identifiant de l'entrée WAL de l'incident

## Protocole d'auto-guérison
1. Détecter le freeze (absence de heartbeat > seuil)
2. Révoquer le bail actif associé
3. Purger la base SQLite (suppression des verrous, nettoyage WAL)
4. Redémarrer le processus UI
5. Consigner l'incident et les actions dans le WAL
6. Notifier le Citoyen habilité

## WAL NEXUS
Chaque incident d'auto-guérison est consigné dans le WAL avec l'identifiant d'incident, les actions effectuées (révocation bail, purge SQLite, redémarrage UI), le statut final et l'horodatage UTC.

## Reference ADR
- **ADR** : ADR-2026-06-28-001-LOGICAL-ARCHITECTURE-N1-N4
- **IntentHash** : 0xSKILL_SELF_HEALING_ORCHESTRATOR_20261025
- **Depot** : gerivdb/SKILLS
- **Statut ADR** : proposed

## Script cible
scripts/heal.ps1
