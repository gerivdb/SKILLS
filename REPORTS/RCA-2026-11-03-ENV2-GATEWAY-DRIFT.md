---
type: REPORT
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xRCA_20261103_ENV2_GATEWAY_DRIFT
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: REPORTS/RCA-2026-11-03-ENV2-GATEWAY-DRIFT.md
---

# Rapport d Incident - RCA-2026-11-03-ENV2-GATEWAY-DRIFT

## AUDIT - Contexte et constats

### Incident
Crash au demarrage du serveur gateway-manager (Uvicorn/ASGI) sur ENV2 (HP Z600, double Xeon E5620, 24 Go DDR3 ECC), suite a une mise a jour silencieuse de paquets tiers tires par les extensions MCP.

### Symptomes observes
- TypeError: ... got an unexpected keyword argument, localisation super().__init__() dans site-packages (fastapi/routing.py appelant starlette.routing.Router.__init__ avec on_startup=...).
- Crash immediat a linstanciation de APIRouter et des modeles de donnees, alors que le code source utilisateur ne contient pas le parametre incrimane.
- Accumulation de demons et verrouillage temporaire de ports / socket (syndrome de la relance aveugle).

### Severite
Bloquante - arret du service gateway, indisponibilite du routage MCP JSON-RPC 2.0.

## DESIGN - Causes racines

### C1 - Rupture binaire de signature transitive
fastapi 0.109.0 appelle super().__init__(on_startup=...) sur la classe mere starlette.routing.Router. Starlette 1.9.0 (pousse silencieusement par les packages MCP) a supprime ce parametre. Incompatibilite de version entre le parent (FastAPI) et sa sous-bibliotheque (Starlette).

### C2 - Absence de protocole disolation statique avant relance
Aucun test dimport statique en memoire (sans effet de bord) n etait execute avant le demarrage du serveur ASGI. Relance aveugle : le serveur etait demarre pour "voir si ca demarre", exposant le port reseau avant validation du code.

### C3 - Accumulation de demons et verrouillage de ports
Plusieurs instances du gateway tournent en parallele sur Windows. TCPServer pose SO_REUSEADDR par defaut ; sous Windows cela autorise le bind multiple silencieux (zombie port holder). Un demon zombie repondait aux health checks, bloquant le redemarrage.

## PROPOSITION - Skills d immunisation deploies

Quatre skills methodologiques ont ete crees et commites dans D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS (couche L4-TOOLS) :

| Skill | Intent Hash | Role d immunisation | Fichier |
|-------|-------------|---------------------|---------|
| python-dependency-drift-sentinel | 0xSKILL_PDDS_20261103 | Traitement des conflits de signatures transitives (FastAPI vs Starlette) | SKILL.md |
| python-package-integrity-prober | 0xSKILL_PPIP_20261103 | Detection de corruption physique dans site-packages (fichiers __init__.py manquants, dossiers orphelins ~*) | SKILL.md |
| mcp-gateway-protocol-harmonizer | 0xSKILL_MGPH_20261103 | Garantie de conversion universelle JSON-RPC 2.0 (tools/list, initialize, tools/call) pour tout transport | SKILL.md |
| daemon-preflight-import-sentinel | 0xSKILL_DPIS_20261103 | Regle absolue Zero-Daemon Before Zero-Error : pre-vol statique obligatoire avant tout demarrage reseau | SKILL.md |

### Mappage Skill <- Cause racine
- C1 -> python-dependency-drift-sentinel : audit de rupture de signature, verification pip check, reconciliation contractuelle.
- C2 -> daemon-preflight-import-sentinel : purge cache bytecode, test dimport statique unitaire, autorisation de demarrage conditionnee.
- C3 -> daemon-preflight-import-sentinel + mcp-gateway-protocol-harmonizer : preflight singleton (verification /health avant bind), fingerprint dinstance, gestion gracieuse des backends non demarres.

## VALIDATION - Preuves et etat

### Preuves systeme
- 4 dossiers SKILL.md physiquement crees sur le disque (tailles : 2868, 2504, 2713, 2782 octets).
- Frontmatter YAML conforme : type: SKILL, version: "1.0.0", status: active, date, intent_hash, layer: L4-TOOLS, author, source_repo, source_path.
- Structure documentaire standardisee : Objectif, Declencheurs, Entrees, Sorties, Regles Operationnelles.

### Preuves Git (ENV0)
- Commit 8e2b2a9 : feat(skills): ajouter 3 skills d immunisation Python/MCP (PDDS, PPIP, MGPH) - 3 fichiers.
- Commit 963bcc6 : feat(skills): ajouter skill daemon-preflight-import-sentinel (DPIS) - 1 fichier.
- Push e429e3d..963bcc6 main -> main sur https://github.com/gerivdb/SKILLS.git (4 guards BRGS pre-push OK).

### Verification post-commit
- Pre-commit encoding check passe (em-dash U+2014 remplaces par tirets ASCII dans les 4 titres).
- Max 3 fichiers par commit respecte (2 commits atomiques pour 4 skills).
- Pas de git push --force ; push fast-forward valide.

### Statut de l incident
CLOTURE - immunisation mise en place. Les 4 skills sont reutilisables par KiloCode et les agents du systeme pour prevenir la recurrence de cet incident.


