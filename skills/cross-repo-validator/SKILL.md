---
type: skill
version: "1.0.0"
date: "2026-08-01"
intent_hash: 0xPLIX_CROSSREPO_20260801
status: active
extends: repo-ref-validator
---

# Skill: cross-repo-validator

## Purpose
Validate cross-repository references across all 47 active repos in the gerivdb metacluster. Extends repo-ref-validator for multi-repo scope.

## Context
The ecosystem has 47 repos across L1-L4 strata. Cross-repo references (BRIDGES, imports, deployments) must be validated holistically.

## Scope Extension
Base skill (repo-ref-validator) validates single-file references. This skill adds:
- Cross-repo BRIDGES.yaml validation
- Deployment target verification (ECOS_ROOT.json)
- Stratum compliance (L0-L4 paths)
- Registry consistency (repos.json ↔ known_repositories.yaml)

## Validation Targets

### 1. BRIDGES.yaml
- Every rom_repo → 	o_repo pair must exist in both registries
- interface field must match actual API/contract
- status: active/deprecated must match git tags

### 2. Deployment Targets
- plix deploy targets in EPICs must match ECOS_ROOT.json entries
- Stratum prefix validation: L0-CANON/, L1-INFRA/, L2-PLATFORM/, L3-CITIZENS/, L4-TOOLS/
- No orphan deployments (target not in registry)

### 3. Import/Dependency Graph
- Python/JS imports across repos resolved via epo-path-resolver
- Version compatibility: pyproject.toml / package.json cross-check
- Circular dependency detection

### 4. Registry Consistency
- epos.json (TOPOS) ↔ known_repositories.yaml (GOVERNANCE-HUB) sync
- local_path must exist and be under correct stratum
- status field: active/dormant/deprecated/archived consistency

## Validation Command
`powershell
python -m tools.cross_repo_validator --registry repos.json --sot known_repositories.yaml --output .kilo/cross-repo-report.yaml
`

## Output Format
`yaml
repos_checked: 47
bridges_validated: 23
deployments_verified: 47
imports_resolved: 156
circular_deps: 0
stratum_violations: 0
registry_mismatches: 0
status: PASS
`

## Anti-patterns
- Validating single repo without cross-repo context
- Ignoring BRIDGES.yaml in multi-repo changes
- Deployment to non-registered targets
- Registry drift (repos.json ≠ known_repositories.yaml)

## References
- Base: repo-ref-validator (skill)
- S-009: git-checkpoint (skill)
- D-006: git-engineering (design)
- ATOM-066: git-engineering
