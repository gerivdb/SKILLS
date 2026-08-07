---
name: ontology-guardian
description: >
  Validation unifiée du glossaire ONTOLOGY et des crosslinks entre artefacts.
  Scanne les chemins, noms de fichiers et contenu Markdown/YAML/JSON pour détecter
  les termes non déclarés dans ONTOLOGY/ONTOLOGY.yaml.
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

# Skill — ONTOLOGY Guardian

> **Verdict** : **SKILL D’EXÉCUTION** — Validation unifiée du glossaire ONTOLOGY et détection
> de divergence terminologique sur les chemins, noms de fichiers et contenu.

---

## Objectif

Empêcher la divergence ontologique en vérifiant que tout terme utilisé dans :
- les chemins de fichiers
- les noms de fichiers
- le contenu Markdown/YAML/JSON

est bien défini dans `ONTOLOGY/ONTOLOGY.yaml`.

---

## Principes

| Principe | Règle d’application |
|----------|---------------------|
| **Ontologie d’abord** | Aucun terme ne peut être utilisé sans être défini dans `ONTOLOGY/ONTOLOGY.yaml` |
| **Scan systématique** | Toute modification de fichier déclenche un scan des termes |
| **Blocage préventif** | Le commit/PR est bloqué si un terme inconnu est détecté |
| **Short-circuit NEUTRE** | En cas d’ambiguïté, retourner NEUTRE et ne pas créer de lien |

---

## Processus

### Étape 1 — Charger l’ontologie

```powershell
python .kilo/scripts/verify-terms.py --ontology ONTOLOGY/ONTOLOGY.yaml
```

### Étape 2 — Scanner les fichiers modifiés

```powershell
# Fichiers staged
$staged = git diff --cached --name-only --diff-filter=AM

# Fichiers modifiés non staged
$modified = git diff --name-only

$all = $staged + $modified
```

### Étape 3 — Extraire les termes

Pour chaque fichier :
- **Chemin** : extraire `PRD-MOC-{CONTEXT}`, `EPIC-{N}`, noms de dossiers
- **Contenu** : extraire `PRD-MOC-{CONTEXT}`, `EPIC-{N}`, termes techniques

### Étape 4 — Vérifier contre l’ontologie

```python
# Pour chaque terme extrait
if term not in ontology_terms:
    BLOCK Commit/PR
    Logger: "Terme '{term}' non déclaré dans ONTOLOGY/ONTOLOGY.yaml"
```

### Étape 5 — Reporter

```ascii
+-----------------------------------------------------------------------------+
| TERME    FICHIER    LIGNE    ACTION                                          |
+-----------------------------------------------------------------------------+
| N243     PRD/...    L12      BLOQUÉ — terme repo utilisé comme nom MOC       |
+-----------------------------------------------------------------------------+
```

---

## Rôles

| Rôle | Responsabilité |
|------|----------------|
| `ARGUS` | Détecte les termes litigieux et les divergences |
| `ONTOLOGY-GUARDIAN` | Valide la conformité des termes à l’ontologie L0 |
| `MOX` | Valide la structure AEP |
| `NEXUS` | Trace les modifications dans WAL |

---

## Probes

```ascii
+-----------------------------------------------------------------------------+
| PROBE    CONDITION → COMPORTEMENT ATTENDU                                   |
+-----------------------------------------------------------------------------+
| P-901    Tous les termes des chemins sont dans ONTOLOGY                      |
| P-902    Tous les termes des noms de fichiers sont dans ONTOLOGY             |
| P-903    Tous les termes du contenu sont dans ONTOLOGY                       |
| P-904    Aucun terme interdit (forbidden_aliases) n’est utilisé              |
| P-905    verify-terms.py passe en pre-commit et CI                           |
+-----------------------------------------------------------------------------+
```

---

## Critères

```ascii
+-----------------------------------------------------------------------------+
| CRITÈRE    DESCRIPTION                                                      |
+-----------------------------------------------------------------------------+
| ✓          Aucun terme inconnu dans les chemins                              |
| ✓          Aucun terme inconnu dans les noms de fichiers                    |
| ✓          Aucun terme inconnu dans le contenu                              |
| ✓          Aucun terme interdit utilisé                                     |
| ✓          verify-terms.py passe                                            |
+-----------------------------------------------------------------------------+
```

---

## Rollback

1. Supprimer les fichiers non conformes.
2. Logger dans WAL.
3. Corriger via PR review ARGUS.

---

## Références

- `ONTOLOGY/ONTOLOGY.yaml`
- `.kilo/scripts/verify-terms.py`
- `unified-design/designs/actprotocol-fractal-nomenclature.yaml`
- `PRD-MOC-ACTPROTOCOL/fractal/PRD-MOC-ACTPROTOCOL-SKILLS-CITIZENS-2026-08-06.md`
