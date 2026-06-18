# Python CLI Structure — Architecture src/cli/ + src/core/

## Description

Architecture standard pour les outils CLI Python de l'écosystème gerivdb — structure `src/cli/` + `src/core/` avec entry point Click, pyproject.toml, et tests. Ce skill documente le pattern utilisé par CAPTA-4D, KIVA-CLI, et les autres outils Python du metacluster.

## Quand l'utiliser

- Création d'un nouveau CLI Python dans l'écosystème
- Restructuration d'un outil existant vers le pattern `src/cli/` + `src/core/`
- Configuration de `pyproject.toml` avec `[project.scripts]`
- Ajout de commandes Click

## Structure standard

```
<repo>/
├── pyproject.toml          # [project.scripts] entry point
├── src/
│   ├── <package>/
│   │   ├── __init__.py
│   │   ├── cli/
│   │   │   ├── __init__.py
│   │   │   └── main.py     # Click group + commands
│   │   └── core/
│   │       ├── __init__.py
│   │       ├── module_a.py
│   │       └── module_b.py
│   └── config/
│       └── default.yaml
├── tests/
│   ├── __init__.py
│   ├── test_module_a.py
│   └── test_cli.py
└── scripts/
    └── check_scene.py      # Scripts utilitaires
```

## pyproject.toml — Configuration minimale

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "<package>"
version = "0.1.0"
description = "<description>"
requires-python = ">=3.11"
dependencies = [
    "click>=8.0",
    "pyyaml>=6.0",
    "numpy>=1.24",
]

[project.scripts]
<command> = "<package>.cli.main:cli"

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "black>=23.0",
    "ruff>=0.1.0",
    "mypy>=1.0",
]

[tool.black]
line-length = 99

[tool.ruff]
line-length = 99

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--cov=<package> --cov-report=term-missing --cov-fail-under=85"
```

## Pattern CLI Click

```python
# src/<package>/cli/main.py
import click
from <package>.core.<module> import <function>

@click.group()
def cli():
    """<Description>."""
    pass

@cli.command()
@click.argument('profile')
@click.argument('x', type=float)
@click.argument('y', type=float)
@click.argument('z', type=float)
def solve(profile, x, y, z):
    """<Description>."""
    result = <function>(profile, x, y, z)
    click.echo(f"Result: {result}")

if __name__ == '__main__':
    cli()
```

## Convention de nommage

| Élément | Convention | Exemple |
|---------|-----------|---------|
| Package | `kebab-case` | `capta4d` |
| Entry point | `kebab-case` | `capta-4d` |
| Modules core | `snake_case` | `kinematics.py` |
| Commandes CLI | `kebab-case` | `capta-4d solve` |
| Tests | `test_<module>.py` | `test_kinematics.py` |

## Références

- Exemple principal: `gerivdb/CAPTA-4D/`
- Référence CLI: `gerivdb/KIVA-CLI/`
- Standards: `gerivdb/REPO-STANDARDS/`
