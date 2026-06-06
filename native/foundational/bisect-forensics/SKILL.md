---
name: bisect-forensics
description: "Guides git bisect for regression hunting, automated bisect scripts, and git blame for forensic analysis"
triggers:
  - /bisect
  - git bisect
  - find regression
  - bisect start
  - git blame
  - who changed this
  - when was this introduced
  - forensic analysis
domain: foundational
version: "1.0.0"
author: gerivdb
license: MIT
status: active
created: 2026-06-06
updated: 2026-06-06
tags:
  - git
  - bisect
  - blame
  - forensics
  - debugging
phi_weight: 0.005
---

# Bisect Forensics Skill

> **IntentHash**: `0xBISECT_FORENSICS_SKILL_20260606`
> **Version**: 1.0.0
> **Domain**: foundational
> **Type**: foundational
> **Status**: active

---

## Synopsis

Guides `git bisect` for regression hunting and `git blame` for forensic analysis. Supports both manual and automated bisect workflows.

---

## Triggers

- `/bisect start <bad> <good>` — Start bisect session
- `/bisect run <script>` — Automated bisect with test script
- `/blame <file> [line]` — Show who changed each line
- `find regression` — Same as /bisect start
- `who changed this` — Same as /blame
- `when was this introduced` — Find commit that introduced a change

---

## Workflow

### Git Bisect (Manual)

```powershell
# 1. Start bisect
git bisect start
git bisect bad HEAD          # Current commit is broken
git bisect good v1.2.0       # Last known good commit

# 2. Git checks out a middle commit
# Test it:
pytest tests/ 2>$null

# 3. Mark result
git bisect good   # if tests pass
git bisect bad    # if tests fail

# 4. Repeat until git finds the first bad commit
# Git will output: "abc1234 is the first bad commit"

# 5. End bisect
git bisect reset
```

### Git Bisect (Automated)

```powershell
# Run bisect with automatic test script
git bisect start HEAD v1.2.0
git bisect run pytest tests/test_specific.py

# Or with custom script
git bisect run bash -c "python -m pytest tests/ -x -q"

# Bisect will automatically find the first bad commit
```

### Git Blame

```powershell
# Show who changed each line
git blame <file>

# Show specific lines
git blame -L 10,20 <file>

# Show commit that introduced a specific text
git log -S "search_string" --source --all --oneline

# Show commit that introduced a regex
git log -G "regex_pattern" --source --all --oneline

# Show blame ignoring whitespace
git blame -w <file>

# Show blame ignoring moves/copies
git blame -M -C <file>
```

### Find When a Bug Was Introduced

```powershell
# Method 1: git log -S (pickaxe)
git log -S "buggy_function_name" --oneline

# Method 2: git log -G (regex)
git log -G "pattern" --oneline

# Method 3: git bisect (most reliable)
git bisect start HEAD <known-good>
git bisect run <test-script>
```

---

## Examples

### Example 1: Find Regression

```powershell
/bisect start HEAD v1.2.0
# → Starts manual bisect
```

### Example 2: Automated Bisect

```powershell
/bisect run "pytest tests/ -x"
# → Automated bisect with pytest
```

### Example 3: Blame File

```powershell
/blame src/brain/mc_rnn/mc_rnn_layer.py 42
# → Shows who changed line 42
```

### Example 4: Find When Text Was Added

```powershell
/when "McRnnLayer" was introduced
# → git log -S "McRnnLayer" --oneline
```

---

## Dependencies

- **Depends on**: None
- **Provides to**: None

---

## Changelog

| Version | Date | Change | IntentHash |
|---------|------|--------|------------|
| 1.0.0 | 2026-06-06 | Initial version | `0xBISECT_FORENSICS_SKILL_20260606` |
