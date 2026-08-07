---
type: skill
version: "1.0.0"
date: "2026-08-01"
intent_hash: 0xATOMIC_PLANNER_20260801
status: active
---

# Skill: atomic-task-planner

## Purpose
Transform free-form task descriptions into structured atomic execution plans (JSON) for SLM micro-executor. 4 templates covering all task types.

## Context
SLM execution requires atomic steps (1 tool call, <=150 tokens). This skill decomposes complex requests into executable plans.

## Input
- Natural language task description
- Context: available tools, current repo state

## Output
- .kilo/plan/execution_plan.json - structured plan

## 4 Plan Templates

### Template A - Inspection (Pattern A)
`json
{
  "template": "inspection",
  "steps": [
    {"tool": "read", "target": "path/to/file", "verify": "content_contains:pattern"},
    {"tool": "grep", "pattern": "regex", "path": "dir", "verify": "count>0"}
  ],
  "estimated_tokens": 80
}
`

### Template B - Creation (Pattern C)
`json
{
  "template": "creation",
  "steps": [
    {"tool": "write", "target": "path/to/new_file", "content": "template_based", "verify": "Test-Path"}
  ],
  "estimated_tokens": 120
}
`

### Template C - Modification (Pattern D)
`json
{
  "template": "modification",
  "steps": [
    {"tool": "read", "target": "path/to/file"},
    {"tool": "edit", "target": "path/to/file", "old": "exact_string", "new": "replacement", "verify": "diff_check"}
  ],
  "estimated_tokens": 100
}
`

### Template D - Multi-repo Deployment (Pattern E)
`json
{
  "template": "deployment",
  "steps": [
    {"tool": "write", "target": "C:\\DevTools\\source_file", "verify": "Test-Path"},
    {"tool": "bash", "command": "Copy-Item source dest1", "verify": "Test-Path dest1"},
    {"tool": "bash", "command": "Copy-Item source dest2", "verify": "Test-Path dest2"}
  ],
  "estimated_tokens": 150
}
`

## Planning Algorithm
1. Classify task -> select template
2. Extract parameters (paths, patterns, content)
3. Generate step sequence
4. Estimate tokens per step
5. If total > 150: split into sub-plans
6. Output JSON with metadata

## Command
`powershell
python -m tools.atomic_planner "Create skill for X in skills/Y" --output .kilo/plan/execution_plan.json
`

## Anti-patterns
- Generating steps > 150 tokens (must split)
- Missing verification step
- Not specifying exact paths
- Combining multiple templates in one plan

## References
- S-010: slm-micro-executor (skill, partial exists)
- D-005: execution-protocol (design)
- ATOM-063: execution-protocol
