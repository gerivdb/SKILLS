---
type: skill
version: "1.0.0"
date: "2026-06-08"
intent_hash: 0xKILOCODE_WORKTREE_AGENT_20260608
status: active
trit_primitive: TritIsolate
tags: [kilo, agent-manager, worktree, parallel, z600]
---

# kilocode-worktree-agent

## Purpose
Orchestrate parallel KiloCode Agent Manager sessions using VS Code worktrees for multi-repo batch operations on Z600 (CPU-only, 24 GB RAM).

## Trigger
Use when: running parallel agents, user mentions "Agent Manager", "worktree", "parallel sessions", "multi-repo batch", or "agent delegation".

## Hardware constraints (Z600)

| Resource | Limit | Implication |
|----------|-------|-------------|
| RAM | 24 GB DDR3 | 4 agents × ~4 GB = 16 GB, leaves 8 GB for OS |
| CPU | 8 cores / 16 threads | 4 agents × 2 threads = 8 threads, leaves 8 for OS |
| No GPU | CPU-only inference | SLM Owl Alpha ~200 tokens/sec, prompts must be short (< 200 tokens) |
| Disk | SSD 1 To (C:), SSD 2 To (D:) | Worktrees on D:\, source on C:\DevTools |

## Steps

### Step 1 — Plan worktree allocation

Group repos by stratum to minimize cross-repo jumps:

```
Worktree 1: L3-CITIZENS repos
Worktree 2: L1-INFRA repos
Worktree 3: L2-PLATFORM repos
Worktree 4: L0-CANON repos
```

### Step 2 — Create worktrees

```powershell
git worktree add ..\WORKTREE-L3-CITIZENS main
git worktree add ..\WORKTREE-L1-INFRA main
git worktree add ..\WORKTREE-L2-PLATFORM main
git worktree add ..\WORKTREE-L0-CANON main
```

### Step 3 — Launch Agent Manager sessions

1. Open each worktree as a separate workspace
2. Launch Agent Manager with `mode: "local"` (not worktree-isolated)
3. Set `maxAgents: 4` in kilo.json

### Step 4 — Write agent prompts (short, < 200 tokens)

Each prompt must be:
- **Atomic**: one task, one expected output
- **Deterministic**: no complex inference, just file operations
- **Verifiable**: output is a file or git commit

Example:
```
Task: Create STRATUM_RELAY.md in {repo_root}
Source: known_repositories.yaml section P1_STRATEGIC
Output: {repo_root}/STRATUM_RELAY.md with layer + role
Verify: Test-Path {repo_root}/STRATUM_RELAY.md
```

### Step 5 — Monitor and collect results

```powershell
foreach ($wt in @("WORKTREE-L3-CITIZENS","WORKTREE-L1-INFRA","WORKTREE-L2-PLATFORM","WORKTREE-L0-CANON")) {
    $changes = git -C "D:\DO\WEB\TOOLS\$wt" diff --stat
    Write-Host "$wt : $changes"
}
```

### Step 6 — Merge and cleanup

```powershell
git merge WORKTREE-L3-CITIZENS --no-ff -m "feat(p15): batch L3-CITIZENS coverage files"
git worktree remove ..\WORKTREE-L3-CITIZENS
```

## Rules
- Never exceed 4 simultaneous agents on Z600
- Always use `mode: "local"` for batch operations
- Always specify exact file paths in prompts
- Always include verification step in prompts
- Always remove worktrees after merge

## Anti-patterns
- Don't exceed 4 simultaneous agents (RAM exhaustion → silent failures)
- Don't use `mode: "worktree"` for batch operations (nested worktrees)
- Don't write prompts > 200 tokens (SLM context limit)
- Don't skip verification — always check output files exist
- Don't forget to remove worktrees after merge
