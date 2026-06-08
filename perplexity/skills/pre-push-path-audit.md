---
name: pre-push-path-audit
description: "Verification d'integrite local↔remote avant tout push API cross-repo. Detecte les remotes incoherents, les clones orphelins, les path mal places. Utiliser en debut de toute session multi-repo ou avant create_branch/push_files/create_or_update_file via API GitHub."
version: "1.0.0"
triggers:
  - "push vers gerivdb/*"
  - "create_branch"
  - "create_or_update_file via API"
  - "clone d'un repo"
  - "deplacement de repo"
  - "debut session multi-repo"
layer: "L4_ORCHESTRATION"
nexusTags: ["CONFORME_NEXUS", "PRE_PUSH", "INTEGRITY"]
status: "active"
changelog:
  - {v: "1.0.0", date: "2026-06-07", notes: "Creation — remede L1/L10 ADR MC-RNN closure"}
prerequisites:
  - "Acces a known_repositories.yaml (GOVERNANCE-HUB)"
  - "Acces a repo-matrix.json (scripts/)"
  - "git remote -v fonctionnel sur les clones locaux"
slotWeight: 1
trit_primitive: TritCheckConfig
---

# PRE-PUSH-PATH-AUDIT — Verification d'integrite local↔remote

## Domaine et perimetre

Ce skill verifie que **le clone local pointe vers le bon remote** avant toute operation d'ecriture via l'API GitHub. Il detecte :
- Remotes incoherents (ex: clone LYCOS pointant vers VERSUS)
- Clones deja existants (evite les doublons)
- Paths mal places (ex: repo L4 dans TOOLS au lieu de L4-TOOLS)
- Repos dans le SOT mais absents du disque

Cree comme remede aux lacunes L1 et L10 de la session MC-RNN (ADR `adr-mc-rnn-closure-20260607.md`).

## Methodologie

### Phase 1 — Decouverte des repos du perimetre

Depuis le contexte de la session, lister les repos GitHub concernes. Pour chaque repo, recuperer :
- `full_name` depuis `known_repositories.yaml`
- `local_path` depuis `scripts/repo-matrix.json`

### Phase 2 — Verification remote

Pour chaque repo, executer dans le clone local :
```bash
git -C "<local_path>" remote -v
```

Comparer le remote `origin` avec l'attendu :
- Si le clone local n'existe PAS → signaler "CLONE MANQUANT"
- Si le remote ne correspond PAS au `full_name` attendu → **BLOQUER** et signaler le delta
- Si le path local ne correspond pas a la strate attendue (L4-TOOLS, L0-CANON, etc.) → signaler "MAUVAISE STRATE"

### Phase 3 — Verification anti-doublon

Avant de creer un nouveau clone :
```powershell
Get-ChildItem -Path "D:\DO\WEB" -Directory -Recurse -Depth 2 | Where-Object { Test-Path "$_\.git\config" } | ForEach-Object { git -C $_.FullName remote -v }
```
Si un clone du meme repo existe deja (meme remote) → utiliser celui-ci, ne PAS creer de doublon.

### Phase 4 — Rapport

```
[PRE_PUSH_AUDIT] Resultat : OK | FAIL
[PRE_PUSH_AUDIT] Repos verifies : N
[PRE_PUSH_AUDIT] Erreurs : <liste>
[PRE_PUSH_AUDIT] Clone orphelins detectes : <liste>
```

## Regles de decision

- **Regle 1** : Si remote incoherent → STOP, corriger le remote AVANT tout push
- **Regle 2** : Si clone existe deja avec le bon remote → le reutiliser, ne pas cloner
- **Regle 3** : Si path mauvaise strate → deplacer le repo AVANT de travailler
- **Regle 4** : Si repo dans SOT mais pas sur disque → signaler comme MANQUANT

## Format de sortie

```markdown
## Pre-Push Path Audit — [DATE]

| Repo | Path local | Remote | Statut |
|------|------------|--------|--------|
| gerivdb/LYCOS | D:\...\L4-TOOLS\LYCOS | gerivdb/LYCOS | OK |
| gerivdb/CodeDB-E5620 | D:\...\CodeDB-E5620 | gerivdb/CodeDB-E5620 | OK |

Resultat : [OK | FAIL]
```

## Integration avec l'ecosysteme

- **Declencheur** : Tout debut de session multi-repo, tout push API
- **Dependances** : known_repositories.yaml, repo-matrix.json
- **Tags NEXUS** : [CONFORME_NEXUS], [PRE_PUSH], [INTEGRITY]
- **ADR reference** : adr-mc-rnn-closure-20260607.md (lacunes L1, L10)
