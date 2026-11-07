---
type: SKILL
version: "1.0.0"
status: active
date: "2026-10-25"
intent_hash: 0xSKILL_WCA_20261025
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/webview-runtime-crash-analyzer/SKILL.md
---

# Skill — webview-runtime-crash-analyzer

## Objectif

Corréler l'état manquant avec le plantage de l'arbre de composants React Webview. Détecter les exceptions `Cannot read properties of undefined` provoquant le démontage du DOM d'input. Prescrire l'état neutre de repli pour forcer un rendu propre à froid. Couche Rendu React & ErrorBoundary.

## Déclencheur

- Zone de saisie agent absente après rechargement.
- Exception React `Cannot read properties of undefined (reading '...')` dans la console webview.
- Démontage du composant d'entrée (input DOM retiré).
- Rendu blanc persistant malgré un état agent valide.

## Entrées

- `webview_log_path`: chemin vers les logs de la webview agent (console / devtools).
- `state_path`: chemin vers `agent-manager.json` pour vérifier l'état neutre.
- `fallback_state`: état neutre de repli à prescrire (optionnel).

## Sorties

- Rapport JSON des exceptions React détectées avec stack trace.
- État de l'arbre de composants (démonté / actif).
- Prescription d'état neutre de repli.
- Entrée WAL NEXUS horodatée.

## Règles

### 1. Scanner les logs de la webview

- Rechercher les exceptions `Cannot read properties of undefined`.
- Capturer le stack trace associé (fichier, ligne, colonne).
- Identifier le composant React en cause (souvent l'input ou le SidebarProvider).

### 2. Vérifier l'état du DOM d'input

- Détecter si le composant d'entrée a été démonté (plus présent dans l'arbre React).
- Corréler avec l'exception détectée : si l'exception précède le démontage, c'est la cause racine.

### 3. Corréler avec l'état agent

- Lire `agent-manager.json` pour vérifier si l'état agent est valide.
- Si l'état agent est valide mais le DOM est démonté → le crash est purement côté React rendering.

### 4. Prescrire l'état neutre de repli

- Générer un JSON d'état neutre : `{ sessions: {}, activeTarget: null, tabOrder: { local: [] } }`.
- Ce state vide force un rendu propre à froid sans référence à des sessions détruites.
- Recommander l'application de cet état via `ssot-referential-integrity` ou `vscode-storage-memento-inspector`.

## Script d'investigation

`scripts/analyze.ps1` — voir ci-dessous.

## Tests

- `tests/test_webview_runtime_crash_analyzer.ps1` — créer un log webview avec exception React, vérifier la détection et la prescription d'état neutre.

## Probes

- Zéro exception `Cannot read properties of undefined` récurrente après application de l'état neutre.
- Rendu de la zone de saisie rétabli après redémarrage webview.

## WAL NEXUS

```
[WAL_NEXUS] skill=webview-runtime-crash-analyzer action=analyze timestamp=<ISO> log_path=<PATH> exceptions=<n> component_demounted=<bool>
[WAL_NEXUS] skill=webview-runtime-crash-analyzer action=prescribe_fallback timestamp=<ISO> fallback_state=<JSON> applied=<bool>
```

## Référence ADR

- **ADR** : ADR-2026-05-14-004-KILO-CODE-HOTL-OPERATIONAL-STD
- **IntentHash** : 0xB05F1124CDC61605
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed
