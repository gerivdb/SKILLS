---
trit_primitive: TritRunTests
---
# WAZAA Bus Test Generator Skill

## Purpose
Auto-generate unit tests for new WAZAA bus modules and wazaa_client implementations.

## When to Use
- After creating a new `wazaa_client.py` in any agent repo
- After modifying `WAZAA/src/wazaa_bus.py`
- After adding new event types to `event_schema.yaml`

## Workflow

### Step 1: Identify the module to test
```bash
# Find all wazaa_client.py files
Get-ChildItem -Path "D:\DO\WEB" -Filter "wazaa_client.py" -Recurse | Select-Object FullName
```

### Step 2: Generate test scaffold
For each module, create a test file with:
1. Import tests (module loads without errors)
2. Factory tests (create functions return correct types)
3. Method tests (each public method with valid/invalid inputs)
4. Edge cases (boundary values, empty inputs, timeouts)

### Step 3: Run and validate
```bash
cd <repo>
python -m pytest tests/ -v --tb=short
```

### Step 4: Check GATE-5 compliance
```bash
python -m pytest tests/ -v --tb=short --cache-clear
# Verify no emojis in test output
```

## Test Template

```python
#!/usr/bin/env python3
"""Tests for <module_name>"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from <module> import <Class>


class Test<ClassName>(unittest.TestCase):
    def setUp(self):
        self.obj = <Class>()

    def test_create(self):
        self.assertIsNotNone(self.obj)

    def test_<method>(self):
        result = self.obj.<method>()
        self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()
```

## Constraints
- All test strings must be ASCII (GATE-5)
- Use `[OK]`, `[FAIL]`, `[WARN]` instead of emoji indicators
- Test file naming: `test_<module_name>.py`
- Place in `tests/` directory of the target repo
