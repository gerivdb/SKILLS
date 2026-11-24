# SUBMODULE-POLICY — Politique de gestion des sous-modules

## Contexte

Ce repo contient des sous-modules git. Certains appartiennent à l'écosystème gerivdb, d'autres sont des upstreams tiers importés.

## Règle d'or (déclarée dans .gitmodules)

> Submodules are READ-ONLY
> Do not modify submodule content directly
> Use 'git submodule update --remote --merge' to sync
> All submodule changes must be tracked via ASSIMILATION.md

## Sous-modules de ce repo

| Chemin | Remote | Classification | Statut | Action |
|--------|--------|----------------|--------|--------|
| ext/marketingskills | https://github.com/coreyhaines31/marketingskills.git | tierce | propre | Suivre .gitmodules (READ-ONLY) |
| mcp-google-appscript | https://github.com/mohalmah/google-appscript-mcp-server.git | tierce | propre | Suivre .gitmodules (READ-ONLY) |

## Procédure en cas de sous-module tierce dirty

1. **Sauvegarder** les modifications locales dans `.kilo/patches/`
2. **Réinitialiser** le sous-module vers l'état officiel de l'upstream
3. **Committer** le nouveau pointeur dans le parent
4. **Documenter** la décision dans ce fichier et dans ASSIMILATION.md

## Antipatterns interdits

- Modifier un sous-module tierce et committer dans le parent
- Pousser un sous-module tierce sans accès en écriture
- Laisser un sous-module dirty sans documentation
- Contourner la règle READ-ONLY déclarée dans .gitmodules
