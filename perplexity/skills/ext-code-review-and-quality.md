---
name: ext-code-review-and-quality
version: "1.0.0"
description: "Multi-dimensional code review with quality gates (source: addyosmani/agent-skills). Every change gets reviewed before merge. Covers five axes: correctness, readability, architecture, security, and performance."
triggers: ["code review", "quality gate", "PR review", "code quality", "five-axis review"]
layer: "L2_COMPOSITION"
nexusTags: ["EXT_ADDYOSMANI"]
prerequisites: []
slotWeight: 1
status: active
upstream: https://github.com/addyosmani/agent-skills/blob/main/skills/code-review-and-quality/SKILL.md
trit_primitive: TritScanRegistry
---
# ext-code-review-and-quality

> Source: [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | Adapted for gerivdb/SKILLS

Multi-dimensional code review with quality gates. Every change gets reviewed before merge - no exceptions. Review covers five axes: correctness, readability, architecture, security, and performance.

**The approval standard:** Approve a change when it definitely improves overall code health, even if it isn't perfect. Perfect code doesn't exist - the goal is continuous improvement.

## The Five-Axis Review

### 1. Correctness
- Does it match the spec or task requirements?
- Are edge cases handled (null, empty, boundary values)?
- Are error paths handled (not just the happy path)?
- Does it pass all tests? Are the tests actually testing the right things?
- Are there off-by-one errors, race conditions, or state inconsistencies?

### 2. Readability and Simplicity
- Are names descriptive and consistent with project conventions? (No `temp`, `data`, `result` without context)
- Is the control flow straightforward (avoid nested ternaries, deep callbacks)?
- Is the code organized logically (related code grouped, clear module boundaries)?
- **Could this be done in fewer lines?** (1000 lines where 100 suffice is a failure)
- **Are abstractions earning their complexity?** (Don't generalize until the third use case)

### 3. Architecture
- Does it follow existing patterns or introduce a new one? If new, is it justified?
- Does it maintain clean module boundaries?
- Is there code duplication that should be shared?
- Are dependencies flowing in the right direction (no circular dependencies)?
- Is the abstraction level appropriate (not over-engineered, not too coupled)?

### 4. Security
- Is user input validated and sanitized?
- Are secrets kept out of code, logs, and version control?
- Is authentication/authorization checked where needed?
- Are SQL queries parameterized (no string concatenation)?
- Are outputs encoded to prevent XSS?
- Are dependencies from trusted sources with no known vulnerabilities?

### 5. Performance
- Any N+1 query patterns?
- Any unbounded loops or unconstrained data fetching?
- Any synchronous operations that should be async?
- Any unnecessary re-renders in UI components?
- Any missing pagination on list endpoints?

## Change Sizing

```
~100 lines changed   -> Good. Reviewable in one sitting.
~300 lines changed   -> Acceptable if it's a single logical change.
~1000 lines changed  -> Too large. Split it.
```

**Splitting strategies:** Stack (sequential dependencies), By file group (cross-cutting concerns), Horizontal (shared code first), Vertical (feature slices).

## Review Process

1. **Understand the Context** - What is this change trying to accomplish?
2. **Review the Tests First** - Tests reveal intent and coverage
3. **Review the Implementation** - Walk through the code with the five axes
4. **Categorize Findings** - Critical / Important / Suggestion / Nit / FYI
5. **Verify the Verification** - Tests pass? Build succeeds? Manual verification?

## Severity Labels

| Prefix | Meaning | Author Action |
|--------|---------|---------------|
| *(no prefix)* | Required change | Must address before merge |
| **Critical:** | Blocks merge | Security vulnerability, data loss, broken functionality |
| **Nit:** | Minor, optional | Author may ignore - formatting, style preferences |
| **Optional:** / **Consider:** | Suggestion | Worth considering but not required |
| **FYI** | Informational only | No action needed |

## Multi-Model Review Pattern

```
Model A writes the code
    |
    v
Model B reviews for correctness and architecture
    |
    v
Model A addresses the feedback
    |
    v
Human makes the final call
```

## Handling Disagreements

1. **Technical facts and data** override opinions and preferences
2. **Style guides** are the absolute authority on style matters
3. **Software design** must be evaluated on engineering principles, not personal preference
4. **Codebase consistency** is acceptable if it doesn't degrade overall health

**Don't accept "I'll clean it up later."** Require cleanup before submission unless it's a genuine emergency.

## Integration with gerivdb

- Use `ext-code-reviewer` agent for the review execution
- Complements: SCO7 (strategic), Selina (analytical), Riddler (architectural)
- Gate: No merge without review on L2+ repos
