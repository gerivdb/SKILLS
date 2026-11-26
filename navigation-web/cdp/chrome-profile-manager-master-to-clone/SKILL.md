---
name: chrome-profile-manager-master-to-clone
description: Gestion Chrome Pattern A Master-to-Clone (profil maître protégé, clones isolés, locks nettoyés, ports dédiés, multi-instance) via Profile Manager.
---
# chrome-profile-manager-master-to-clone

## Rôle
Orchestrer des instances Chrome/Chromium **attachables CDP** en **Pattern A (Master-to-Clone)** : le profil maître n’est jamais utilisé directement ; chaque tâche/clone reçoit un `--user-data-dir` isolé.

## Règles
- **R5 / Master guard** : interdiction de créer/utiliser/supprimer le profil maître (`409` attendu côté API en cas de tentative).
- **Clones** : copie/instanciation vers `M3-PROFILE\clones\<clone_id>` (ou chemin dédié), args explicites (`--remote-debugging-port`, `--user-data-dir`, `--profile-directory`, `--remote-allow-origins=*`, flags no-first-run).
- **Locks** : nettoyage `SingletonLock/Socket/Cookie` avant lancement si résiduels.
- **Multi-instance** : ports dédiés par clone, PIDs distincts, isolation CDP.
- **TTL/watchdog** : expiration contrôlée, violations journalisées (`POST /violations`), WAL events.

## API/outil
- `scripts/profile_manager.py`, `scripts/profile_manager_api.py` (ex. `127.0.0.1:8244`), `chrome_instances.json`.
- Recompute statut depuis PID/port réel ; adoption du propriétaire réel du port si `--user-data-dir` conforme ; `rogue` si non conforme.

## HITL / limites
- Lancement/kill navigateur et actions humaines (login) selon politique ; REF-216 attach-only pour GeriCode.
