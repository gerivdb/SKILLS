---
type: skill
version: "1.0.0"
date: "2026-06-08"
intent_hash: 0xGAP_REPORT_LIFECYCLE_20260608
status: active
trit_primitive: TritObserve
tags: [sgr, gap, lifecycle, resolution, closure]
---

# gap-report-lifecycle

## Purpose
Manage the full lifecycle of SGR gap reports — from detection through resolution, exceptions, and phase closure.

## Trigger
Use when: managing SGR gaps, user mentions "gap lifecycle", "resolve gaps", "gap closure", "gap exceptions", or "session summary".

## Gap lifecycle

```
DETECTED → TRIAGED → RESOLVED/EXCEPTED → VERIFIED → CLOSED
   ↓           ↓            ↓                  ↓          ↓
 SGR run    Priority    Scanner created    Re-run SGR   Report
 produces   assigned    or exception       gap gone     archived
 GAP_REPORT documented                    from report
```

## Phase protocols

### Phase 1 — Detection (SGR run)

After SGR produces GAP_REPORT:
1. Parse report: count gaps per priority (P1/P2/P3)
2. Identify gap patterns (REPO_UNCOVERED, SKILL_ORPHAN, TRIT_ORPHAN, CITIZEN_UNBACKED)
3. Check exceptions list in `config/sgr.yaml`
4. Produce triage summary

### Phase 2 — Triage

For each gap, determine:

| Gap type | Severity | Action |
|----------|----------|--------|
| `REPO_UNCOVERED_*` (P1) | Critical | Create scanner ARGUS immediately |
| `REPO_UNCOVERED_*` (P2) | High | Create scanner or document exception |
| `SKILL_ORPHAN_*` (P3) | Medium | Batch patch trit_primitive |
| `TRIT_ORPHAN_*` (P3) | Medium | Link to workflow/citizen |
| `CITIZEN_UNBACKED_*` (P2) | High | Create ADR backing |

### Phase 3 — Resolution

**Option A — Create scanner** (for REPO_UNCOVERED gaps):
1. Use `scaffold-scanner` to generate YAML
2. Test: `declarative_runner {scanner}.yaml` → score 1.0
3. Register in `argus.yaml`

**Option B — Batch patch** (for SKILL_ORPHAN gaps):
1. Use `patch_skill_frontmatter.py --skills-dir {dir} --force`
2. Verify: `skill_trit_coverage` scanner score 1.0

**Option C — Document exception** (for gaps that won't be fixed):
1. Add entry to `config/sgr.yaml` exceptions list
2. Document reason, review date

### Phase 4 — Verification

1. Re-run SGR: `python run_sgr.py`
2. Compare new GAP_REPORT with previous
3. Expected: all targeted gaps gone or in exceptions list
4. If gaps persist → return to Phase 2

### Phase 5 — Closure

1. Archive report: `NEXUS/reports/sgr/GAP_REPORT-{date}.json`
2. Update GAP_REPORT summary (total_gaps, by_priority, resolved_count)
3. Session complete

## Exception format

```yaml
- gap_id: "REPO_UNCOVERED_NEXUS"
  reason: "NEXUS est le SOT data — couverture ARGUS déléguée"
  approved_by: "HITL-2026-06-08"
  review_date: "2026-09-08"
```

Required fields: `gap_id`, `reason`, `approved_by`, `review_date`.

## Rules
- Always verify by re-running SGR after resolutions
- Always include review_date in exceptions
- Always register scanners in argus.yaml AND test them
- Always archive the final GAP_REPORT for audit

## Anti-patterns
- Don't resolve gaps without verifying (re-run SGR required)
- Don't document exceptions without review date
- Don't leave orphaned scanners (register AND test)
- Don't skip the archive step — GAP_REPORT must be preserved
