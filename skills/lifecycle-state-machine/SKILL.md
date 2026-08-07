---
name: lifecycle-state-machine
description: >-
  Validate async component lifecycle patterns - verify proper initialization,
  error handling, shutdown timeouts, and state transitions. Detects missing
  try/except in initialize(), missing timeout in close(), and invalid state access.
license: MIT
metadata:
  category: architecture
  author: ecos
  targets: [python, async]
---

# Lifecycle State Machine Validator

Validate async components respect proper lifecycle patterns with state transitions,
error handling, and cleanup guarantees.

---

## Triggers

Use this skill when:
- "validate lifecycle patterns"
- "check async initialization"
- "audit shutdown handling"
- "detect missing try/except"
- "verify state machine transitions"

---

## Quick Reference

| Pattern | Required | Check |
|---------|----------|-------|
| `async def initialize()` | try/except | [OK] Logging + state on error |
| `async def close()` | timeout | [OK] Max 30s, graceful cleanup |
| State transitions | valid only | [OK] UNINIT -> INIT -> READY -> SHUTDOWN |
| Double-init | prevented | [OK] Idempotent initialization |

---

## Process

### Phase 1: Find Async Components

Search for classes with async lifecycle methods:

```python
# Pattern 1: __init__ + initialize() + close()
class GatewayServer:
    def __init__(self):
        self._state = "UNINITIALIZED"
    
    async def initialize(self):
        self._state = "INITIALIZING"
        # MUST have try/except here
        try:
            await self.router.initialize()
            self._state = "READY"
        except Exception as e:
            self._state = "FAILED"
            logger.error(f"Init failed: {e}")
            raise

    async def close(self):
        # MUST have timeout
        await asyncio.wait_for(self.router.close(), timeout=30.0)
        self._state = "SHUTDOWN"
```

### Phase 2: Validate Error Handling

Check each `initialize()` method for:
- [OK] try/except block present
- [OK] Error logged with context
- [OK] State set to FAILED on error
- [OK] Exception re-raised or handled

### Phase 3: Validate Shutdown

Check each `close()` method for:
- [OK] asyncio.wait_with_timeout() used
- [OK] Timeout <= 30 seconds
- [OK] Cleanup happens in finally block
- [OK] Partial cleanup handled

### Phase 4: Detect Issues

Report findings:

```markdown
## Lifecycle Audit Results

### CRITICAL: Missing Error Handling
- server.py: GatewayServer.initialize() - no try/except
- watchdog.py: Watchdog.initialize() - no try/except
- provider_health.py: HealthMonitor.initialize() - no try/except

### WARNING: Missing Shutdown Timeout
- router.py: MCPRouter.close() - no timeout
- llm_autodiscover.py: LLMAutodiscover.close() - no timeout

### INFO: State Not Tracked
- backend_discovery.py: BackendDiscovery - no _state field
```

---

## Implementation Checklist

For each async component:

- [ ] Add `_state` class variable with initial value
- [ ] Wrap `initialize()` body in try/except
- [ ] Set `_state = "FAILED"` in except block
- [ ] Log error with logger.exception()
- [ ] Use `asyncio.wait_for(close(), timeout=30)` 
- [ ] Add finally block for cleanup
- [ ] Track state transitions in docstring

---

## Example Fix

**Before (problematic):**
```python
async def initialize(self):
    await self.router.initialize()
    await self.discovery.load()
```

**After (correct):**
```python
async def initialize(self):
    self._state = "INITIALIZING"
    try:
        await self.router.initialize()
        await self.discovery.load()
        self._state = "READY"
        logger.info("Component initialized successfully")
    except Exception as e:
        self._state = "FAILED"
        logger.exception(f"Initialization failed: {e}")
        raise
```

---

## Detection Patterns

### Regex for initialize():
```regex
async def initialize\(self\):\s*\n\s*(?!try)
```

### Regex for close():
```regex
async def close\(self\):\s*\n(?!.*wait_for.*timeout)
```

### State enum:
```python
class ComponentState:
    UNINITIALIZED = "uninitialized"
    INITIALIZING = "initializing"
    READY = "ready"
    FAILED = "failed"
    SHUTDOWN = "shutdown"
```