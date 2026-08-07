---
type: skill
version: "1.0.0"
date: "2026-08-01"
intent_hash: 0xCFMI_DASHBOARD_20260801
status: active
---

# Skill: cfmi-dashboard-generator

## Purpose
Generate HTML dashboard with Chart.js visualization of CFMI I-Scores across pipelines. Consumes cfmi-scanner output.

## Context
Dashboard provides at-a-glance maturity view for governance. Updates on each scan.

## Input
- .kilo/cfmi-scan.yaml (from cfmi-scanner)
- .kilo/wal/cfmi.wal (historical data)

## Output
- .kilo/dashboard/cfmi-dashboard.html u2014 standalone HTML with embedded Chart.js

## Dashboard Sections

### 1. Pipeline Overview (Radar Chart)
- Axes: ALFRED, BRGS, KIVA
- Value: Current I-Score
- Target: 90 (GREEN threshold)

### 2. Gate Status Matrix (Heatmap)
- Rows: Gates (12 total)
- Columns: Last 10 runs
- Color: GREEN/YELLOW/RED

### 3. I-Score Trend (Line Chart)
- X-axis: Time (last 30 days)
- Y-axis: I-Score (0-100)
- Lines: ALFRED, BRGS, KIVA, Overall

### 4. WAL Timeline (Table)
- Last 50 entries from cfmi.wal
- Filterable by pipeline, status

## Generation Command
`powershell
python -m tools.cfmi_dashboard --input .kilo/cfmi-scan.yaml --wal .kilo/wal/cfmi.wal --output .kilo/dashboard/cfmi-dashboard.html
`

## Template Structure
`html
<!DOCTYPE html>
<html>
<head>
  <title>CFMI Dashboard</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>/* embedded CSS */</style>
</head>
<body>
  <canvas id="radar"></canvas>
  <canvas id="heatmap"></canvas>
  <canvas id="trend"></canvas>
  <table id="wal-timeline"></table>
  <script>/* Chart.js init + data injection */</script>
</body>
</html>
`

## Auto-refresh
- Dashboard regenerates on each cfmi-scanner run
- Optional: --watch mode for live updates

## References
- S-003: cfmi-scanner (skill)
- D-004: cfmi-governance (design)
- ATOM-052: CFMI Pipeline
