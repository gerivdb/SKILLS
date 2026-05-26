---
name: dependency-injection
description: >-
  Implement dependency injection container for Python async applications. Enables
  testable code through mock injection, detects circular dependencies, and
  provides lazy loading with centralized configuration.
license: MIT
metadata:
  category: architecture
  author: ecos
  targets: [python, testing]
---

# Dependency Injection Container

Manage dependencies centrally for testability, lazy loading, and circular dependency detection.

---

## Triggers

Use this skill when:
- "implement DI container"
- "fix circular dependency"
- "make code testable"
- "refactor hard-coded dependencies"
- "centralize configuration"

---

## Quick Reference

| Feature | Purpose |
|---------|---------|
| Singleton registration | One instance per app |
| Factory registration | New instance each time |
| Lazy resolution | Resolve on first access |
| Circular detection | Prevent deadlock |

---

## Process

### Phase 1: Identify Hard-Coded Dependencies

Find direct instantiations:
```python
# Problem: Hard-coded, not testable
class GatewayServer:
    def __init__(self):
        self.router = MCPRouter()  # Direct instantiation
        self.discovery = BackendDiscovery()  # Direct instantiation
        self.config = config_loader.load()  # Global access
```

### Phase 2: Create Container

Implement the DI container:
```python
import threading
from typing import Callable, Any, Dict, Optional

class DIContainer:
    def __init__(self):
        self._singletons: Dict[str, Any] = {}
        self._factories: Dict[str, Callable] = {}
        self._lock = threading.Lock()
    
    def register_singleton(self, name: str, factory: Callable[[], Any]):
        """Register a singleton factory"""
        with self._lock:
            self._factories[name] = ('singleton', factory)
    
    def register_factory(self, name: str, factory: Callable[[], Any]):
        """Register a factory (new instance each time)"""
        with self._lock:
            self._factories[name] = ('factory', factory)
    
    def get(self, name: str) -> Any:
        """Resolve dependency"""
        if name in self._singletons:
            return self._singletons[name]
        
        if name not in self._factories:
            raise KeyError(f"Dependency not registered: {name}")
        
        factory_type, factory = self._factories[name]
        
        if factory_type == 'singleton':
            with self._lock:
                if name not in self._singletons:
                    self._singletons[name] = factory()
                return self._singletons[name]
        else:
            return factory()
```

### Phase 3: Refactor Classes

Update to use injection:
```python
# Before
class MCPRouter:
    def __init__(self):
        self.discovery = BackendDiscovery()

# After
class MCPRouter:
    def __init__(self, discovery: BackendDiscovery):
        self.discovery = discovery
```

### Phase 4: Setup Wiring

```python
def configure_container(container: DIContainer):
    # Register singletons
    container.register_singleton('config', lambda: ConfigLoader())
    container.register_singleton('http_client', lambda: httpx.AsyncClient(timeout=30.0))
    
    # Register factories
    container.register_factory('router', lambda: MCPRouter(
        discovery=container.get('discovery'),
        http_client=container.get('http_client')
    ))
    
    return container
```

---

## Circular Dependency Detection

```python
class CircularDependencyError(Exception):
    pass

class DIContainer:
    def __init__(self):
        self._resolving = set()  # Track currently resolving
    
    def get(self, name: str) -> Any:
        if name in self._resolving:
            raise CircularDependencyError(
                f"Circular dependency detected: {name}"
            )
        
        self._resolving.add(name)
        try:
            # ... resolution logic
        finally:
            self._resolving.remove(name)
```

---

## Testing with Mocks

```python
import pytest
from unittest.mock import AsyncMock, MagicMock

@pytest.fixture
def mock_container():
    container = DIContainer()
    container.register_singleton('discovery', lambda: MagicMock())
    container.register_singleton('http_client', lambda: AsyncMock())
    return container

async def test_router(mock_container):
    router = MCPRouter(
        discovery=mock_container.get('discovery'),
        http_client=mock_container.get('http_client')
    )
    
    # Mock the discovery
    mock_discovery = mock_container.get('discovery')
    mock_discovery.get_server.return_value = MagicMock()
    
    # Test
    result = await router.route('backend1', 'server1', 'tool', {})
    
    mock_discovery.get_server.assert_called_once()
```

---

## Benefits

| Benefit | Description |
|---------|-------------|
| Testability | Inject mocks/stubs |
| Flexibility | Easy to swap implementations |
| Clarity | Dependencies explicit |
| Lifecycle | Singleton/factory per dependency |