---
name: ide-tools
description: "KiloCode, Cline, VSIX, MCP Sequential Thinking, Rust alternatives. Use when user mentions 'KiloCode', 'Cline', 'VSIX', 'MCP Sequential Thinking', 'Rust'."
version: "1.0.0"
changelog:
  - {v: "1.0.0", date: "2026-05-30", notes: "Version initiale"}
triggers: []
layer: "L0_UNKNOWN"
nexusTags: ["CONFORME_NEXUS"]---
|
# IDE Tools

## Domaine et périmètre

Ce skill couvre les **outils de développement IDE** dans l'écosystème gerivdb :
- KiloCode (agent IA VS Code, configuration, skills, agents)
- Cline (agent IA open-source, fork de Claude Code)
- VSIX (extensions VS Code, AI Orchestrator)
- MCP Sequential Thinking (raisonnement structuré)
- Alternatives Rust (pour le Z600, pas d'AVX)

## Méthodologie

### Phase 1 : Identification de l'outil
- Déterminer l'outil concerné (KiloCode, Cline, VSIX, MCP).
- Vérifier la version installée et la configuration actuelle.
- Identifier le besoin : installation, configuration, dépannage.

### Phase 2 : Action
- Pour KiloCode : vérifier `.kilo/`, `kilo.json`, skills, agents.
- Pour Cline : vérifier la configuration API, les permissions.
- Pour VSIX : installer/mettre à jour l'extension.
- Pour MCP Sequential Thinking : vérifier la config dans `mcp.json`.

### Phase 3 : Validation
- Tester l'outil sur un cas simple.
- Vérifier l'intégration avec l'écosystème (DevTools, repos).
- Documenter la configuration.

## Règles de décision
- **Règle 1** : KiloCode est l'agent principal — Cline est le fallback.
- **Règle 2** : Les MCP doivent être déclarés dans `mcp.json` avec les bons `allowedDirectories`.
- **Règle 3** : Sur Z600, privilégier les outils légers (pas de modèle Lourd en local).

## Format de sortie

```markdown
## Statut IDE Tools
- KiloCode : [version] [OK | ERREUR]
- Cline : [version] [OK | ERREUR]
- MCP Sequential Thinking : [actif | inactif]
- VSIX installées : [liste]
```

## Exemples d'utilisation
- "Vérifie la config KiloCode" → Lire `kilo.json`, `.kilo/`.
- "Installe le MCP Sequential Thinking" → Configurer `mcp.json`.
- "Cline ne fonctionne pas — diagnostique" → Vérifier API key, permissions.

## Intégration avec l'écosystème
- Dépôts concernés : vscode-lm-proxy, vsix-ai-orchestrator, CLINE, KiloCode
- Couche EECS : L4_ORCHESTRATION
- Tags NEXUS : [CONFORME_NEXUS]
