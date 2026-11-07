---
name: naming-convention-enforcer
description: Vérifie et applique les conventions de nommage des fichiers, dossiers et skills dans L4-TOOLS\SKILLS, L3-CITIZENS\CITIZENS et L3-CITIZENS\LOOPX. Utilise ce skill quand tu dois auditer ou corriger le respect des conventions de nommage (kebab-case, snake_case, préfixes, suffixes).
version: 1.0.0
intent_hash: 0xSKILL_NAMING_CONVENTION_ENFORCER_20261105
citizen: L2-PLATFORM
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: skills/naming-convention-enforcer/SKILL.md
---

# Skill — naming-convention-enforcer

## Objectif

Garantir la cohérence des noms de fichiers, dossiers, skills et routines selon les conventions de nommage établies dans l'écosystème GeriCode / L2-PLATFORM.

## Déclencheur

- Avant création d'un nouveau skill ou routine
- Audit mensuel de cohérence de nommage
- Après import de fichier externe
- Quand des noms non conformes sont détectés (majuscules, espaces, caractères spéciaux)

## Prérequis

- Accès en lecture aux répertoires cibles
- Accès en écriture pour les corrections (avec confirmation HITL)
- PowerShell 5.1+ ou Python 3

## Conventions de nommage

| Élément | Convention | Exemple valide | Exemple invalide |
|---------|------------|----------------|------------------|
| Skill (dossier) | `kebab-case`, lowercase | `cache-cleaner`, `process-hygiene` | `CacheCleaner`, `cache_cleaner` |
| Routine LOOPX | `kebab-case`, lowercase | `daily-maintenance`, `session-boot` | `DailyMaintenance`, `daily_maintenance` |
| Citizen (dossier) | `kebab-case`, lowercase | `gerivdb-citizen`, `kilo-agent` | `GerivdbCitizen` |
| Fichier SKILL.md | Exact | `SKILL.md` | `skill.md`, `Skill.md` |
| Fichier de config | `kebab-case` ou `snake_case` | `mission_queue.yaml`, `LOOPX_CONFIG.yaml` | `MissionQueue.yaml` |
| Fichier de log | `kebab-case` + `.log` | `interception-log.txt`, `daily-maintenance.log` | `InterceptionLog.txt` |
| Fichier Python | `snake_case` | `engine.py`, `cache_cleaner.py` | `Engine.py`, `cacheCleaner.py` |
| Fichier PowerShell | `kebab-case` + `.ps1` | `daily-maintenance.ps1`, `clean-temp.ps1` | `DailyMaintenance.ps1` |
| Branche Git | `type/description` | `feat/`, `fix/`, `maint/` | `feature/`, `hotfix/` sans slash |

## Protocole

### Étape 1 — Audit de nommage

```powershell
# Vérifier les dossiers de skills non conformes (pas de kebab-case)
Get-ChildItem -Path <repo>\SKILLS -Directory | 
  Where-Object { $_.Name -match '[A-Z_]|[^a-z0-9-]' } |
  Select-Object Name, FullName
```

### Étape 2 — Rapport d'anomalies

Lister chaque élément non conforme avec sa règle violée et la suggestion de correction.

### Étape 3 — Correction (avec HITL)

Renommer les éléments non conformes après confirmation :

```powershell
Rename-Item -Path "<ancien>" -NewName "<nouveau>"
```

### Étape 4 — Mise à jour des références

Mettre à jour tous les chemins référencés dans les fichiers de configuration, SKILL.md, et registres.

### Étape 5 — Logging NEXUS/WAL

```json
{
  "timestamp": "2026-11-05T00:00:00Z",
  "event_type": "naming_convention_enforcement",
  "intent_hash": "0xSKILL_NAMING_CONVENTION_ENFORCER_20261105",
  "data": {
    "anomalies_found": 5,
    "renamed": [
      {"from": "OldSkill", "to": "old-skill", "type": "folder"}
    ],
    "references_updated": [],
    "wal_logged": true
  }
}
```

## Règles d'application

1. **Dry-run par défaut** : lister les anomalies avant correction
2. **Confirmation HITL** obligatoire pour tout renommage
3. **Ne jamais renommer** `.git`, `.kilo`, `node_modules`
4. **Ne jamais renommer** un fichier sans mettre à jour ses références
5. **Conserver** la casse des extensions (`.md`, `.py`, `.ps1`, `.yaml`, `.json`)

## Sortie standard

```yaml
elements_scanned: 120
anomalies_found: []
renamed: []
references_updated: []
protected_skipped: []
errors: []
recommendations: []
```

## Anti-patterns bloquants

- Renommer `.git`, `.kilo`, `node_modules`
- Renommer sans confirmation HITL
- Oublier de mettre à jour les références de chemin
- Utiliser des majuscules ou espaces dans les noms de dossiers
- Négliger le logging WAL après correction

## Intégration

- **GeriCode** : `scripts/verify-agent-manager-env.ps1`
- **LOOPX** : `.kilo/orchestrator/daily-maintenance.ps1`
- **CITIZENS** : `scripts/enforce-naming.ps1`

## Référence ADR

- **ADR** : ADR-2026-08-09-001-NAMING_CONVENTION
- **IntentHash** : 0xSKILL_NAMING_CONVENTION_ENFORCER_20261105
- **Dépôt** : gerivdb/GeriCode
- **Statut ADR** : proposed