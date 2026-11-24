---
name: windmill
description: Transforme des scripts (Python, TypeScript, Go, Bash) et workflows en briques typées, versionnées et rejouables. Pattern inspiré de https://github.com/windmill-labs/windmill
version: 1.0.0
intent_hash: 0xSKILL_WINDMILL_20261124
layer: L4-TOOLS
author: gerivdb
source_repo: external/windmill-labs/windmill
source_url: https://github.com/windmill-labs/windmill
path: windmill
---

# Windmill — Skill KiloCode

## Objectif

Transformer des scripts (Python, TypeScript, Go, Bash) et workflows en briques typées, versionnées et rejouables. Ce skill encapsule le pattern du repo externe `windmill` adapté à ENV2, avec respect des règles BDCP et Shell-Only.

## Déclencheur

Ce skill s'active quand :
- Un script autonome doit être transformé en brique typée et versionnée
- Un workflow doit être décomposé en briques rejouables
- Un script doit être exposé comme skill canonique avec preuve d'exécution
- La versioning de scripts doit être formalisée

## Entrée

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `script_path` | string | ✅ | Chemin absolu vers le script à transformer |
| `script_language` | enum | ✅ | python / typescript / go / bash / powershell |
| `entrypoint` | string | ❌ | Point d'entrée du script (fonction ou commande) |
| `version` | string | ❌ | Version semver (défaut: 1.0.0) |

## Sortie

| Champ | Type | Description |
|-------|------|-------------|
| `typed_brick` | string | Nom de la brique typée générée |
| `brick_path` | string | Chemin absolu vers la brique générée |
| `type_signature` | string | Signature typée des entrées/sorties |
| `version` | string | Version semver de la brique |
| `evidence_hash` | string | Hash SHA-256 de la brique générée |

## Protocole Obligatoire

### Étape 1 — Analyse du script

```
→ Lire le script source
→ Identifier les entrées, sorties et effets de bord
→ Déduire la signature typée (types d'entrée et de sortie)
→ Vérifier que le script respecte les règles BDCP (pas de réseau direct, CDP uniquement)
```

### Étape 2 — Transformation en brique typée

```
→ Créer le répertoire de la brique sous D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\
→ Générer le SKILL.md avec frontmatter et signature typée
→ Envelopper le script dans une interface skill standardisée
→ Valider que l'exécution retourne un code de retour (0 = succès)
```

### Étape 3 — Versioning

```
→ Assigner une version semver (v1.0.0 initial)
→ Enregistrer la version dans skills-index.json
→ À chaque modification, incrémenter selon semver (patch/minor/major)
```

### Étape 4 — Rejouabilité

```
→ Tester la brique en isolation (exécution standalone)
→ Capturer la preuve brute (stdout, code de retour, hash SHA-256, timestamp UTC)
→ Vérifier que la brique est idempotente (même entrée → même sortie)
→ Enregistrer dans le WAL (WAL-0x243)
```

## Anti-patterns

- ❌ Transformer un script sans signature typée
- ❌ Utiliser pwsh -Command ou powershell -Command (interdit par Shell-Only, utiliser cmd /c ou bash -c)
- ❌ Oublier le hash SHA-256 et l'horodatage UTC
- ❌ Ne pas tester la brique en isolation avant enregistrement

## Référence ADR

- **ADR** : ADR-2026-11-24-001-SHELL-ONLY-NO-INTERACTIVE
- **IntentHash** : 0xADR_SHELL_ONLY_NO_INTERACTIVE_20261124
- **Dépôt** : gerivdb/GOVERNANCE-HUB

## Référence Règles

- **Règle** : shell-only-no-interactive
- **Règle** : skill-citizen-prealable
- **Règle** : explicit-path-compliance
- **Règle** : proof-recalculation
