---
type: SKILL
version: "1.0.0"
status: active
gericode_version: "1.0"
intent_hash: 0xSKILL_CHROMIUM_CDP_COCKPIT_20261120
stratum: L4
shard_id: G
turn_counter: 1
uuid: chromium-extension-cockpit-001
timestamp: "2026-11-20T07:03:00Z"
invariants:
  friction: 0.0
  entropy: 0.0
wal_reference: "WAL-0x243-CDP-COCKPIT-001"
name: chromium-extension-cockpit
description: |
  Pilotage et preuve matérielle d'extensions Chromium via CDP (port 9222).
  Permet de recharger, inspecter, purger les erreurs et prouver l'égalité
  Disque vs Live d'une extension sans geste manuel dans le navigateur.
triggers:
  - "recharger extension"
  - "cdp cockpit"
  - "proof ipa-001"
  - "chromium extension debug"
  - "clear errors extension"
  - "disque vs live version"
workdir: "D:/DO/WEB/TOOLS/L4-TOOLS/SKILLS/chromium-extension-cockpit"
entrypoint: "scripts/chromium_cdp_cockpit.py"
source_repo: gerivdb/SKILLS
---

# Skill : chromium-extension-cockpit

## Objectif

Fournir aux agents LLM (KiloCode, Cline, Antigravity) un ensemble de primitives déterministes pour piloter, déboguer et certifier des extensions Chromium à chaud, sans aucune intervention manuelle dans le navigateur.

## Capacités (via `scripts/chromium_cdp_cockpit.py`)

| Action | Commande | Objectif |
|--------|----------|----------|
| `status` | `python scripts/chromium_cdp_cockpit.py status` | Liste les extensions installées, leurs versions et état d'erreurs |
| `reload` | `python scripts/chromium_cdp_cockpit.py reload --id <ID>` | Rechargement à chaud d'une extension via son ID Chromium |
| `clear-errors` | `python scripts/chromium_cdp_cockpit.py clear-errors --id <ID>` | Purge le journal d'erreurs (Clear All) d'une extension |
| `frames` | `python scripts/chromium_cdp_cockpit.py frames --id <ID>` | Inspecte la hiérarchie iframes d'une extension (panel/popup) |
| `version` | `python scripts/chromium_cdp_cockpit.py version --manifest <path>` | Preuve Disque vs Live (manifest version == runtime version) |

## Règles embarquées (Invariants)

### R-01 — Invariant de Runtime
Toujours vérifier si le port `9222` répond avant toute modification de fichier d'extension.
- Si le port ne répond pas → STOP, demander à l'utilisateur de lancer Chromium avec `--remote-debugging-port=9222`.

### R-02 — Invariant de Chemin
Vérifier que le dossier édité est bien celui qui est monté dans `Secure Preferences` (`extensions.settings.<ID>.path`).
- Ne jamais éditer un fichier dans un dossier qui n'est pas le dossier d'exécution réel chargé par Chrome.

### R-03 — Cycle Reload-Verify Obligatoire
Après toute modification de code (`edit_file` / `write_file`) sur un fichier d'extension :
1. Incrémenter le patch version dans `manifest.json`.
2. Déclencher le rechargement via l'action `reload`.
3. Vérifier par l'action `version` l'égalité `Version_disk == Version_live`.
4. Consulter `clear-errors` puis vérifier `ERRORS REMAINING: []`.

### R-04 — Preuve IPA-001
Toute modification d'extension doit être accompagnée des 3 preuves matérielles :
1. Chemin absolu + contenu brut du fichier modifié.
2. Hash de commit Git (`git rev-parse --short HEAD` + `git show --stat`).
3. Vérification live via CDP (status OK, 0 erreur, version match).

## Utilisation dans VS Code

Les tâches suivantes sont disponibles via `Ctrl+Shift+P` → *Run Task* (fichier `.vscode/tasks.json` dans le dépôt consommateur) :

- **Chromium: Statut Extensions & Erreurs** — voir toutes les extensions et leur état
- **Chromium: Recharger Extension Active** — recharger une extension par son ID
- **Chromium: Purger Journal Erreurs** — purger les erreurs console d'une extension
- **Chromium: Inspecter Iframes Extension** — voir la hiérarchie des iframes
- **Chromium: Preuve Disque vs Live (Version)** — comparer version disque et runtime

## Exemple de cycle de travail déterministe

```
1. Éditer sidekeep-x/manifest.json (bump version 1.0.2 → 1.0.3)
2. Tâche: Chromium: Recharger Extension Active → ID jcobknapiakdmpjadnlhbipeggdkiacj
3. Tâche: Chromium: Purger Journal Erreurs → même ID
4. Tâche: Chromium: Preuve Disque vs Live → manifest sidekeep-x/manifest.json
5. Résultat attendu: match: true, hasErrors: false
```

## Fichiers associés

- `scripts/chromium_cdp_cockpit.py` — script maître CLI
- `SKILL.md` — ce fichier

## Référence ADR

- **ADR** : ADR-ENV2-010 (cadre M3 Tree/Branch pour extensions)
- **IntentHash** : 0xSKILL_CHROMIUM_CDP_COCKPIT_20261120
