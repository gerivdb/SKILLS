---
name: git-hooks-manager
description: "Create, install, debug, and manage git hooks (pre-commit, pre-push, commit-msg) with templates and testing"
triggers:
  - /hooks
  - git hooks
  - install hooks
  - pre-commit hook
  - pre-push hook
  - commit-msg hook
  - hook management
  - debug hooks
domain: foundational
version: "1.0.0"
author: gerivdb
license: MIT
status: active
created: 2026-06-06
updated: 2026-06-06
tags:
  - git
  - hooks
  - pre-commit
  - pre-push
  - automation
phi_weight: 0.006
---

# Git Hooks Manager Skill

> **IntentHash**: `0xGIT_HOOKS_MANAGER_SKILL_20260606`
> **Version**: 1.0.0
> **Domain**: foundational
> **Type**: foundational
> **Status**: active

---

## Synopsis

Creates, installs, debugs, and manages git hooks. Provides templates for common hooks (pre-commit, pre-push, commit-msg) and validates hook health.

---

## Triggers

- `/hooks install` — Install all hooks from `.githooks/`
- `/hooks list` — List installed hooks
- `/hooks test` — Test all hooks
- `/hooks create <type>` — Create a new hook
- `git hooks` — Interactive mode
- `install hooks` — Same as /hooks install
- `debug hooks` — Debug failing hooks

---

## Workflow

### Install Hooks

```powershell
# Point git to hooks directory
git config core.hooksPath .githooks

# Verify
git config --get core.hooksPath

# Ensure hooks are executable (Linux/macOS)
# chmod +x .githooks/*
```

### List Installed Hooks

```powershell
Get-ChildItem -Path .githooks -File | Select-Object Name, Length, LastWriteTime
```

### Test Hooks

```powershell
# Test pre-commit
.git/hooks/pre-commit

# Test pre-push
.git/hooks/pre-push

# Test commit-msg
echo "test message" | .git/hooks/commit-msg
```

### Create New Hook

```powershell
# Create hook file
New-Item -ItemType File -Path ".githooks/<hook-name>" -Force

# Add shebang and logic
Set-Content -Path ".githooks/<hook-name>" -Value "#!/usr/bin/env bash`n# Hook logic here`n"

# Make executable (Linux/macOS)
# chmod +x .githooks/<hook-name>
```

---

## Hook Templates

### pre-commit (Conventional Commits + Lint)

```bash
#!/usr/bin/env bash
# Pre-commit hook: validate commit message format and run linters

# Check for secrets
if git diff --cached --name-only | xargs grep -l "password\|secret\|token" 2>/dev/null; then
    echo "WARNING: Possible secrets in staged files"
fi

# Run Python linting on staged files
STAGED_PY=$(git diff --cached --name-only --diff-filter=ACM | grep '\.py$')
if [ -n "$STAGED_PY" ]; then
    echo "Running Python linting..."
    echo "$STAGED_PY" | xargs python -m py_compile 2>/dev/null
    if [ $? -ne 0 ]; then
        echo "ERROR: Python syntax errors found"
        exit 1
    fi
fi

exit 0
```

### commit-msg (Conventional Commits)

```bash
#!/usr/bin/env bash
# Commit-msg hook: enforce conventional commits

MSG=$(cat "$1")
PATTERN="^(feat|fix|docs|style|refactor|test|chore|ci|build|perf|revert)(\(.+\))?: .{1,72}"

if ! echo "$MSG" | grep -qE "$PATTERN"; then
    echo "ERROR: Commit message does not follow Conventional Commits"
    echo "Format: <type>(<scope>): <description>"
    echo "Types: feat, fix, docs, style, refactor, test, chore, ci, build, perf, revert"
    exit 1
fi

exit 0
```

### pre-push (Tests + Branch Protection)

```bash
#!/usr/bin/env bash
# Pre-push hook: run tests and validate branch

BRANCH=$(git rev-parse --abbrev-ref HEAD)

# Block direct push to main
if [ "$BRANCH" = "main" ]; then
    echo "ERROR: Direct push to main is not allowed. Use a PR."
    exit 1
fi

# Run tests if pytest available
if command -v pytest &>/dev/null; then
    pytest --co -q 2>/dev/null
    if [ $? -ne 0 ]; then
        echo "ERROR: Tests failed. Fix before pushing."
        exit 1
    fi
fi

exit 0
```

---

## Debugging Hooks

```powershell
# Check hook is executable
Get-Item .githooks/pre-commit | Select-Object Mode

# Run hook manually with debug
bash -x .githooks/pre-commit

# Check git hooks path
git config --get core.hooksPath

# Temporarily skip hooks
git commit --no-verify
git push --no-verify
```

---

## Examples

### Example 1: Install All Hooks

```powershell
/hooks install
# → git config core.hooksPath .githooks
```

### Example 2: Create Pre-commit Hook

```powershell
/hooks create pre-commit
# → Creates .githooks/pre-commit with template
```

### Example 3: Test Hooks

```powershell
/hooks test
# → Runs each hook and reports pass/fail
```

---

## Dependencies

- **Depends on**: None
- **Provides to**: `conventional-commit-validator`

---

## Changelog

| Version | Date | Change | IntentHash |
|---------|------|--------|------------|
| 1.0.0 | 2026-06-06 | Initial version | `0xGIT_HOOKS_MANAGER_SKILL_20260606` |
