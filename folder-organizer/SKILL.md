---
name: folder-organizer
description: Organise et range l'arborescence des dossiers dans L4-TOOLS\SKILLS, L3-CITIZENS\CITIZENS et L3-CITIZENS\LOOPX selon une taxonomie de maintenance. Utilise ce skill quand tu dois structurer, renommer ou déplacer des dossiers pour améliorer la lisibilité et la maintenabilité.
version: 1.0.0
intent_hash: 0xSKILL_FOLDER_ORGANIZER_20261105
citizen: L2-PLATFORM
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: skills/folder-organizer/SKILL.md
---

# Skill — folder-organizer

## Objectif

Maintenir une arborescence cohérente et prévisible en organisant les dossiers selon une taxonomie de maintenance (scripts, outils, tests, docs, archives, logs, cache, etc.) appliquée aux trois répertoires cibles.

## Déclencheur

- Arborescence devenue illisible (> 50 dossiers à la racine)
- Après ajout massif de skills ou de routines
- Avant archivage ou transfert de repo
- Quand des fichiers sont éparpillés à la racine sans dossier de destination

## Prérequis

- Accès en lecture et écriture aux répertoires cibles
- Connaissance de la taxonomie cible
- Plan de déplacement validé (dry-run obligatoire)

## Taxonomie de maintenance par répertoire

### L4-TOOLS\SKILLS

| Catégorie | Dossier cible | Contenu |
|-----------|---------------|---------|
| Skills actifs | `<nom-du-skill>/` | SKILL.md + scripts |
| Hygiène git | `*hygiene*`, `*auditor*`, `*cleaner*` | Nettoyage git |
| Hygiène processus | `*process*`, `*reaper*`, `*zombie*` | Processus orphelins |
| Registres | `*registry*`, `*sync*`, `*prune*` | Registres |
| M3-Tree | `m3-*` | Primitives M3 |
| Tests | `tests/` | Tests unitaires |
| Scripts | `scripts/` | Scripts PowerShell/Python |
| Config | `config/` | Fichiers de configuration |
| Archives | `archive/`, `archived/` | Skills archivés |

### L3-CITIZENS\CITIZENS

| Catégorie | Dossier cible | Contenu |
|-----------|---------------|---------|
| Citoyens | `citizens/` | Définitions de citoyens |
| Config | `config/` | Configuration |
| Scripts | `scripts/` | Scripts |
| Templates | `templates/` | Modèles |
| ADR | `ADR/` | Décisions d'architecture |
| INTENTS | `INTENTS/` | Intentions |
| PRD | `PRD/` | Spécifications |

### L3-CITIZENS\LOOPX

| Catégorie | Dossier cible | Contenu |
|-----------|---------------|---------|
| Core | `core/` | Moteur LOOPX |
| Routines | `routines/` | Routines définies |
| Scripts | `scripts/` | Scripts d'exécution |
| Config | `config/` | Configuration LOOPX |
| Tests | `tests/` | Tests |
| Data | `data/` | Données |
| Logs | `logs/` | Journaux |

## Protocole

### Étape 1 — Inventaire de l'arborescence actuelle

```powershell
Get-ChildItem -Path <repo> -Directory | Select-Object Name, FullName, (Get-ChildItem $_.FullName -Recurse -File).Count
```

### Étape 2 — Plan de déplacement (dry-run)

Lister chaque dossier avec sa catégorie cible et son nouveau chemin.

### Étape 3 — Déplacement

```powershell
Move-Item -Path "<ancien_chemin>" -Destination "<nouveau_chemin>"
```

### Étape 4 — Mise à jour des références

Mettre à jour les chemins dans les fichiers de configuration, SKILL.md, et registres qui pointaient vers les anciens emplacements.

### Étape 5 — Logging NEXUS/WAL

```json
{
  "timestamp": "2026-11-05T00:00:00Z",
  "event_type": "folder_organizer_reorganization",
  "intent_hash": "0xSKILL_FOLDER_ORGANIZER_20261105",
  "data": {
    "folders_moved": [
      {"from": "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\old-name", "to": "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\new-name", "category": "hygiene"}
    ],
    "references_updated": [],
    "wal_logged": true
  }
}
```

## Règles d'organisation

1. **Dry-run obligatoire** : présenter le plan avant tout déplacement
2. **Ne jamais déplacer** `.git`, `.kilo`, `node_modules`
3. **Ne jamais déplacer** un dossier contenant des références absolues sans mise à jour
4. **Conserver** une structure plate raisonnable (max 3 niveaux de profondeur)
5. **Documenter** chaque déplacement dans le logging WAL

## Sortie standard

```yaml
folders_scanned: 45
folders_organized: []
folders_kept: []
protected_skipped: []
references_updated: []
errors: []
recommendations: []
```

## Anti-patterns bloquants

- Déplacer `.git`, `.kilo`, `node_modules`
- Déplacer sans dry-run préalable
- Oublier de mettre à jour les références de chemin
- Créer une arborescence trop profonde (> 5 niveaux)
- Négliger le logging WAL après réorganisation

## Intégration

- **GeriCode** : `scripts/verify-agent-manager-env.ps1`
- **LOOPX** : `.kilo/orchestrator/daily-maintenance.ps1`
- **CITIZENS** : `scripts/organize-folders.ps1`

## Référence ADR

- **ADR** : ADR-2026-08-09-001-FOLDER_TAXONOMY
- **IntentHash** : 0xSKILL_FOLDER_ORGANIZER_20261105
- **Dépôt** : gerivdb/GeriCode
- **Statut ADR** : proposed