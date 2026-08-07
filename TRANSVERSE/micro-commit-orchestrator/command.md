---
name: micro-commit-orchestrator
description: "Workflow git atomique par ATOM (stage -> commit -> verify -> push)"
version: "1.0.0"
layer: TRANSVERSE
intent_hash: 0xMICRO_COMMIT_ORCHESTRATOR_CMD_20260731
---

# Command: micro-commit-orchestrator

## Usage

```powershell
# Workflow complet ATOM (recommande)
python scripts/commit.py --atom ATOM-062 --files "src/file1.py src/file2.py" --msg "add validation" --intent 0xHASH --refs "ADR-123,INTENT-456"

# Etape par etape
python scripts/commit.py --stage-only --files "src/file1.py"
python scripts/commit.py --commit-only --msg "feat(ATOM-062): add validation"
python scripts/commit.py --verify-only
python scripts/commit.py --push-only

# Verification pre-commit
python scripts/commit.py --check-format --msg "feat(ATOM-062): add validation"
```

## Arguments

| Argument | Requis | Description |
|----------|--------|-------------|
| `--atom` | Oui* | Numero ATOM (ex: ATOM-062) |
| `--files` | Oui* | Fichiers a committer (space-separated) |
| `--msg` | Oui* | Description courte (sans prefixe type) |
| `--type` | Non | Type commit: feat/fix/docs/refactor/test/chore/perf (defaut: feat) |
| `--intent` | Non* | IntentHash (0x...) - requis si decision archi |
| `--refs` | Non | Refs ADR/INTENT/EPIC (comma-separated) |
| `--stage-only` | Non | Seulement git add |
| `--commit-only` | Non | Seulement git commit (requiert --msg) |
| `--verify-only` | Non | Seulement verification post-commit |
| `--push-only` | Non | Seulement git push |
| `--check-format` | Non | Verifier format message sans commit |
| `--branch` | Non | Branche cible (defaut: current) |
| `--dry-run` | Non | Simuler sans executer |

* Requis pour workflow complet (--atom + --files + --msg)

## Format message genere

```
feat(ATOM-062): add validation for atoms.md

IntentHash: 0xATOM_VALIDATION_20260731
Refs: ADR-2026-07-28-020, INTENT-2026-07-28-015
```

## Validations

| Check | Description |
|-------|-------------|
| Format | type(ATOM-XXX): desc |
| Files | <= 3 fichiers |
| IntentHash | Present si --atom fourni |
| Secrets | Scan .kiva/secrets/ |
| Repo | git status clean (hors staged) |

## Codes de sortie

- `0` : ATOM livree (commit + push OK)
- `1` : Echec validation / commit / push
- `2` : Erreur format / repo / args
