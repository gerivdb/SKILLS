---
name: kilo-worktree-reconciler
description: Réconcilie uniquement les kilo worktrees d'Agent Manager avec .kilo/worktrees/ et .kilo/agent-manager.json, sans toucher aux git worktrees standards. Utilise ce skill quand tu dois nettoyer des références orphelines, vérifier la cohérence des sessions/worktrees, ou automatiser la réconciliation Agent Manager.
version: 1.0.0
intent_hash: 0xKILO_WORKTREE_RECONCILER_20260810
---

# Kilo Worktree Reconciler

## Objectif
Assurer la cohérence entre :
- `.kilo/worktrees/` (dossiers physiques des kilo worktrees)
- `.kilo/agent-manager.json` (worktrees + sessions + tabOrder + worktreeOrder)

Sans toucher aux git worktrees standards (`git worktree list`).

## Déclencheur
- Nettoyage après session Agent Manager
- Audit de `.kilo/agent-manager.json`
- Vérification avant création d'une nouvelle session
- Post-session cleanup automatique

## Prérequis
- PowerShell 7+
- Accès en écriture à `.kilo/agent-manager.json`
- Droit de lecture sur `.kilo/worktrees/`

## Protocole

### Étape 1 — Collecter l'état filesystem
```powershell
$fsKiloWorktrees = @{}
if (Test-Path '.kilo/worktrees') {
    Get-ChildItem -LiteralPath '.kilo/worktrees' -Directory | ForEach-Object {
        $fsKiloWorktrees[$_.Name] = $_.FullName
    }
}
```

### Étape 2 — Charger agent-manager.json
```powershell
$agentManager = Get-Content '.kilo/agent-manager.json' -Raw | ConvertFrom-Json
```

### Étape 3 — Détecter les worktrees orphelins
Pour chaque entrée dans `worktrees` :
- Vérifier que `path` existe toujours
- Si non → orphelin `missing-path`

### Étape 4 — Détecter les sessions orphelines
Pour chaque session :
- Si `worktreeId` est null → orphelin `no-worktree-id`
- Si `worktreeId` existe mais worktree manquant → orphelin `missing-worktree`

### Étape 5 — Nettoyer (avec confirmation)
Supprimer les entrées orphelines de :
- `worktrees`
- `sessions`
- `tabOrder` (garder les `pending:*`)
- `worktreeOrder`

## Format de sortie
Rapport Markdown dans `.kilo/reports/agent-manager-reconciliation-YYYY-MM-DD.md` :
- Orphaned Worktrees (JSON)
- Orphaned Sessions (JSON)
- Statistiques

## Anti-patterns bloquants
- Mélanger git worktrees et kilo worktrees
- Supprimer des entrées sans vérification préalable
- Perdre les clés JSON lors du filtrage
- Toucher à `.git/index.lock` sans diagnostic

## Référence ADR
- **ADR** : ADR-2026-08-10-001-KILO-WORKTREE-RECONCILER
- **IntentHash** : 0xKILO_WORKTREE_RECONCILER_20260810
- **Dépôt** : gerivdb/GeriCode
- **Statut ADR** : proposed
