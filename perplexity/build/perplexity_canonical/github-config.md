---
name: github-config
description: "GITHUB_TOKEN, gh auth, scopes, Actions settings, rate-limit. Use when user mentions 'GITHUB_TOKEN', 'gh auth', 'scopes', 'Settings Actions'."
---
|

# github-config
|
# GitHub Config

## Domaine et périmètre

Ce skill couvre la **configuration GitHub** pour l'écosystème gerivdb :
- GITHUB_TOKEN (création, rotation, scopes)
- Authentification `gh auth` (login, logout, status)
- Scopes et permissions (repo, workflow, admin:org)
- Settings Actions (permissions au niveau dépôt/organisation)
- Rate-limits GitHub API (monitoring, contournement)

## Méthodologie

### Phase 1 : Diagnostic
- Vérifier l'état de l'auth : `gh auth status`.
- Contrôler les scopes du token actuel : `gh auth token`.
- Vérifier les rate-limits : `gh api /rate_limit`.

### Phase 2 : Configuration
- Configurer le GITHUB_TOKEN avec les scopes requis.
- Ajuster les Settings Actions (permissions GITHUB_TOKEN).
- Configurer les webhooks et secrets CI si nécessaire.

### Phase 3 : Validation
- Tester l'accès aux dépôts cibles.
- Vérifier que les workflows Actions se déclenchent correctement.
- Documenter la configuration (token expiry, scopes).

## Règles de décision
- **Règle 1** : Le GITHUB_TOKEN doit avoir au minimum les scopes `repo` et `workflow`.
- **Règle 2** : Les tokens expirent après 90 jours — planifier la rotation.
- **Règle 3** : Les rate-limits sont de 5000 requêtes/heure (auth) ou 60 (non-auth).

## Format de sortie

```markdown
## Config GitHub
- Auth : [OK | ERREUR]
- Scopes : [liste]
- Rate-limit : [N]/5000 restantes
- Token expiry : [date]
```

## Exemples d'utilisation
- "Vérifie l'état de gh auth" → `gh auth status`.
- "Les workflows IRIS échouent — vérifie les permissions" → Inspecter Settings Actions.
- "Quel est mon rate-limit restant ?" → `gh api /rate_limit`.

## Intégration avec l'écosystème
- Dépôts concernés : tous les repos gerivdb
- Couche EECS : L1_CAUSALITY
- Tags NEXUS : [CONFORME_NEXUS]

