---
name: profile-manager-api-ops
description: Opérations API Profile Manager (8244) — endpoints, garde-fous R5/B7/B9, encodage M2, et tests T1-T6.
---
# profile-manager-api-ops

Contrat opérationnel de l’API Profile Manager (cockpit Pattern A, attach-only REF-216).

## Endpoints (service `127.0.0.1:8244`)
- `GET /health` — liveness/service.
- `GET /profiles` — liste (statut recomputé).
- `GET /profiles/{id}` — détail (si exposé).
- `POST /profiles` — création clone (`task`, `port`, `ttl_s`).
- `DELETE /profiles/{id}` — arrêt + suppression clone/répertoire + **purge entrée** (B9).
- `GET /violations`, `POST /violations` — registre violations.
- `GET /profiles/{id}/logs` (SSE) — flux logs (si exposé).

## Garde-fous
- **R5 master-guard** : refus (409) de création/utilisation/suppression ciblant le profil maître.
- **R4 kill physique** : terminaison process via `taskkill /F /T /PID` (Windows) avec vérification sortie.
- **B7 adoption** : `_compute_instance_status` recompute le statut réel à chaque `GET /profiles` (PID/port/owner, adoption du propriétaire réel si `--user-data-dir` conforme, marquage `rogue` sinon).
- **B9 purge** : `DELETE` retire l’entrée persistée (pas de résidu `stopped` dans `chrome_instances.json`).

## Encodage (M2)
- Appels `subprocess.run(..., encoding="utf-8", errors="replace")` pour `tasklist`/`taskkill`/commandes texte afin d’éviter les crashs de décodage console.

## Tests (T1–T6, voir `PROFILE_COCKPIT_DEPLOYMENT_REPORT.md`)
- T1 health, T2 list/create, T3 isolation multi-ports/PIDs, T4 delete/kill+purge, T5 R5 master 409, T6 recompute/adoption/violations (selon couverture rapport).

## Références
- `chrome-profile-manager-master-to-clone`, `hotl-autonomy-boundary-guard`.
- Runtime : `scripts/profile_manager.py`, `scripts/profile_manager_api.py`, `e2e_output/chrome_instances.json`.