---
type: SKILL
version: "1.0.0"
status: active
date: "2026-10-25"
intent_hash: 0xSKILL_VSM_20261025
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/vscode-storage-memento-inspector/SKILL.md
---

# Skill — vscode-storage-memento-inspector

## Objectif

Forensic et remédiation directe de la base SQLite `state.vscdb` sous `workspaceStorage/<hash>/`. Détecter et purger la clé `memento/webviewView.kilo-code.SidebarProvider` lorsque les `sidebarSessionTabIDs` référencent des sessions fantômes ou détruites, brisant la boucle de crash au redémarrage de VS Code. Couche Persistance SQLite Memento.

## Déclencheur

- Interface agent blanche après rechargement de fenêtre VS Code.
- Exception React réinjectée au démarrage via `state.vscdb`.
- Reload VS Code inopérant car l'état corrompu persiste dans Memento.

## Entrées

- `vscode_storage_root`: chemin vers le dossier `workspaceStorage` de VS Code (défaut : `%APPDATA%\Code\WorkspaceStorage` ou `%USERPROFILE%\.vscode\Workspaces`).
- `target_key`: clé Memento à inspecter (défaut : `memento/webviewView.kilo-code.SidebarProvider`).
- `dry_run`: mode lecture seule sans modification (défaut : true).

## Sorties

- Rapport JSON des bases `state.vscdb` trouvées et de leur contenu Memento.
- Détection des sessions fantômes dans `sidebarSessionTabIDs`.
- Clé purgée (si `dry_run: false`).
- Entrée WAL NEXUS horodatée.

## Règles

### 1. Découvrir les bases state.vscdb

- Scanner récursivement `vscode_storage_root` pour tous les fichiers `state.vscdb`.
- Pour chaque base, ouvrir en lecture seule avec `sqlite3` (mode URI `?mode=ro` pour éviter le verrou WAL).

### 2. Lire la clé Memento cible

- Requête SQL : `SELECT value FROM ItemTable WHERE key = 'memento/webviewView.kilo-code.SidebarProvider'`.
- Parser le contenu JSON de la valeur.
- Extraire `sidebarSessionTabIDs`.

### 3. Détecter les sessions fantômes

- Comparer chaque UUID dans `sidebarSessionTabIDs` avec les sessions actives connues (depuis `agent-manager.json` si accessible).
- Marquer comme fantôme tout UUID sans session correspondante.

### 4. Purger la clé corrompue (uniquement si dry_run: false)

- Requête SQL : `DELETE FROM ItemTable WHERE key = 'memento/webviewView.kilo-code.SidebarProvider'`.
- Vérifier le verrou WAL : si la base est verrouillée, attendre et réessayer (max 3 tentatives).
- Sauvegarder le fichier `.vscdb` avant suppression (`.bak` avec horodatage).

### 5. Gestion des verrous WAL

- Utiliser `PRAGMA journal_mode=WAL` en lecture.
- En cas de `database is locked`, attendre 2 s et réessayer.
- Ne jamais forcer la suppression d'une base verrouillée par un processus actif.

## Script d'investigation

`scripts/inspect.py` — voir ci-dessous (Python autonome avec sqlite3).

## Tests

- `tests/test_vscode_storage_memento_inspector.py` — créer un `state.vscdb` de test avec clé corrompue, vérifier la détection et la purge.

## Probes

- Zéro clé `memento/webviewView.kilo-code.SidebarProvider` contenant des sessions fantômes après purge.
- Redémarrage VS Code sans exception React réinjectée.

## WAL NEXUS

```
[WAL_NEXUS] skill=vscode-storage-memento-inspector action=inspect timestamp=<ISO> db_path=<PATH> key=<KEY> ghosts=<n>
[WAL_NEXUS] skill=vscode-storage-memento-inspector action=purge timestamp=<ISO> db_path=<PATH> key=<KEY> dry_run=<bool> status=<OK|FAIL>
```

## Référence ADR

- **ADR** : ADR-2026-05-14-004-KILO-CODE-HOTL-OPERATIONAL-STD
- **IntentHash** : 0xB05F1124CDC61605
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed
