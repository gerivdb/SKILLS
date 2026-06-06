---
name: conventional-commit-validator
description: "Enforces Conventional Commits specification (feat, fix, docs, chore, refactor, etc.) with commit-msg hook integration"
triggers:
  - /commit-msg
  - conventional commit
  - commit message format
  - validate commit message
  - commit lint
  - commit convention
domain: foundational
version: "1.0.0"
author: gerivdb
license: MIT
status: active
created: 2026-06-06
updated: 2026-06-06
tags:
  - git
  - commit
  - conventional-commits
  - lint
  - hook
phi_weight: 0.006
---

# Conventional Commit Validator Skill

> **IntentHash**: `0xCONVENTIONAL_COMMIT_VALIDATOR_SKILL_20260606`
> **Version**: 1.0.0
> **Domain**: foundational
> **Type**: foundational
> **Status**: active

---

## Synopsis

Validates and enforces the [Conventional Commits](https://www.conventionalcommits.org/) specification. Can be used standalone or installed as a commit-msg hook.

---

## Triggers

- `/commit-msg <message>` — Validate a commit message
- `/commit-msg install` — Install as commit-msg hook
- `conventional commit` — Show format guide
- `validate commit message` — Validate last commit
- `commit lint` — Lint all commits on branch

---

## Conventional Commits Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Allowed Types

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting (no logic change) |
| `refactor` | Code change (neither feat nor fix) |
| `perf` | Performance improvement |
| `test` | Adding/correcting tests |
| `chore` | Build, CI, tooling, misc |
| `ci` | CI/CD changes |
| `build` | Build system changes |
| `revert` | Revert previous commit |

### Rules

1. Type is **required**, lowercase
2. Scope is **optional**, lowercase, in parentheses
3. Description is **required**, max 72 chars, no period at end
4. Use imperative mood: "add" not "added" or "adds"
5. Body is optional, separated by blank line
6. Footer is optional, format: `BREAKING CHANGE: <description>` or `Closes #<issue>`

---

## Workflow

### Validate Message

```powershell
# Validate a message
/commit-msg "feat(mc-rnn): add MC-RNN layer implementation"
# → ✅ VALID

/commit-msg "added MC-RNN layer"
# → ❌ FAIL: missing type, not imperative mood
```

### Install as Hook

```powershell
# Install commit-msg hook
/commit-msg install
# → Creates .githooks/commit-msg with validation logic
# → git config core.hooksPath .githooks
```

### Lint Branch Commits

```powershell
# Check all commits on current branch vs main
git log main..HEAD --oneline | ForEach-Object {
    $msg = ($_ -split ' ', 2)[1]
    # Validate each message
}
```

---

## Validation Regex

```powershell
$pattern = '^(feat|fix|docs|style|refactor|perf|test|chore|ci|build|revert)(\([a-z0-9-]+\))?: .{1,72}$'

function Test-CommitMessage {
    param([string]$message)
    if ($message -match $pattern) {
        return $true
    }
    return $false
}
```

---

## Examples

### Valid Messages

```
feat: add user authentication
fix(api): resolve null pointer in login handler
docs: update README with installation guide
chore(deps): bump numpy from 1.24 to 1.26
feat!: remove deprecated API (BREAKING CHANGE)
fix: correct typo in error message
refactor(core): simplify cache eviction logic
test(mc-rnn): add 35 unit tests for MC-RNN layer
```

### Invalid Messages

```
added user authentication        → missing type, not imperative
FIX: resolve bug                 → type must be lowercase
feat:add user auth               → missing space after colon
feat: Add user authentication.   → don't use period, not imperative
very long description that exceeds the seventy-two character limit for commit messages → too long
```

---

## Dependencies

- **Depends on**: `git-hooks-manager`
- **Provides to**: None

---

## Changelog

| Version | Date | Change | IntentHash |
|---------|------|--------|------------|
| 1.0.0 | 2026-06-06 | Initial version | `0xCONVENTIONAL_COMMIT_VALIDATOR_SKILL_20260606` |
