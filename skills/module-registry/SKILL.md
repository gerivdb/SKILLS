---
type: skill
version: "1.0.0"
date: "2026-08-02"
intent_hash: 0xSKL007_MODULE_REGISTRY_20260802
status: active
---

# Skill: SKL007 — Module Registry (ADMG/TALEX)

## Purpose
Manages registration, discovery, and versioning of TALEX narrative modules. Each module is a self-contained narrative unit (character arc, location story, faction plotline) with ternary metadata, IntentHash locking, and dependency resolution.

## Context
TALEX narratives are composed from modular units. The Module Registry provides:
- Module registration with ternary metadata
- Dependency graph resolution (DAG)
- Version management with IntentHash
- Hot-loading for live narrative generation

## Module Structure

```yaml
module:
  id: "character_arc:detective_morality"
  version: "1.2.0"
  intent_hash: "0x..."              # Hash of module content
  type: "character_arc"             # character_arc | location_story | faction_plot | theme_exploration
  domains: [0, 7, 10]               # Affected narrative domains (0-15)
  ternary_metadata:
    state_hash: "0x..."             # 243-trit initial state
    coupling_delta: "0x..."         # Coupling matrix modifications
    program_hash: "0x..."           # Generation program hash
  dependencies:
    - "location_story:baker_street"
    - "faction_plot:scotland_yard"
  provides:
    - "character:detective"
    - "theme:morality"
  requires:
    - "lore:victorian_etiquette"
    - "lore:detective_procedures"
```

## Registry Operations

### 1. Register Module
```python
from src.primus.core import ternary_hash_to_intent_hash, validate_intent_hash

def register_module(module_spec: dict) -> tuple[bool, str]:
    # Validate structure
    required = ['id', 'version', 'intent_hash', 'type', 'domains']
    for field in required:
        if field not in module_spec:
            return False, f"Missing required field: {field}"
    
    # Verify IntentHash
    if not validate_intent_hash(module_spec['intent_hash']):
        return False, "Invalid IntentHash format"
    
    # Verify content matches hash
    content_hash = ternary_hash_to_intent_hash(str(module_spec))
    if content_hash != module_spec['intent_hash']:
        return False, f"Content hash mismatch: {content_hash} != {module_spec['intent_hash']}"
    
    # Store in registry (Redis/Filesystem/DB)
    registry[module_spec['id']] = module_spec
    return True, module_spec['id']
```

### 2. Resolve Dependencies (Topological Sort)
```python
def resolve_dependencies(module_ids: list[str]) -> list[str]:
    """Returns modules in load order (dependencies first)."""
    graph = {mid: set(registry[mid].get('dependencies', [])) for mid in module_ids}
    
    # Kahn's algorithm
    in_degree = {mid: 0 for mid in module_ids}
    for mid, deps in graph.items():
        for dep in deps:
            if dep in in_degree:
                in_degree[dep] += 1
    
    queue = [mid for mid, deg in in_degree.items() if deg == 0]
    result = []
    
    while queue:
        mid = queue.pop(0)
        result.append(mid)
        for other_mid, deps in graph.items():
            if mid in deps:
                in_degree[other_mid] -= 1
                if in_degree[other_mid] == 0:
                    queue.append(other_mid)
    
    if len(result) != len(module_ids):
        raise ValueError("Circular dependency detected")
    
    return result
```

### 3. Compute Composite State
```python
def compute_composite_state(module_ids: list[str]) -> TernaryState:
    """Merge multiple modules into single TernaryState."""
    load_order = resolve_dependencies(module_ids)
    
    # Start with zero state
    composite = TernaryState.zero(b"composite")
    
    for mid in load_order:
        module = registry[mid]
        # Apply coupling delta
        if 'coupling_delta' in module['ternary_metadata']:
            delta_hash = module['ternary_metadata']['coupling_delta']
            # Apply to composite coupling matrix
            pass
        
        # Merge program
        if 'program_hash' in module['ternary_metadata']:
            # Load and merge generation program
            pass
        
        # Update vector (domain activations)
        for domain in module['domains']:
            composite.vector.waves[domain * 5 + 2] = Wave(
                band=FrequencyBand.ALPHA, trit=Trit.POS
            )
    
    return composite
```

## Registry Storage Backends

| Backend | Use Case | Persistence |
|---------|----------|-------------|
| **Filesystem** | Development, CI | JSON/YAML files |
| **Redis** | Production, distributed | In-memory + AOF |
| **PostgreSQL** | Audit trail, querying | ACID |
| **Git** | Version history, diff | Immutable |

## Module Lifecycle

```
CREATE → REGISTER → VALIDATE → RESOLVE DEPS → LOAD → EXECUTE → VERSION BUMP
                │
                ├── FAIL: Invalid IntentHash
                ├── FAIL: Circular dependency
                └── FAIL: Lore violation (SKL002)
```

## API Interface

```python
class ModuleRegistry:
    def register(self, spec: dict) -> str: ...
    def unregister(self, module_id: str) -> bool: ...
    def get(self, module_id: str) -> dict: ...
    def list(self, type_filter: str = None) -> list[str]: ...
    def resolve(self, module_ids: list[str]) -> list[str]: ...
    def compose(self, module_ids: list[str]) -> TernaryState: ...
    def verify(self, module_id: str) -> tuple[bool, list[str]]: ...
    def diff(self, v1: str, v2: str) -> dict: ...
```

## Build Requirements
- Python 3.10+
- PRIMUS core: hash, state, types
- Storage backend (configurable)
- SKL002 (Lore Validator) for module verification

## Validation

```python
# Test module registration
module = {
    'id': 'test:module',
    'version': '1.0.0',
    'intent_hash': ternary_hash_to_intent_hash('test content'),
    'type': 'character_arc',
    'domains': [0, 1],
    'dependencies': [],
    'ternary_metadata': {
        'state_hash': ternary_hash_to_intent_hash('state'),
        'coupling_delta': ternary_hash_to_intent_hash('delta'),
        'program_hash': ternary_hash_to_intent_hash('program')
    }
}

valid, msg = register_module(module)
assert valid, msg

# Test dependency resolution
mods = ['a', 'b', 'c']
registry['a'] = {'dependencies': []}
registry['b'] = {'dependencies': ['a']}
registry['c'] = {'dependencies': ['b']}
order = resolve_dependencies(mods)
assert order == ['a', 'b', 'c']

# Test circular detection
registry['a']['dependencies'] = ['c']
try:
    resolve_dependencies(mods)
    assert False, "Should have raised circular dependency"
except ValueError:
    pass
```

## Anti-patterns
- Not verifying IntentHash on register (tampering risk)
- Skipping dependency resolution (load order errors)
- Circular dependencies (breaks DAG)
- Not versioning modules (no rollback)
- Hardcoding registry backend (use abstraction)

## References
- PRD-MOC-INVENTORY-SYNTHESIS.md (SKL007)
- PRIMUS core: hash, state, types
- SKL002 (Lore Validator)
- SKL005 (Coupling Matrix)
- TALEX module architecture
- IntentHash specification