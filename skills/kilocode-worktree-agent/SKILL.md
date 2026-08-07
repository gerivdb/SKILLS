---
type: skill
version: "1.0.0"
date: "2026-06-08"
intent_hash: 0xKILOCODE_WORKTREE_AGENT_20260608
status: active
---

# Skill: kilocode-worktree-agent

## Purpose
Orchestrate parallel KiloCode Agent Manager sessions using VS Code worktrees for multi-repo batch operations on Z600 (CPU-only, 18 GB RAM).

## Context
KiloCode Agent Manager launches separate KiloCode sessions with their own context. Each session consumes RAM and CPU. On Z600 (2x Xeon E5620, 18 GB DDR3, no GPU), the practical limit is **4 simultaneous agents** before memory pressure.

## Hardware constraints (Z600)

| Resource | Limit | Implication |
|----------|-------|-------------|
| RAM | 18 GB DDR3 | 4 agents x ~3 GB = 12 GB, leaves 6 GB for OS |
| CPU | 8 cores / 16 threads | 4 agents x 2 threads = 8 threads, leaves 8 for OS |
| No GPU | CPU-only inference | SLM Owl Alpha ~200 tokens/sec, prompts must be short (< 200 tokens) |
| Disk | SSD 1 To (C:), SSD 2 To (D:) | Worktrees on D:\, source on C:\DevTools |

## Protocol

### Step 1 - Plan worktree allocation

Group repos by stratum to minimize cross-repo jumps:

```
Worktree 1: L3-CITIZENS repos (CANDIDATOR, IRIS, KRONOS, UAE, strix, GERIBOOKING, BANK-BUSTER, racines)
Worktree 2: L1-INFRA repos (FLUENCE, LLM-REPO, TOPOS, KIVA-CLI)
Worktree 3: L2-PLATFORM repos (GeriCode, KEEL)
Worktree 4: L0-CANON repos (GOVERNANCE-HUB, NEXUS, ONTOLOGY, BRAIN)
```

### Step 2 - Create worktrees

```powershell
# From the main repo
git worktree add ..\WORKTREE-L3-CITIZENS main
git worktree add ..\WORKTREE-L1-INFRA main
git worktree add ..\WORKTREE-L2-PLATFORM main
git worktree add ..\WORKTREE-L0-CANON main
```

### Step 3 - Launch Agent Manager sessions

In VS Code KiloCode:
1. Open each worktree as a separate workspace
2. Launch Agent Manager with `mode: "local"` (not worktree-isolated)
3. Set `maxAgents: 4` in kilo.json

### Step 4 - Write agent prompts (short, < 200 tokens)

Each prompt must be:
- **Atomic**: one task, one expected output
- **Deterministic**: no complex inference, just file operations
- **Verifiable**: output is a file or git commit

Example prompt format:
```
Task: Create STRATUM_RELAY.md in {repo_root}
Source: known_repositories.yaml section P1_STRATEGIC
Output: {repo_root}/STRATUM_RELAY.md with layer + role
Verify: Test-Path {repo_root}/STRATUM_RELAY.md
```

### Step 5 - Monitor and collect results

```powershell
# Check all worktrees completed
foreach ($wt in @("WORKTREE-L3-CITIZENS","WORKTREE-L1-INFRA","WORKTREE-L2-PLATFORM","WORKTREE-L0-CANON")) {
    $changes = git -C "D:\DO\WEB\TOOLS\$wt" diff --stat
    Write-Host "$wt : $changes"
}
```

### Step 6 - Merge and cleanup

```powershell
# Merge each worktree back to main
git merge WORKTREE-L3-CITIZENS --no-ff -m "feat(p12): batch L3-CITIZENS coverage files"

# Remove worktrees
git worktree remove ..\WORKTREE-L3-CITIZENS
git worktree remove ..\WORKTREE-L1-INFRA
git worktree remove ..\WORKTREE-L2-PLATFORM
git worktree remove ..\WORKTREE-L0-CANON
```

## Anti-patterns

- **DON'T** exceed 4 simultaneous agents on Z600 (RAM exhaustion -> silent failures)
- **DON'T** use `mode: "worktree"` for batch operations (creates nested worktrees, confusing)
- **DON'T** write prompts > 200 tokens (SLM context limit on CPU-only)
- **DON'T** skip verification - always check output files exist before merging
- **DON'T** forget to remove worktrees after merge (disk accumulation)

## Prompt design rules for Owl Alpha (Z600)

| Rule | Rationale |
|------|-----------|
| Max 200 tokens per prompt | SLM context window on CPU-only |
| One task per agent | Atomic = verifiable |
| Specify exact file paths | No inference needed |
| Include verification step | Agent self-checks output |
| No nested conditionals | SLM struggles with complex branching |
