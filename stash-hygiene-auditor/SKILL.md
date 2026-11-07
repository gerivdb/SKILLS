---
name: stash-hygiene-auditor
description: Détecte et purge les stashes git temporaires ou anciens. Utilise ce skill quand tu dois auditer les stashes, supprimer les stashes temporaires, ou restaurer des stashs utiles.
version: 1.0.0
intent_hash: 0xSTASH_HYGIENE_AUDITOR_20260809
---

# Stash Hygiene Auditor

## Objectif
Maintenir la propreté des stashes git en détectant et purgeant les stashes temporaires, anciens ou obsolètes.

## Déclencheur
- Fin de session KiloCode
- Audit quotidien
- Avant tout changement de contexte important
- Après chaque merge ou rebase

## Prérequis
- Repo git valide
- Accès en écriture au repo

## Protocole

### Étape 1 — Lister tous les stashes
```powershell
git stash list
```

### Étape 2 — Inspecter chaque stash

Pour chaque stash :
1. Afficher le message : `git stash list`
2. Afficher le contenu : `git stash show -p stash@{n}`
3. Calculer l'âge du stash (date du commit associé)
4. Classifier le stash :
   - `temp` / `WIP` / `wrong branch` → temporaire
   - `before switch` / `before merge` → intermédiaire
   - `work in progress` / `feature/xxx` → utile

### Étape 3 — Calcul d'âge et décision

```powershell
$cutoff = (Get-Date).AddDays(-7)
git stash list --format="%gd %ci" | ForEach-Object {
  $parts = $_ -split ' '
  $stashId = $parts[0]
  $stashDate = [datetime]$parts[1]
  $age = (Get-Date) - $stashDate

  if ($age.TotalDays -gt 7) {
    Write-Host "Stash $stashDate is $([math]::Round($age.TotalDays, 1)) days old - dropping"
    git stash drop $stashId
  }
}
```

**Règles de décision** :

| Cas | Action |
|-----|--------|
| Stash temporaire (message contient "temp", "WIP", "wrong") | `git stash drop stash@{n}` |
| Stash intermédiaire (avant switch/merge) | `git stash drop stash@{n}` |
| Stash ancien (> 7 jours) | `git stash drop stash@{n}` |
| Stash avec contenu unique non commité | Demander confirmation avant drop |
| Stash utile (feature en cours) | Conserver |

### Étape 4 — Supprimer les stashes sélectionnés
```powershell
git stash drop stash@{n}
```

### Étape 5 — Vérification finale
```powershell
git stash list
```

## Règles de purge

1. **Age > 7 jours** → suppression automatique
2. **Message contient "temp" ou "WIP"** → suppression automatique
3. **Message contient "wrong branch"** → suppression automatique
4. **Message contient "before switch"** → suppression automatique après switch effectué
5. **Contenu déjà commité dans une branche** → suppression automatique
6. **Contenu unique non commité** → demande de confirmation HITL

## Sortie standard

```yaml
stashes_total: 18
stashes_dropped: []
stashes_kept: []
stashes_restored: []
recommendations: []
```

## Anti-patterns bloquants
- Drop un stash sans inspecter son contenu
- Drop un stash avec des modifications uniques non sauvegardées
- Conserver des stashes "temp" ou "WIP" pendant des semaines
- Utiliser `git stash clear` sans vérification individuelle

## Référence ADR
- **ADR** : ADR-2026-06-19-001-STASH_HYGIENE
- **IntentHash** : 0xSTASH_HYGIENE_AUDITOR_20260809
- **Dépôt** : gerivdb/GeriCode
- **Statut ADR** : proposed

## Références
- **IntentHash parent** : `0xPRD_MOC_GIT_HYGIENE_MECHANISMS_20260809`
- **IntentHash review fixes** : `0xPRD_MOC_GIT_HYGIENE_REVIEW_FIXES_20260809`
- **IntentHash incohérences** : `0xPRD_MOC_GIT_HYGIENE_INCOHERENCE_FIXES_20260809`
