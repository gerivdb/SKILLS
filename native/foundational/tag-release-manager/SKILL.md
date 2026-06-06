---
name: tag-release-manager
description: "Semantic versioning, git tag creation, release branch management, release automation, and changelog integration"
triggers:
  - /release
  - create release
  - tag release
  - semantic version
  - bump version
  - create tag
  - release notes
  - publish release
domain: foundational
version: "1.0.0"
author: gerivdb
license: MIT
status: active
created: 2026-06-06
updated: 2026-06-06
tags:
  - git
  - tag
  - release
  - semver
  - versioning
phi_weight: 0.007
---

# Tag Release Manager Skill

> **IntentHash**: `0xTAG_RELEASE_MANAGER_SKILL_20260606`
> **Version**: 1.0.0
> **Domain**: foundational
> **Type**: foundational
> **Status**: active

---

## Synopsis

Manages semantic versioning, git tags, release branches, and release automation. Integrates with `changelog-generator` for release notes.

---

## Triggers

- `/release create <version>` — Create a new release
- `/release bump <major|minor|patch>` — Bump version
- `/tag create <version>` — Create git tag
- `semantic version` — Version guidance
- `create release` — Same as /release create
- `release notes` — Generate release notes

---

## Semantic Versioning (SemVer)

Format: `v<major>.<minor>.<patch>[-prerelease]`

| Bump Type | When | Example |
|-----------|------|---------|
| `major` | Breaking changes | `v1.2.3` → `v2.0.0` |
| `minor` | New features (backward compatible) | `v1.2.3` → `v1.3.0` |
| `patch` | Bug fixes | `v1.2.3` → `v1.2.4` |
| `prerelease` | Pre-release | `v1.3.0-alpha.1` |

---

## Workflow

### Step 1: Determine Version Bump

Analyze commits since last tag:

```powershell
# Get last tag
git describe --tags --abbrev=0

# Get commits since last tag
git log <last-tag>..HEAD --oneline

# Count by type
git log <last-tag>..HEAD --oneline | Select-String "^feat" | Measure-Object  # → minor
git log <last-tag>..HEAD --oneline | Select-String "^fix" | Measure-Object   # → patch
git log <last-tag>..HEAD --oneline | Select-String "BREAKING" | Measure-Object # → major
```

### Step 2: Create Release Branch (optional)

```powershell
git checkout main
git pull origin main
git checkout -b release/v1.3.0

# Bump version in version files
# Update CHANGELOG.md
git commit -m "chore: bump version to v1.3.0"
```

### Step 3: Create Tag

```powershell
# Lightweight tag
git tag v1.3.0

# Annotated tag (recommended)
git tag -a v1.3.0 -m "Release v1.3.0

Features:
- feat(mc-rnn): MC-RNN layer implementation
- feat(citizens): Jules agents module

Fixes:
- fix(wal): schema alignment"

# Push tag
git push origin v1.3.0

# Push all tags
git push origin --tags
```

### Step 4: Generate Release Notes

```powershell
# Use changelog-generator skill
# Or manually:
git log <previous-tag>..<new-tag> --oneline --no-merges
```

### Step 5: Create GitHub Release (optional)

```powershell
gh release create v1.3.0 \
  --title "Release v1.3.0" \
  --notes-file RELEASE_NOTES.md \
  --target main
```

---

## Tag Conventions

| Pattern | Usage |
|---------|-------|
| `v1.2.3` | Stable release |
| `v1.2.3-alpha.1` | Alpha pre-release |
| `v1.2.3-beta.2` | Beta pre-release |
| `v1.2.3-rc.1` | Release candidate |

---

## Examples

### Example 1: Create Release

```powershell
/release create v1.3.0
# → Analyzes commits, creates tag, generates notes
```

### Example 2: Bump Version

```powershell
/release bump minor
# → Determines new version from last tag, creates tag
```

### Example 3: List Tags

```powershell
/tag list
# → git tag -l --sort=-version:refname
```

---

## Dependencies

- **Depends on**: `changelog-generator`
- **Provides to**: `git-flow-manager`, `kiva-pr-workflow`

---

## Changelog

| Version | Date | Change | IntentHash |
|---------|------|--------|------------|
| 1.0.0 | 2026-06-06 | Initial version | `0xTAG_RELEASE_MANAGER_SKILL_20260606` |
