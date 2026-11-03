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

# Skill - self-healing-orchestrator

## Objectif
Combo maitre de plus haut niveau : detecte un freeze, revoque le bail, purge la base SQLite, redemarre l'UI et consigne l'incident dans le WAL. Assure la reprise automatique apres une panne ou un blocage du systeme.

## Declencheur
- Un freeze du systeme est detecte (absence de reponse heartbeat)
- Un bail est expire ou bloque
- Une base SQLite est corrompue ou verrouillee
- L'UI ne repond plus et doit etre redemarree
- Un incident de niveau critique necessite une recuperation automatisee

## Entrees
- `incident_id`: identifiant de l'incident detecte
- `freeze_detected`: boolean indiquant un gel du systeme
- `lease_id`: identifiant du bail a revoquer
- `sqlite_path`: chemin de la base SQLite a purger
- `ui_process`: nom du processus UI a redemarrer
- `wal_path`: chemin du journal WAL pour consignation

## Sorties
- `heal_status`: statut de l'auto-guerison (success, partial, failed)
- `lease_revoked`: boolean indiquant la revocation du bail
- `sqlite_purged`: boolean indiquant la purge de la base
- `ui_restarted`: boolean indiquant le redemarrage de l'UI
- `wal_entry_id`: identifiant de l'entree WAL de l'incident

## Protocole d'auto-guerison
1. Detecter le freeze (absence de heartbeat > seuil)
2. Revoquer le bail actif associe
3. Purger la base SQLite (suppression des verrous, nettoyage WAL)
4. Redemarrer le processus UI
5. Consigner l'incident et les actions dans le WAL
6. Notifier le Citoyen habilite

## WAL NEXUS
Chaque incident d'auto-guerison est consigne dans le WAL avec l'identifiant d'incident, les actions effectuees (revocation bail, purge SQLite, redemarrage UI), le statut final et l'horodatage UTC.

## Reference ADR
- **ADR** : ADR-2026-06-28-001-LOGICAL-ARCHITECTURE-N1-N4
- **IntentHash** : 0xSKILL_SELF_HEALING_ORCHESTRATOR_20261025
- **Depot** : gerivdb/SKILLS
- **Statut ADR** : proposed

## Script cible
scripts/heal.ps1
