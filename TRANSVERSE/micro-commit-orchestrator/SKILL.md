---
type: skill
version: "1.0.0"
date: "2026-07-31"
intent_hash: 0xMICRO_COMMIT_ORCHESTRATOR_20260731
status: active
layer: TRANSVERSE
nexusTags: ["GIT", "COMMIT", "ATOM", "ATOMIC", "WORKFLOW"]
scope: ecosystem
guards:
  - agent-budget-check
  - git-remote-safety
  - slm-micro-executor
---

# micro-commit-orchestrator -- Workflow git atomique par ATOM

## But
Orchestr le workflow git complet pour un ATOM unique : stage -> commit -> verify -> push.
Garantit : <= 3 fichiers, <= 30 min, format Conventional Commits + IntentHash + Refs.

## Contexte
SLM local (Z600 : 2xe Xeon E5620, 18 GB DDR3, pas de GPU) :
- Contexte effectif : ~2000 tokens fiables
- Regle d or : 1 ATOM = 1 commit = 1 PR = 1 validation

Ce skill s utilise APRES slm-micro-executor (code pret) pour livrer l ATOM.

## Workflow ATOM (5 etapes atomiques)

```
1. STAGE     : git add <fichiers>           (1 tool call)
2. VALIDATE  : Verifier format commit msg   (1 tool call)  
3. COMMIT    : git commit -m "..."          (1 tool call)
4. VERIFY    : git log --oneline -1         (1 tool call)
5. PUSH      : git push origin <branche>    (1 tool call)
```

## Format commit ATOM

```
<type>(ATOM-<XXX>): <description courte>

[Corps optionnel]

IntentHash: 0x<HASH>
Refs: ADR-XXXX, INTENT-XXXX, EPIC-XXXX
```

Types: feat, fix, docs, refactor, test, chore, perf

## CLI

```powershell
# Workflow complet ATOM
python scripts/commit.py --atom ATOM-062 --files "f1.py f2.py" --msg "feat: add validation" --intent 0xHASH --refs "ADR-123,INTENT-456"

# Etape par etape
python scripts/commit.py --stage-only --files "f1.py f2.py"
python scripts/commit.py --commit-only --msg "feat(ATOM-062): ..."

# Verification pre-push
python scripts/commit.py --verify-only
```

## Validation pre-commit (hooks/)

- Format message: type(ATOM-XXX): desc
- <= 3 fichiers modifies
- IntentHash present (0x...)
- Refs non-vides si decision archi
- Pas de secrets (scan .kiva/secrets/)

## Codes de sortie

- `0` : ATOM livree avec succes
- `1` : Echec validation / commit / push
- `2` : Erreur format / repo
