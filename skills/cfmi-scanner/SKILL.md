---
type: skill
version: "1.0.0"
date: "2026-08-01"
intent_hash: 0xCFMI_SCANNER_20260801
status: active
---

# Skill: cfmi-scanner

## Purpose
Scan CFMI (Cross-Functional Maturity Index) gates across ALFRED, BRGS, KIVA pipelines. Compute I-Score per ATOM-052.

## Context
CFMI governs the 3 main pipelines: ALFRED (archival), BRGS (build/release), KIVA (CI/CD). Each has gates that must pass for deployment.

## Gates to Scan

### ALFRED (Archival)
- gate.archive.ingest: Ingestion pipeline health
- gate.archive.verify: Checksum validation
- gate.archive.index: Search index freshness

### BRGS (Build/Release/Governance/Scan)
- gate.brgs.build: Compilation success
- gate.brgs.test: Test suite pass rate
- gate.brgs.governance: Policy compliance
- gate.brgs.scan: Security scan clean

### KIVA (CI/CD)
- gate.kiva.lint: Linting pass
- gate.kiva.unit: Unit tests pass
- gate.kiva.integration: Integration tests pass
- gate.kiva.deploy: Deployment readiness

## I-Score Calculation
`
I-Score = (passed_gates / total_gates) * 100
Thresholds:
  - GREEN:  u2265 90
  - YELLOW: 70-89
  - RED:    < 70
`

## WAL Integration
- Each gate result appended to WAL (Write-Ahead Log)
- Format: [CFMI] gate=<name> status=<PASS|FAIL> score=<I-Score> timestamp=<ISO8601>
- WAL path: .kilo/wal/cfmi.wal

## Scan Command
`powershell
python -m tools.cfmi_scanner --pipelines ALFRED,BRGS,KIVA --output .kilo/cfmi-scan.yaml
`

## Output Format
`yaml
pipeline: BRGS
gates:
  - name: gate.brgs.build
    status: PASS
    latency_ms: 1240
  - name: gate.brgs.test
    status: PASS
    latency_ms: 3420
  - name: gate.brgs.governance
    status: FAIL
    reason: "policy: ADR-066 not linked"
i_score: 75
status: YELLOW
`

## Auto-fix Trigger
If I-Score < 70 (RED), trigger cfmi-auto-fix skill (separate).

## References
- D-004: cfmi-governance (design)
- ATOM-052: CFMI Pipeline
- ATOM-053: TDD AIRAIN Law
