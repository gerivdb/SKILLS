---
name: verify-terms
description: >
  Scan des chemins, noms de fichiers et contenu pour valider que tous les termes
  utilises sont declares dans ONTOLOGY/ONTOLOGY.yaml.
  Bloque le commit/CI si un terme inconnu ou interdit est detecte.
  Utiliser en pre-commit hook et CI pour garantir la non-divergence ontologique.
version: "1.0.0"
status: active
intent_hash: 0xVERIFY_TERMS_20260806
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/verify-terms/SKILL.md
triggers:
  - "verify-terms"
  - "terme absent de ONTOLOGY"
  - "divergence ontologique"
  - "pre-commit nomenclature"
tools:
  - bash
  - read
  - grep
citizen: "ARGUS"
layer: "L4"
---

# Skill - Verify Terms

> **Verdict** : **SKILL D'EXECUTION** - Scan terminologique pour bloquer la divergence ontologique
> avant commit/CI.

---

## Objectif

Verifier que tous les termes utilises dans :
- les chemins de fichiers
- les noms de fichiers
- le contenu Markdown/YAML/JSON

sont bien definis dans `ONTOLOGY/ONTOLOGY.yaml`.

---

## Processus

### Etape 1 - Charger l'ontologie

```powershell
python .kilo/scripts/verify-terms.py --ontology ONTOLOGY/ONTOLOGY.yaml
```

### Etape 2 - Scanner les fichiers modifies

```powershell
$staged = git diff --cached --name-only --diff-filter=AM
$modified = git diff --name-only
$all = $staged + $modified
```

### Etape 3 - Extraire les termes

Pour chaque fichier :
- **Chemin** : `PRD-MOC-{CONTEXT}`, `EPIC-{N}`, noms de dossiers
- **Contenu** : `PRD-MOC-{CONTEXT}`, `EPIC-{N}`, termes techniques

### Etape 4 - Verifier contre l'ontologie

```python
if term not in ontology_terms:
    BLOCK Commit/PR
```

### Etape 5 - Reporter

```ascii
+-----------------------------------------------------------------------------+
| TERME    FICHIER    LIGNE    ACTION                                          |
+-----------------------------------------------------------------------------+
| N243     PRD/...    L12      BLOQUE - terme repo utilise comme nom MOC       |
+-----------------------------------------------------------------------------+
```

---

## Roles

| Role | Responsabilite |
|------|----------------|
| `ARGUS` | Detecte les termes litigieux |
| `ONTOLOGY-GUARDIAN` | Valide la conformite |
| `NEXUS` | Trace dans WAL |

---

## Probes

```ascii
+-----------------------------------------------------------------------------+
| PROBE    CONDITION -> COMPORTEMENT ATTENDU                                   |
+-----------------------------------------------------------------------------+
| P-701    Tous les termes des chemins sont dans ONTOLOGY                      |
| P-702    Tous les termes des noms de fichiers sont dans ONTOLOGY             |
| P-703    Tous les termes du contenu sont dans ONTOLOGY                       |
| P-704    Aucun terme interdit (forbidden_aliases) n'est utilise              |
| P-705    verify-terms.py passe en pre-commit et CI                           |
| P-706    verify-terms.py bloque les termes inconnus                          |
+-----------------------------------------------------------------------------+
```

---

## Criteres

```ascii
+-----------------------------------------------------------------------------+
| CRITERE    DESCRIPTION                                                      |
+-----------------------------------------------------------------------------+
| [OK]          Aucun terme inconnu dans les chemins                              |
| [OK]          Aucun terme inconnu dans les noms de fichiers                    |
| [OK]          Aucun terme inconnu dans le contenu                              |
| [OK]          Aucun terme interdit utilise                                     |
| [OK]          verify-terms.py passe                                            |
+-----------------------------------------------------------------------------+
```

---

## Rollback

1. Supprimer les fichiers non conformes.
2. Logger dans WAL.
3. Corriger via PR review ARGUS.

---

## References

- `ONTOLOGY/ONTOLOGY.yaml`
- `.kilo/scripts/verify-terms.py`
- `unified-design/designs/actprotocol-fractal-nomenclature.yaml`
