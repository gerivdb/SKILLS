---
name: network-resilient-sync
description: "Network-resilient git sync: pre-checks reachability, retry with backoff, offline mode, queued pushes"
triggers:
  - /sync
  - git sync
  - network sync
  - offline sync
  - retry push
  - remote unreachable
domain: foundational
version: "1.0.0"
author: gerivdb
license: MIT
status: active
created: 2026-06-06
updated: 2026-06-06
tags:
  - git
  - network
  - sync
  - resilience
  - offline
phi_weight: 0.004
---

# Network Resilient Sync Skill

> **IntentHash**: `0xNETWORK_RESILIENT_SYNC_SKILL_20260606`
> **Version**: 1.0.0
> **Domain**: foundational
> **Type**: foundational
> **Status**: active

---

## Synopsis

Provides network-resilient git synchronization. Pre-checks remote reachability, implements retry with exponential backoff, and queues push operations for later execution.

---

## Triggers

- `/sync` — Network-resilient sync
- `git sync` — Same as above
- `offline sync` — Sync in offline mode
- `retry push` — Retry failed push
- `remote unreachable` — Handle unreachable remote

---

## Workflow

### Pre-Check Reachability

```powershell
# Quick reachability check (10s timeout)
$reachable = $false
try {
    git ls-remote --heads origin 2>$null | Out-Null
    if ($LASTEXITCODE -eq 0) { $reachable = $true }
} catch { }

if (-not $reachable) {
    Write-Output "WARNING: Remote unreachable. Switching to offline mode."
}
```

### Retry with Backoff

```powershell
$maxRetries = 3
$delay = 2
for ($i = 0; $i -lt $maxRetries; $i++) {
    git push origin <branch> 2>$null
    if ($LASTEXITCODE -eq 0) { break }
    Write-Output "Push failed, retrying in ${delay}s..."
    Start-Sleep -Seconds $delay
    $delay *= 2  # exponential backoff
}
```

### Offline Mode

```powershell
# If remote unreachable, queue push operations
$queueFile = ".git/push-queue.json"
$queue = @()
if (Test-Path $queueFile) {
    $queue = Get-Content $queueFile | ConvertFrom-Json
}
$queue += @{ branch = $branch; timestamp = Get-Date }
$queue | ConvertTo-Json | Set-Content $queueFile
Write-Output "Push queued for later execution"
```

### Flush Queue

```powershell
# When network is back
$queue = Get-Content ".git/push-queue.json" | ConvertFrom-Json
foreach ($item in $queue) {
    git push origin $item.branch
}
Remove-Item ".git/push-queue.json"
```

---

## Examples

### Example 1: Resilient Sync

```powershell
/sync
# → Checks reachability, syncs or queues
```

---

## Dependencies

- **Depends on**: None
- **Provides to**: `sync-branches`

---

## Changelog

| Version | Date | Change | IntentHash |
|---------|------|--------|------------|
| 1.0.0 | 2026-06-06 | Initial version | `0xNETWORK_RESILIENT_SYNC_SKILL_20260606` |
