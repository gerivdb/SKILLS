---
name: branch-protection-config
description: "Configure branch protection rules, required reviews, status checks via gh CLI"
triggers:
  - /branch-protection
  - protect branch
  - branch protection rules
  - required reviews
  - status checks
  - prevent force push
domain: foundational
version: "1.0.0"
author: gerivdb
license: MIT
status: active
created: 2026-06-06
updated: 2026-06-06
tags:
  - git
  - branch
  - protection
  - github
  - policy
phi_weight: 0.004
---

# Branch Protection Config Skill

> **IntentHash**: `0xBRANCH_PROTECTION_CONFIG_SKILL_20260606`
> **Version**: 1.0.0
> **Domain**: foundational
> **Type**: foundational
> **Status**: active

---

## Synopsis

Configures branch protection rules via GitHub API. Prevents deletion of protected branches.

---

## Triggers

- `/branch-protection check <branch>` — Check protection status
- `/branch-protection set <branch>` — Set protection rules
- `protect branch` — Interactive mode
- `prevent force push` — Block force push on branch

---

## Workflow

### Check Protection

```powershell
gh api repos/{owner}/{repo}/branches/{branch}/protection
```

### Set Protection

```powershell
# Require PR reviews
gh api repos/{owner}/{repo}/branches/main/protection \
  --method PUT \
  --input - <<< '{
    "required_pull_request_reviews": {
      "required_approving_review_count": 1
    },
    "enforce_admins": true,
    "required_status_checks": null,
    "restrictions": null
  }'
```

### Delete Protected Branch (with warning)

```powershell
# Check protection first
$protected = gh api repos/{owner}/{repo}/branches/{branch}/protection 2>$null
if ($protected) {
    Write-Output "WARNING: Branch {branch} is protected. Deletion may fail."
    Write-Output "Disable protection first or use --force"
}
```

---

## Examples

### Example 1: Check Protection

```powershell
/branch-protection check main
# → Shows protection rules for main
```

---

## Dependencies

- **Depends on**: None
- **Provides to**: `sync-branches`

---

## Changelog

| Version | Date | Change | IntentHash |
|---------|------|--------|------------|
| 1.0.0 | 2026-06-06 | Initial version | `0xBRANCH_PROTECTION_CONFIG_SKILL_20260606` |
