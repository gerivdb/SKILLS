---
name: session-snapshot
version: "1.0.0"
description: "Capture structurée d'une session de travail : commits produits, fichiers créés/modifiés, métriques finales, phases bloquantes et dépendances. Utiliser en fin de session pour produire un bilan vérifiable. Utiliser quand l'utilisateur demande 'résumé session', 'snapshot', 'bilan', 'clôturer session', 'vérifier que tout est terminé'."
triggers:
  - "résumé session"
  - "snapshot"
  - "bilan"
  - "clôturer session"
  - "vérifier que tout est terminé"
  - "session complète"
  - "état des lieux"
layer: "L4_ORCHESTRATION"
nexusTags: ["CONFORME_NEXUS", "SESSION_MANAGEMENT"]
prerequisites:
  - "git log accessible sur les repos concernés"
  - "Accès aux fichiers créés/modifiés durant la session"
slotWeight: 1
status: "active"
changelog:
  - {v: "1.0.0", date: "2026-06-07", notes: "Version initiale — capture structurée de session"}
---

# SESSION-SNAPSHOT — Capture structurée de session

## Domaine et périmètre

Ce skill produit un **snapshot vérifiable** d'une session de travail. Il capture les commits, fichiers, métriques, et l'état des phases pour permettre une clôture propre et un audit ultérieur.

## Méthodologie

### Phase 1 — Collecte des commits

Pour chaque repo concerné :
```bash
git -C "<repo_path>" log --oneline -10
git -C "<repo_path>" show --stat <commit_hash>
```

Extraire pour chaque commit :
- Hash court
- Message de commit
- Nombre de fichiers créés/modifiés
- Lignes insérées/supprimées

### Phase 2 — Vérification des fichiers

Pour chaque fichier mentionné dans les commits :
```bash
Test-Path "<file_path>"
```

Vérifier l'existence réelle sur le filesystem.

### Phase 3 — Métriques

Calculer :
- **Total commits** : somme sur tous les repos
- **Total fichiers** : somme des fichiers créés/modifiés
- **Total lignes** : somme des insertions
- **Slots utilisés** : depuis MANIFEST.json (`skillsCount`)
- **Phases en attente** : liste des dépendances non résolues

### Phase 4 — Rapport de snapshot

Produire un rapport structuré :

```markdown
## Session Snapshot — [DATE]

### Commits produits (N commits, M repos)

| Commit | Repo | Contenu | Fichiers | Lignes |
|--------|------|---------|----------|--------|
| `hash` | REPO | description | N | ±N |

### Métriques
- **Total commits** : N
- **Total fichiers** : N
- **Total lignes** : ~N
- **Slots SKILLS** : N/100
- **Agents** : N
- **Working trees** : propres/dirty

### Phases en attente
| Phase | Dépendance | Statut |
|-------|------------|--------|
| ... | ... | ⏳ |

### Vérification croisée
- [ ] Chaque commit listé existe sur le remote
- [ ] Chaque fichier mentionné existe sur le filesystem
- [ ] Les 3 repos sont sur la bonne branche (main)
- [ ] Les working trees sont propres
```

## Règles de décision

- **Règle 1** : Toujours vérifier les commits sur le remote (pas juste local)
- **Règle 2** : Toujours vérifier l'existence réelle des fichiers (pas juste les commits)
- **Règle 3** : Toujours vérifier l'état des working trees
- **Règle 4** : Si un commit est listé mais pas sur le remote → signaler comme NON VÉRIFIÉ
- **Règle 5** : Si un fichier est mentionné mais n'existe pas → signaler comme MANQUANT

## Format de sortie

Le snapshot doit être **vérifiable** : chaque élément doit être confirmable par une commande git ou filesystem.

## Intégration avec l'écosystème

- **Dépôts concernés** : Tous les repos modifiés durant la session
- **Couche EECS** : L4_ORCHESTRATION
- **Skills dépendants** : Aucun (skill terminal)
- **Tags NEXUS** : [CONFORME_NEXUS], [SESSION_MANAGEMENT]
