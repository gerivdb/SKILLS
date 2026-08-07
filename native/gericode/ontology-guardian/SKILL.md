---
name: ontology-guardian
description: >
  Validation unifiee du glossaire ONTOLOGY et des crosslinks entre artefacts.
  Scanne les chemins, noms de fichiers et contenu Markdown/YAML/JSON pour detecter
  les termes non declares dans ONTOLOGY/ONTOLOGY.yaml.
  Utiliser avant tout commit/PR pour bloquer la divergence terminologique.
version: "1.0.0"
status: active
intent_hash: 0xONTOLOGY_GUARDIAN_20260806
author: gerivdb
source_repo: gerivdb/GeriCode
source_path: .kilo/skills/ontology-guardian/SKILL.md
triggers:
  - "terme absent de ONTOLOGY"
  - "divergence ontologique"
  - "glossary validation"
  - "cross-artifact validation"
  - "verify-terms"
tools:
  - bash
  - read
  - grep
citizen: "ARGUS"
layer: "L4"
---

# Skill - ONTOLOGY Guardian

> **Verdict** : **SKILL D'EXECUTION** - Validation unifiee du glossaire ONTOLOGY et detection
> de divergence terminologique sur les chemins, noms de fichiers et contenu.

---

## Objectif

Empecher la divergence ontologique en verifiant que tout terme utilise dans :
- les chemins de fichiers
- les noms de fichiers
- le contenu Markdown/YAML/JSON

est bien defini dans `ONTOLOGY/ONTOLOGY.yaml`.

---

## Principes

| Principe | Regle d'application |
|----------|---------------------|
| **Ontologie d'abord** | Aucun terme ne peut etre utilise sans etre defini dans `ONTOLOGY/ONTOLOGY.yaml` |
| **Scan systematique** | Toute modification de fichier declenche un scan des termes |
| **Blocage preventif** | Le commit/PR est bloque si un terme inconnu est detecte |
| **Short-circuit NEUTRE** | En cas d'ambiguite, retourner NEUTRE et ne pas creer de lien |

---

## Processus

### Etape 1 - Charger l'ontologie

```powershell
python .kilo/scripts/verify-terms.py --ontology ONTOLOGY/ONTOLOGY.yaml
```

### Etape 2 - Scanner les fichiers modifies

```powershell
# Fichiers staged
$staged = git diff --cached --name-only --diff-filter=AM

# Fichiers modifies non staged
$modified = git diff --name-only

$all = $staged + $modified
```

### Etape 3 - Extraire les termes

Pour chaque fichier :
- **Chemin** : extraire `PRD-MOC-{CONTEXT}`, `EPIC-{N}`, noms de dossiers
- **Contenu** : extraire `PRD-MOC-{CONTEXT}`, `EPIC-{N}`, termes techniques

### Etape 4 - Verifier contre l'ontologie

```python
# Pour chaque terme extrait
if term not in ontology_terms:
    BLOCK Commit/PR
    Logger: "Terme '{term}' non declare dans ONTOLOGY/ONTOLOGY.yaml"
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
| `ARGUS` | Detecte les termes litigieux et les divergences |
| `ONTOLOGY-GUARDIAN` | Valide la conformite des termes a l'ontologie L0 |
| `MOX` | Valide la structure AEP |
| `NEXUS` | Trace les modifications dans WAL |

---

## Probes

```ascii
+-----------------------------------------------------------------------------+
| PROBE    CONDITION -> COMPORTEMENT ATTENDU                                   |
+-----------------------------------------------------------------------------+
| P-901    Tous les termes des chemins sont dans ONTOLOGY                      |
| P-902    Tous les termes des noms de fichiers sont dans ONTOLOGY             |
| P-903    Tous les termes du contenu sont dans ONTOLOGY                       |
| P-904    Aucun terme interdit (forbidden_aliases) n'est utilise              |
| P-905    verify-terms.py passe en pre-commit et CI                           |
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
- `PRD-MOC-ACTPROTOCOL/fractal/PRD-MOC-ACTPROTOCOL-SKILLS-CITIZENS-2026-08-06.md`
