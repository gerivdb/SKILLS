---
name: ontology-guardian
description: >
  Validation active des termes ontologiques avant ecriture de documents gouvernants.
  Bloque l'usage de termes non declares dans ONTOLOGY/ONTOLOGY.yaml.
  Utiliser comme garde avant toute creation/modification de PRD, INTENT, EPIC, ADR, README.
version: "1.0.0"
status: active
intent_hash: 0xONTOLOGY_GUARDIAN_20260806
author: gerivdb
source_repo: gerivdb/ONTOLOGY
source_path: SKILLS/ontology-guardian/SKILL.md
triggers:
  - "terme ontologique"
  - "verifier terme"
  - "bloquer terme"
  - "ONTOLOGY validation"
  - "concept non declare"
tools:
  - bash
  - read
  - grep
citizen: "MOX"
layer: "L4"
---

# Skill — Ontology Guardian

> **Verdict** : **SKILL D'EXÉCUTION** — Garde actif contre l'usage de termes non déclarés dans ONTOLOGY.

---

## Objectif

Empêcher la création/modification de documents gouvernants (PRD, INTENT, EPIC, ADR, README)
utilisant des termes **non déclarés** dans `ONTOLOGY/ONTOLOGY.yaml`.

---

## Règle fondamentale

**Aucun terme utilisé comme identifiant stable dans un document gouvernant ne peut être utilisé s'il n'est pas déclaré dans ONTOLOGY/ONTOLOGY.yaml.**

### Termes autorisés

- Termes déclarés dans `ONTOLOGY/ONTOLOGY.yaml` sous `entities.terms`
- Aliases autorisés d'un terme déclaré

### Termes interdits

- N'importe quel terme utilisé comme slug/identifiant dans un nom de fichier/document sans être déclaré dans ONTOLOGY
- Exemples d'interdiction :
  - `N243` si non déclaré → maintenant autorisé car déclaré
  - `PRD-MOC-N243` autorisé car alias de N243
  - `INTENT-N243` autorisé car alias de N243
  - Tout autre terme non déclaré → BLOQUÉ

---

## Processus

### Étape 1 — Extraire les termes du document

```powershell
# Extraire tous les termes potentiels du document
$content = Get-Content "document.md" -Raw
$terms = [regex]::Matches($content, '(?i)(prd|intent|epic|adr|moc|repo|skill|citizen|persona)[-_]([a-zA-Z0-9_-]+)') | ForEach-Object { $_.Groups[2].Value }
$terms | Sort-Object -Unique
```

### Étape 2 — Vérifier contre ONTOLOGY

```powershell
# Charger ONTOLOGY.yaml
$ontology = Get-Content "D:\DO\WEB\ONTOLOGY\ONTOLOGY.yaml" -Raw | ConvertFrom-Yaml
$declaredTerms = $ontology.entities.terms.PSObject.Properties.Name

# Vérifier chaque terme
$undeclared = $terms | Where-Object { $_ -notin $declaredTerms }
if ($undeclared) {
  Write-Error "TERMES NON DECLARES: $($undeclared -join ', ')"
  exit 1
}
```

### Étape 3 — Autoriser / Bloquer

| Cas | Action |
|-----|--------|
| Tous les termes déclarés | ✅ Autoriser |
| Terme non déclaré | ❌ Bloquer + exiger déclaration ONTOLOGY d'abord |

---

## Rôles

| Rôle | Responsabilité |
|------|----------------|
| `MOX` | Valide la conformité ontologique avant commit |
| `ARGUS` | Détecte les termes manquants dans ONTOLOGY |
| `NEXUS` | Trace les violations et corrections |
| `ONTOLOGY-GUARDIAN` | Skill d'exécution de la garde |

---

## Probes

```ascii
+-----------------------------------------------------------------------------+
| PROBE    CONDITION → COMPORTEMENT ATTENDU                                   |
+-----------------------------------------------------------------------------+
| P-1401   Tous les termes des PRD/INTENT/EPIC sont déclarés dans ONTOLOGY   |
| P-1402   Aucun terme non déclaré utilisé comme identifiant stable           |
| P-1403   N243 est déclaré dans ONTOLOGY avec aliases PRD-MOC-N243, INTENT-N243 |
| P-1404   Toute nouvelle entrée dans ONTOLOGY est tracée dans WAL            |
+-----------------------------------------------------------------------------+
```

---

## Critères

```ascii
+-----------------------------------------------------------------------------+
| CRITÈRE    DESCRIPTION                                                      |
+-----------------------------------------------------------------------------+
| ✓          Zéro terme non déclaré dans docs gouvernants                     |
| ✓          N243 déclaré avec aliases autorisés                             |
| ✓          Toute modification d'ONTOLOGY tracée dans WAL                   |
+-----------------------------------------------------------------------------+
```

---

## Rollback

1. Identifier le document avec terme non déclaré.
2. Restaurer depuis git.
3. Logger la violation dans WAL.
4. Corriger via PR review MOX.

---

## Références

- `ONTOLOGY/ONTOLOGY.yaml`
- `ONTOLOGY/schema/*.yaml`
- `GOVERNANCE-HUB/known_repositories.yaml`
- `TOPOS/repo-manifest.yaml`
