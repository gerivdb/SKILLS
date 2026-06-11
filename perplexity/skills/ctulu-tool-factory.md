---
name: ctulu-tool-factory
description: "A partir d'un nom de tool + d'une source de donnees (GitHub API endpoint, fichier type, CI report format), genere le fichier tools/<nom>_adapter.py complet avec fetch(), normalize(), to_dict(), tests unitaires inclus."
version: "1.0.0"
triggers:
  - "ctulu tool"
  - "generer adapter"
  - "nouveau tool ctulu"
  - "tool factory"
  - "adapter generator"
layer: "L2_COMPOSITION"
nexusTags: ["CONFORME_NEXUS", "CTULU", "TOOL_FACTORY"]
status: "active"
changelog:
  - {v: "1.0.0", date: "2026-06-11", notes: "Creation — pattern detecte dans N+20+21 (12 tools CTULU identiques)"}
slotWeight: 2
trit_primitive: TritDoConfig
---

# CTULU-TOOL-FACTORY — Generation de tools CTULU

## Domaine et perimetre

Ce skill genere un fichier tool CTULU complet a partir d'un nom et d'une source de donnees. Le pattern a ete detecte dans N+20+21 ou 12 tools ont ete crees avec la meme structure.

## Template de generation

### Entree

- `tool_name` : nom du tool (ex: "branch_visualizer")
- `source_type` : type de source (github_api / file / ci_report)
- `api_endpoint` : endpoint GitHub API si applicable
- `output_schema` : schema de sortie attendu

### Sortie

Fichier `tools/<tool_name>.py` avec :

```python
class <ToolName>Adapter:
    def fetch(self) -> dict:
        """Recupere les donnees depuis la source."""
        ...

    def normalize(self, raw: dict) -> dict:
        """Normalise les donnees brutes."""
        ...

    def to_dict(self) -> dict:
        """Retourne le resultat structure."""
        ...

    def get_summary(self) -> dict:
        """Retourne un resume."""
        ...
```

Plus tests unitaires `tests/tools/test_<tool_name>.py`.

## Methodologie

1. Generer le fichier Python avec le template
2. Generer les tests unitaires
3. Verifier la compilation
4. Ouvrir la PR

## Integration

- **Declencheur** : Creation d'un nouveau tool CTULU
- **Pattern source** : N+20+21 (12 tools)
