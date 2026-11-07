---
name: audit-repo
description: Audit systématique des repos existants avant toute proposition de création. Vérifie la SOT (known_repositories.yaml), audite le repo cible, et détermine si le composant existe déjà, doit être étendu ou remplacé.
version: 1.0.0
intent_hash: 0xAUDIT_REPO_SKILL_20260809
---

# Audit Repo — Skill KiloCode

## Objectif

Éviter les réimplémentations inutiles et les propositions hors-sol en systématisant l'audit des repos existants **avant** toute proposition de nouveau composant.

## Déclencheur

Avant toute action qui :
- Propose un nouveau repo ou module
- Référence un composant par nom sans vérifier son existence
- Modifie un composant existant sans auditer son état actuel
- Crée une dépendance vers un repo dont on n'a pas vérifié la SOT

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `repo_name` | string | ✅ | Nom du repo à auditer (ex: `KORX`) |
| `source_repo` | string | ✅ | Repo où la demande a été formulée (pour traçabilité) |
| `layer_hint` | string | ❌ | State attendue (L0, L1, L2, L3, L4, L5) |
| `capabilities` | array | ❌ | Fonctionnalités attendues (pour comparaison) |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `exists` | bool | Le repo existe-t-il dans `known_repositories.yaml` ? |
| `local_path` | string | Chemin local du clone (si existe) |
| `layer` | string | Strate documentée dans la SOT |
| `role` | string | Rôle déclaré dans la SOT |
| `language` | string | Langage principal détecté |
| `implemented` | array | Fonctionnalités implémentées identifiées |
| `missing` | array | Fonctionnalités manquantes vs besoins |
| `recommendation` | enum | `use` / `extend` / `replace` / `create` |
| `evidence` | array | Preuves (fichiers, commits, README) |

## Protocole Obligatoire

### Étape 1 — Vérifier la SOT

```
GET gerivdb/GOVERNANCE-HUB/known_repositories.yaml
→ Chercher full_name = gerivdb/<REPO_CIBLE>
→ Si NON trouve → Recommandation: create
→ Si trouve → continuer Étape 2
```

### Étape 2 — Vérifier le chemin local

```
→ Lire le champ local_path du repo trouvé
→ Vérifier si le dossier existe physiquement
→ Si EXISTE → auditer le contenu
→ Si N'EXISTE PAS → Recommandation: create (avec HITL)
```

### Étape 3 — Auditer le contenu

```
→ Lister les fichiers principaux (README, src/, build., package.json, Cargo.toml)
→ Identifier le langage et les dépendances
→ Rechercher les fonctionnalités liées aux besoins
→ Comparer capabilities attendues vs implémentées
```

### Étape 4 — Rechercher les gaps

```
→ Pour chaque capacité attendue :
  → Chercher dans le code (grep, glob)
  → Si trouvé → implemented
  → Si non trouvé → missing
```

### Étape 5 — Émettre la recommandation

| Condition | Recommandation |
|-----------|----------------|
| Repo existe + couvre tous les besoins | `use` |
| Repo existe + couvre partiellement les besoins | `extend` |
| Repo existe + ne couvre pas les besoins | `replace` ou `create` selon écart |
| Repo n'existe pas | `create` |

## Exemple de Sortie

```yaml
audit_repo:
  repo_name: KORX
  exists: true
  local_path: D:\DO\WEB\TOOLS\L4-TOOLS\KORX
  layer: L4_TOOLS
  role: State Machine Compiler
  language: Zig 0.15.2
  implemented:
    - compilation JSON → .kbin
    - decompilation .kbin → JSON
    - memory-map .kbin
    - lexer primitives @N, @E, @S, @Q, @B, @P
  missing:
    - effets After Effects
    - pattern detection
    - mémoire sémantique
  recommendation: extend
  evidence:
    - README.md
    - src/compiler.zig
    - src/kbin.zig
```

## Anti-patterns

- ❌ Proposer un nouveau repo sans vérifier `known_repositories.yaml`
- ❌ Dire "à implémenter" sans auditer l'existant
- ❌ Confondre "je ne trouve pas dans le contexte" avec "n'existe pas"
- ❌ Réimplémenter un composant existant par préférence personnelle

## Référence ADR

- **ADR** : ADR-20260622-001-illegitimate-clone-prevention
- **IntentHash** : 0xADR_ILLEGIT_CLONE_PREV_20260622
- **Dépôt** : gerivdb/GOVERNANCE-HUB

## Référence Règles

- **Règle** : clone-causal-prevention
- **Règle** : hitl-clone-gate
