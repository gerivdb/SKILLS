---
name: wal-reconciler
description: "Validates WAL integrity against actual git state, detects orphaned entries, compacts old entries"
triggers:
  - /wal-reconcile
  - wal integrity
  - wal validation
  - wal compact
  - wal audit
  - wal vs git
domain: foundational
version: "1.0.0"
author: gerivdb
license: MIT
status: active
created: 2026-06-06
updated: 2026-06-06
tags:
  - wal
  - git
  - integrity
  - reconciliation
  - audit
phi_weight: 0.006
---

# WAL Reconciler Skill

> **IntentHash**: `0xWAL_RECONCILER_SKILL_20260606`
> **Version**: 1.0.0
> **Domain**: foundational
> **Type**: foundational
> **Status**: active

---

## Synopsis

Validates WAL (Write-Ahead Log) integrity against actual git state. Detects orphaned entries, truncates corrupted tails, compacts old entries.

---

## Triggers

- `/wal-reconcile` — Full WAL reconciliation
- `/wal-audit` — Audit WAL integrity only
- `/wal-compact` — Compact old WAL entries
- `wal integrity` — Same as /wal-reconcile
- `wal vs git` — Compare WAL to git state

---

## Workflow

### Read WAL

```powershell
# WAL is a single-line JSONL file
$wal = Get-Content "global_wal.jsonl" -Raw | ConvertFrom-Json
```

### Validate Each Entry

```powershell
foreach ($entry in $wal) {
    # Check commit exists
    $commitExists = git cat-file -t $entry.commit_sha 2>$null
    if ($commitExists -ne "commit") {
        Write-Output "ORPHANED: $($entry.commit_sha) — commit does not exist"
    }

    # Check branch exists (if referenced)
    if ($entry.branch) {
        $branchExists = git rev-parse --verify $entry.branch 2>$null
        if (-not $branchExists) {
            Write-Output "STALE: branch $($entry.branch) does not exist"
        }
    }
}
```

### Compact WAL

```powershell
# Keep last N entries
$maxEntries = 100
$wal = $wal | Select-Object -Last $maxEntries
$wal | ConvertTo-Json -Compress | Set-Content "global_wal.jsonl"
```

### Truncate Corrupted Tail

```powershell
# If JSONL is corrupted, find last valid line
$content = Get-Content "global_wal.jsonl" -Raw
$lines = $content -split "`n"
$valid = @()
foreach ($line in $lines) {
    try {
        $line | ConvertFrom-Json | Out-Null
        $valid += $line
    } catch {
        Write-Output "CORRUPTED: $line"
    }
}
$valid -join "`n" | Set-Content "global_wal.jsonl"
```

---

## Examples

### Example 1: Full Reconciliation

```powershell
/wal-reconcile
# → Reads WAL, validates each entry, reports orphans
```

---

## Dependencies

- **Depends on**: None
- **Provides to**: `kiva-pr-workflow`

---

## Changelog

| Version | Date | Change | IntentHash |
|---------|------|--------|------------|
| 1.0.0 | 2026-06-06 | Initial version | `0xWAL_RECONCILER_SKILL_20260606` |
