---
name: ext-test-driven-development
version: "1.0.0"
description: "TDD methodology (source: addyosmani/agent-skills). Write a failing test before writing the code that makes it pass. For bug fixes, reproduce the bug with a test before attempting a fix."
triggers: ["TDD", "test-driven", "write test", "prove-it", "bug reproduction", "test coverage"]
layer: "L2_COMPOSITION"
nexusTags: ["EXT_ADDYOSMANI"]
prerequisites: []
slotWeight: 1
status: active
upstream: https://github.com/addyosmani/agent-skills/blob/main/skills/test-driven-development/SKILL.md
trit_primitive: TritRunTests
---
# ext-test-driven-development

> Source: [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | Adapted for gerivdb/SKILLS

Write a failing test before writing the code that makes it pass. For bug fixes, reproduce the bug with a test before attempting a fix. Tests are proof - "seems right" is not done.

## The TDD Cycle

```
    RED                GREEN              REFACTOR
 Write a test    Write minimal code    Clean up the
 that fails  ->  to make it pass  ->  implementation  ->  (repeat)
```

### Step 1: RED - Write a Failing Test
Write the test first. It must fail. A test that passes immediately proves nothing.

### Step 2: GREEN - Make It Pass
Write the minimum code to make the test pass. Don't over-engineer.

### Step 3: REFACTOR - Clean Up
With tests green, improve the code without changing behavior. Run tests after every refactor step.

## The Prove-It Pattern (Bug Fixes)

```
Bug report arrives
       |
       v
  Write a test that demonstrates the bug
       |
       v
  Test FAILS (confirming the bug exists)
       |
       v
  Implement the fix
       |
       v
  Test PASSES (proving the fix works)
       |
       v
  Run full test suite (no regressions)
```

## The Test Pyramid

```
          /\
         /  \         E2E Tests (~5%)
        /    \        Full user flows, real browser
       /------\
      /        \      Integration Tests (~15%)
     /          \     Component interactions, API boundaries
    /------------\
   /              \   Unit Tests (~80%)
  /                \  Pure logic, isolated, milliseconds each
 /------------------\
```

## Test Sizes

| Size | Constraints | Speed | Example |
|------|------------|-------|---------|
| **Small** | Single process, no I/O, no network | Milliseconds | Pure function tests |
| **Medium** | Multi-process OK, localhost only | Seconds | API tests with test DB |
| **Large** | Multi-machine, external services | Minutes | E2E tests, performance benchmarks |

## Writing Good Tests

### Test State, Not Interactions
Assert on the *outcome* of an operation, not on which methods were called internally.

### DAMP Over DRY in Tests
In tests, **DAMP (Descriptive And Meaningful Phrases)** is better than DRY. Each test should tell a complete story without requiring the reader to trace through shared helpers.

### Prefer Real Implementations Over Mocks
```
Preference order (most to least preferred):
1. Real implementation  -> Highest confidence
2. Fake                 -> In-memory version of a dependency
3. Stub                 -> Returns canned data
4. Mock (interaction)   -> Use sparingly, only at boundaries
```

### Use the Arrange-Act-Assert Pattern
```typescript
it('marks overdue tasks when deadline has passed', () => {
  // Arrange: Set up the test scenario
  const task = createTask({ title: 'Test', deadline: new Date('2025-01-01') });
  // Act: Perform the action being tested
  const result = checkOverdue(task, new Date('2025-01-02'));
  // Assert: Verify the outcome
  expect(result.isOverdue).toBe(true);
});
```

### Name Tests Descriptively
```typescript
// Good: Reads like a specification
describe('TaskService.completeTask', () => {
  it('sets status to completed and records timestamp', ...);
  it('throws NotFoundError for non-existent task', ...);
  it('is idempotent - completing an already-completed task is a no-op', ...);
});

// Bad: Vague names
describe('TaskService', () => {
  it('works', ...);
  it('handles errors', ...);
});
```

## Test Anti-Patterns to Avoid

| Anti-Pattern | Problem | Fix |
|---|---|---|
| Testing implementation details | Tests break when refactoring | Test inputs and outputs, not internal structure |
| Flaky tests (timing, order-dependent) | Erode trust in the test suite | Use deterministic assertions, isolate test state |
| Testing framework code | Wastes time testing third-party behavior | Only test YOUR code |
| Snapshot abuse | Large snapshots nobody reviews | Use snapshots sparingly |
| No test isolation | Tests pass individually but fail together | Each test sets up and tears down its own state |
| Mocking everything | Tests pass but production breaks | Prefer real > fake > stub > mock |

## Integration with gerivdb

- Use `ext-test-engineer` agent for test design and coverage analysis
- Complements: CoPaw (quality assurance), Selina (metrics)
- Gate: No merge without tests for L2+ repos
- ENV2 specific: Tests must be ASCII-safe (GATE-5 encoding policy)
