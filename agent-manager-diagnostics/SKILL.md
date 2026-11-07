---
type: SKILL
version: "1.0.0"
intent_hash: 0xAGENT_MANAGER_DIAGNOSTICS_SKILL_20260809
---

# Agent Manager Diagnostics

## Objectif

Diagnostics standardisés pour l'environnement Agent Manager. Vérifie CLI, auth, providers et prérequis système avant toute session parallèle.

## Déclencheur

- Avant tout appel à Agent Manager
- Avant toute création de session parallèle
- Quand l'Agent Manager apparaît vide sans raison explicite

## Règles

### 1. Exécuter le script de diagnostic PowerShell

```powershell
powershell -File "scripts/verify-agent-manager-env.ps1"
```

### 2. Vérifier les résultats

| Status | Action |
|--------|--------|
| OK | Continuer |
| WARN | Vérifier manuellement, peut bloquer certaines fonctionnalités |
| ERROR | STOP — corriger avant de continuer |

### 3. Checks obligatoires

1. **CLI kilocode** : `where kilocode` / `which kilocode`
2. **Auth token** : `kilocode auth login` / token valide
3. **Providers** : Kilo Gateway, OpenAI, Anthropic configurés
4. **VS Code** : Extension disponible
5. **Git** : Git CLI disponible
6. **Node.js** : Pour scripts
7. **Python** : Pour KIX diagnostics

### 4. Intégration KIX

Si Python est disponible, exécuter :

```bash
python src/diagnostics.py --check agent-manager
```

### 5. Intégration TRIX

Si TRIX est installé, exécuter :

```bash
trix preflight
```

## Anti-patterns bloquants

- Lancer Agent Manager sans diagnostic préalable
- Ignorer les ERROR checks
- Supposer que "ça marche" sans vérifier le PATH

## WAL NEXUS

Logger chaque diagnostic :

```
[AGENT_MANAGER_DIAG] check=env status=OK|WARN|ERROR detail=<message>
[AGENT_MANAGER_DIAG] check=kix status=OK|WARN|ERROR detail=<message>
[AGENT_MANAGER_DIAG] check=trix status=OK|WARN|ERROR detail=<message>
```

## Référence ADR

- **ADR** : ADR-2026-08-09-AGENT-MANAGER-DIAGNOSTICS
- **IntentHash** : 0xPRD_MOC_AGENT_MANAGER_DIAGNOSTICS_20260809
- **Statut ADR** : proposed
