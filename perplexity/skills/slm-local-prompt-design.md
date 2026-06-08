---
type: skill
version: "1.0.0"
date: "2026-06-08"
intent_hash: 0xSLM_LOCAL_PROMPT_DESIGN_20260608
status: active
trit_primitive: TritOptimize
tags: [slm, prompt, design, z600, owl-alpha]
---

# slm-local-prompt-design

## Purpose
Design effective prompts for local SLM (Small Language Model) inference on CPU-only hardware — maximize determinism, minimize hallucination.

## Trigger
Use when: writing prompts for local SLM, user mentions "prompt design", "SLM", "Owl Alpha", "local inference", or "CPU-only".

## Context

Owl Alpha on Z600 (2× Xeon E5620, 24 GB DDR3, no GPU) has specific constraints:
- Context window: ~4000 tokens (practical limit: ~2000 for reliability)
- Inference speed: ~200 tokens/sec on CPU
- No parallel GPU offloading

Prompts designed for cloud LLMs (long, conversational, multi-step) fail on local SLMs.

## Prompt anatomy for SLM (Z600)

```
[CONTEXT: 1-2 sentences max]
[TASK: 1 sentence, imperative mood]
[INPUT: bullet list, max 5 items]
[OUTPUT: exact format expected]
[VERIFY: how to check success]
```

Total: < 200 tokens.

## Rules

### 1. One task per prompt

```
❌ "Analyze the codebase, identify gaps, create scanners, test them, and report"
✅ "Create scanners/gaps/REPO_COVERAGE_GENERIC.yaml. Input: repo_list.yaml. Output: YAML file. Verify: score=1.0"
```

### 2. Specify exact paths

```
❌ "Find the right config file"
✅ "Read D:\DO\WEB\TOOLS\L0-CANON\GOVERNANCE-HUB\config\argus.yaml"
```

### 3. Include verification

```
✅ "After writing, run: python -m engine.declarative_runner {path} — expect score=1.0"
```

### 4. No nested conditionals

```
❌ "If X then Y, unless Z in which case W"
✅ "Step 1: Check X. Step 2: If X, do Y. Step 3: Verify."
```

### 5. Batch operations > sequential

```
❌ Loop 16 times: "Process repo1... repo2... repo3..."
✅ "Process all repos in D:\DO\WEB\TOOLS\L3-CITIZENS. For each: create STRATUM_RELAY.md. Report: count OK/FAIL."
```

### 6. Deterministic > creative

```
❌ "Suggest a good name for this scanner"
✅ "Scanner ID format: {repo_name}_health. Example: KIVA-CLI → kivacli_health."
```

## Pattern library

### Pattern A — File creation

```
Task: Create {file_path}
Source: {metadata_source}
Content: YAML with keys [{key1}, {key2}]
Verify: Test-Path {file_path}
```

### Pattern B — Batch patch

```
Task: Patch all .md files in {dir}
Change: Add {field}: {value} to frontmatter
Condition: Only if {field} not already present
Verify: grep count
```

### Pattern C — Gap resolution

```
Task: Close gap {gap_id} from {report_path}
Source: GAP_REPORT section {priority}, gap {gap_id}
Action: {specific_remediation}
Verify: Re-run SGR, gap {gap_id} should not appear
```

## Performance benchmarks (Z600)

| Prompt type | Token count | Expected success rate |
|-------------|-------------|----------------------|
| File creation (deterministic) | 50-100 | > 95% |
| Batch patch (pattern-based) | 100-150 | > 90% |
| Multi-step analysis | 150-200 | ~ 70% |
| Creative/inferential | 200+ | < 50% |

## Anti-patterns
- Don't write prompts > 200 tokens
- Don't use conversational tone ("Please", "Could you", "I'd like")
- Don't ask for opinions or suggestions — give deterministic tasks
- Don't nest more than 2 levels of instructions
- Don't assume the SLM knows project conventions — specify them explicitly
