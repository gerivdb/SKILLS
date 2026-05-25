---
name: devtools-core
description: "PowerShell modules, CI Gate, MCP, Fix-MCPConnection, cleanup. Use when user mentions 'DevTools', 'PowerShell', 'CI Gate', 'nettoyage'."
---
|
# DevTools Core

## Domaine et périmètre

Ce skill couvre la gestion du hub central **DevTools** (`C:\DevTools`) :
- Modules PowerShell (ECOS CLI, health checks, MCP)
- CI Gate (validation avant commit/push)
- MCP (Model Context Protocol) — configuration et dépannage
- Scripts de nettoyage et maintenance
- Fix-MCPConnection et Deploy-MCPFix

## Méthodologie

### Phase 1 : Diagnostic
- Vérifier l'état de DevTools : `ecos status`, `ecos health`.
- Contrôler la configuration MCP : `verify-mcp-access.ps1`.
- Lister les scripts disponibles dans `SCRIPTS/`, `bin/`, `monitoring/`.

### Phase 2 : Action
- Exécuter la commande ECOS appropriée (status, health, registry, sync).
- Corriger les problèmes MCP via `Fix-MCPConnection.ps1` si nécessaire.
- Nettoyer les fichiers temporaires et logs obsolètes.

### Phase 3 : Validation
- Vérifier que les modifications n'ont pas cassé les dépendances.
- Tester l'accès cross-repo (DevTools ↔ D:\DO\WEB).
- Documenter les changements dans le changelog DevTools.

## Règles de décision
- **Règle 1** : Ne JAMAIS faire `git add .` dans DevTools (450+ fichiers non trackés).
- **Règle 2** : Toujours `git add <fichier>` explicite dans DevTools.
- **Règle 3** : Ne pas modifier `Fix-MCPConnection.ps1` ni `Deploy-MCPFix.ps1`.

## Format de sortie

```markdown
## Statut DevTools
- ECOS CLI : [version]
- MCP Access : [OK | ERREUR]
- Repos actifs : [N]
- Dernier health-check : [date]
```

## Exemples d'utilisation
- "Vérifie l'état de DevTools" → `ecos status`.
- "Corrige l'accès MCP" → `verify-mcp-access.ps1 -Fix`.
- "Liste les repos du registre" → `ecos registry`.

## Intégration avec l'écosystème
- Dépôts concernés : DevTools (C:\DevTools), tous les repos D:\DO\WEB
- Couche EECS : L1_CAUSALITY
- Tags NEXUS : [CONFORME_NEXUS]
