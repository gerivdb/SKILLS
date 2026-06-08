---
type: skill
version: "1.0.0"
date: "2026-06-08"
intent_hash: 0xSKILL_TRIT_PATCHER_20260608
status: active
trit_primitive: TritDocumentClassify
tags: [skill, trit, frontmatter, batch, patch]
---

# skill-trit-patcher

## Purpose
Batch patch `trit_primitive` field into skill file frontmatters — close all SKILL_ORPHAN gaps from SGR.

## Trigger
Use when: SGR detects SKILL_ORPHAN gaps, user mentions "trit patch", "skill orphan", "batch frontmatter", or "trit_primitive missing".

## TRIT_MAPPING rules

Infer `trit_primitive` from keyword matches in skill name:

| Keyword in skill name | Assigned trit_primitive |
|----------------------|------------------------|
| argus, monitor, watch, health, probe, tracker | TritObserve |
| audit, check, validate, lint, test | TritCheckConfig / TritRunTests |
| prd, reasoning, adr, governance, decision, decompose | TritDecompose |
| sync, git, workflow, resolver | TritFullSync / TritDocumentTrace |
| scaffold, keel, peg, pipeline, build | TritIsolate |
| hitl, triade, swarm, task, hub, bus | TritNotify |
| security, guard, hardening, recovery, encoding | TritEnforcePolicy / TritQuarantine |
| pruning, optimizer, boinc, z600, pulse, hardware, bench | TritEntropyMeasure |
| diagram, iot, media, infographic, vega, mermaid, uml | TritDocumentCreate |
| base243, ternary | TritTernaryStateRust |
| ide, devtools, github, intent, reformer, compliance, bridge | TritCheckConfig / TritDiscoverArtifact |
| skill, deps | TritDocumentClassify |
| crossref, xref | TritCrossRef |
| blindspot, gap | TritBlindSpot |
| metagov, decision-gate | TritMetaGov |
| ping, health-check | TritPingService |
| deploy, simulation | TritSimulateDeploy |
| rollback, undo | TritRollback |
| rollforward | TritRollforward |
| sign, crypto | TritSignOperation |
| vector-clock, consistency | TritCheckConsistency |
| quantum, resolve | TritResolvePath |
| notify, alert | TritNotify |
| scan, registry | TritScanRegistry |
| french, grammar | TritCheckFrenchGrammar |
| entropy | TritEntropyMeasure |
| compare | TritCompareRegistries |
| enforce, policy | TritEnforcePolicy |
| registration | TritEnforceRegistration |
| classify, classification | TritDocumentClassify |
| register | TritDocumentRegister |
| trace | TritDocumentTrace |
| move, copy | TritDocumentMove |
| purge, cleanup | TritDocumentPurge |
| dependency, deps | TritCheckDependencies |
| path | TritResolvePath |
| run-tests | TritRunTests |
| syntax | TritValidateSyntax |
| config | TritCheckConfig |
| check-encoding | TritCheckEncoding |
| check-consistency | TritCheckConsistency |
| check-deps | TritCheckDependencies |
| check-french | TritCheckFrenchGrammar |
| prerequisites | TritCheckPrerequisites |
| scan-secrets | TritScanSecrets |
| full-sync | TritFullSync |
| verse-sync | TritVerseSync |
| diamond, orchestrate | TritDiamondOrchestrate |
| *(fallback)* | TritObserve |

## Steps

### Step 1 — Dry run

```powershell
python scripts/patch_skill_frontmatter.py `
  --skills-dir D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\perplexity\skills `
  --dry-run
```

Review output. All orphan skills should appear with assigned trits.

### Step 2 — Real run

```powershell
python scripts/patch_skill_frontmatter.py `
  --skills-dir D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\perplexity\skills
```

### Step 3 — Force re-patch (if mapping changed)

```powershell
python scripts/patch_skill_frontmatter.py `
  --skills-dir D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\perplexity\skills `
  --force
```

### Step 4 — Validate with scanner

```powershell
python -m engine.declarative_runner `
  ARGUS/scanners/declared/skill_trit_coverage.yaml `
  skills_dir=D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\perplexity\skills `
  gov_root=D:\DO\WEB\TOOLS\L0-CANON\GOVERNANCE-HUB
```

Expected: score 1.0, SKL-001 healthy (0 orphans).

## Rules
- ONLY use exact names from `TritRegistry.yaml` — never invent trit names
- Always dry-run before modifying existing values
- Check `TritRegistry.yaml` for exact primitive names before assigning

## Anti-patterns
- Don't assign non-TritRegistry names (e.g., `TritDecide`, `TritExpress`, `TritBuild`)
- Don't run without `--dry-run` first when modifying existing values
- Don't forget to check `TritRegistry.yaml` for exact names
