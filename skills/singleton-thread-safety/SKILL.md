---
name: singleton-thread-safety
description: >-
  Detect and fix singleton patterns that lack thread-safety. Identifies race
  conditions in __new__(), missing locks, and non-thread-safe state mutations.
  Provides thread-safe implementations using locks or alternative patterns.
license: MIT
metadata:
  category: architecture
  author: ecos
  targets: [python, threading]
---

# Singleton Thread-Safety Auditor

Detect race conditions in singleton implementations and provide thread-safe alternatives.

---

## Triggers

Use this skill when:
- "audit singletons"
- "fix race condition"
- "thread-safe singleton"
- "check __new__ implementation"
- "singleton pattern review"

---

## Quick Reference

| Issue | Risk | Fix |
|-------|------|-----|
| No lock in `__new__` | Race condition | Add threading.Lock |
| Non-atomic check | Double creation | Use lock in __new__ |
| Mutable class state | Data corruption | Thread-safe dict/list |
| Global shared state | Concurrent access | Add locks around mutations |

---

## Process

### Phase 1: Find Singleton Patterns

Search for:
- Classes with `__new__` method overriding
- Classes with `_instance` class variable
- Module-level global instances

```python
# Pattern 1: Classic Singleton
class Watchdog:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

# Pattern 2: Global instance
_config_loader = ConfigLoader()

# Pattern 3: Class variable singleton
class HealthMonitor:
    _instance: Optional["HealthMonitor"] = None
```

### Phase 2: Identify Thread-Safety Issues

Check each singleton for:
- ❌ No `threading.Lock` in `__new__`
- ❌ `if _instance is None` not protected
- ❌ Mutable state without lock protection
- ❌ Lazy initialization not atomic

### Phase 3: Provide Fixes

**Before (racy):**
```python
class Watchdog:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:  # Race condition!
            cls._instance = super().__new__(cls)
        return cls._instance
```

**After (thread-safe):**
```python
import threading

class Watchdog:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:  # Double-check
                    cls._instance = super().__new__(cls)
        return cls._instance
```

---

## Common Issues

### Issue 1: Race in `__new__`
```python
# Thread A checks _instance: None
# Thread B checks _instance: None
# Thread A creates instance
# Thread B creates instance -> TWO INSTANCES!
```

### Issue 2: Mutable class state
```python
class HealthMonitor:
    _instance = None
    
    def __init__(self):
        self._backends = {}  # Not thread-safe!
    
    def register(self, backend_id, backend):
        # Multiple threads could write simultaneously
        self._backends[backend_id] = backend
```

### Issue 3: Global without protection
```python
# config.py
_configs = {}  # Global dict, not thread-safe

def get_config(backend_id):
    if backend_id not in _configs:  # Race!
        _configs[backend_id] = load(backend_id)
    return _configs[backend_id]
```

---

## Fix Templates

### Template 1: Thread-Safe Singleton
```python
import threading
from typing import Optional, Any

class ThreadSafeSingleton:
    _instance: Optional[Any] = None
    _lock: threading.Lock = threading.Lock()
    _init_lock: threading.Lock = threading.Lock()
    _initialized: bool = False
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self.__class__._initialized:
            with self.__class__._init_lock:
                if not self.__class__._initialized:
                    self._setup()
                    self.__class__._initialized = True
```

### Template 2: Thread-Safe Shared State
```python
import threading
from typing import Dict, Any

class ThreadSafeDict:
    def __init__(self):
        self._data: Dict[str, Any] = {}
        self._lock = threading.RLock()
    
    def __setitem__(self, key: str, value: Any):
        with self._lock:
            self._data[key] = value
    
    def __getitem__(self, key: str) -> Any:
        with self._lock:
            return self._data[key]
    
    def get(self, key: str, default=None):
        with self._lock:
            return self._data.get(key, default)
```

---

## Audit Report Format

```markdown
## Singleton Thread-Safety Audit

### CRITICAL: Race Condition in __new__
- watchdog.py: Watchdog - no lock in __new__
- provider_health.py: HealthMonitor - no lock in __new__

### WARNING: Non-Thread-Safe Mutable State
- config.py: _configs dict - no lock protection
- rate_limiter.py: global_rate_limiter - shared state without lock

### PASSED
- llm_autodiscover.py: LLMAutodiscover - thread-safe implementation
```

---

## References

- Python `threading.Lock` vs `threading.RLock`
- Double-checked locking pattern
- `atexit.register()` for cleanup
- Context manager for lock acquisition