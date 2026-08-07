---
type: skill
version: "1.0.0"
date: "2026-08-01"
intent_hash: 0xGIT_CHECKPOINT_20260801
status: active
extends: repo-state-auditor
---

# Skill: git-checkpoint

## Purpose
Create cross-repo Git state snapshots for rollback, audit, and synchronization. Extends repo-state-auditor with checkpoint creation.

## Context
Before multi-repo operations (deploy, sync, migration), capture consistent state across all 47 repos.

## Snapshot Contents
Per repo:
- HEAD commit SHA
- Current branch name
- Working tree status (clean/dirty)
- Stash count
- Remote tracking status

## Checkpoint Structure
`
.kilo/checkpoints/
  <timestamp>_<operation_id>/
    manifest.yaml          # list of repos + metadata
    <repo_name>/
      head.sha             # git rev-parse HEAD
      branch.txt           # git branch --show-current
      status.txt           # git status --short
      stash.list           # git stash list
      remote.status        # git status -uno
`

## Operations

### Create Checkpoint
`powershell
python -m tools.git_checkpoint create --operation deploy_v18_6 --repos all
`
- Runs epo-state-auditor first to verify state
- Captures all 47 repos in parallel (5 at a time)
- Stores manifest with timestamp + operation ID

### List Checkpoints
`powershell
python -m tools.git_checkpoint list --last 10
`

### Restore Checkpoint
`powershell
python -m tools.git_checkpoint restore <checkpoint_id> --dry-run
python -m tools.git_checkpoint restore <checkpoint_id> --force
`
- --dry-run: shows what would change
- --force: actually resets each repo to captured HEAD

### Diff Checkpoint
`powershell
python -m tools.git_checkpoint diff <checkpoint_id_1> <checkpoint_id_2>
`
- Shows per-repo differences
- Highlights: new commits, branch changes, working tree drift

## Integration
- Called by plix deploy before deployment
- Called by plix sync before cross-repo sync
- Called by cfmi-scanner before pipeline runs

## Anti-patterns
- Creating checkpoint without running repo-state-auditor first
- Restoring without --dry-run verification
- Not cleaning old checkpoints (> 30 days)
- Checkpointing only subset of affected repos

## References
- Base: repo-state-auditor (skill)
- S-008: cross-repo-validator (skill)
- D-006: git-engineering (design)
- ATOM-066: git-engineering
