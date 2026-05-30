---
name: local-recovery
description: "Disappeared local clones, WAZAA, git detective, restoration. Use when user mentions 'clone disparu', 'WAZAA', 'restauration', 'ecos repo'."
version: "1.0.0"
changelog:
  - {v: "1.0.0", date: "2026-05-30", notes: "Version initiale"}
triggers: []
layer: "L0_UNKNOWN"
nexusTags: ["CONFORME_NEXUS"]
---
|
# Local Recovery

## Domaine et périmètre

Ce skill couvre la **restauration de clones locaux disparus** dans l'écosystème gerivdb :
- Détection des clones manquants (comparaison registre vs disque)
- WAZAA (outil de détection et restauration Git)
- Git detective (analyse des traces : reflog, stash, branches orphelines)
- Restauration des dépôts depuis les remotes GitHub

## Méthodologie

### Phase 1 : Détection
- Comparer le registre ECOS_ROOT avec les clones locaux existants.
- Lister les dépôts manquants (présents dans le registre mais pas sur disque).
- Vérifier les traces locales (reflog, stash, `.git/objects`).

### Phase 2 : Investigation
- Utiliser WAZAA pour scanner les traces de clones supprimés.
- Analyser l'historique Git local (reflog, logs) pour retrouver les SHA.
- Vérifier si des données récupérables existent (stash, branches cachées).

### Phase 3 : Restauration
- Cloner depuis le remote GitHub si le dépôt existe toujours.
- Restaurer le stash local si disponible (`git stash pop`).
- Réaligner avec ECOS_ROOT et vérifier la conformité.

## Règles de décision
- **Règle 1** : Toujours vérifier le remote avant de déclarer un dépôt perdu.
- **Règle 2** : WAZAA est le premier outil à utiliser pour la détection.
- **Règle 3** : Si le dépôt n'existe plus sur GitHub non plus → marquer [HORS_NEXUS].

## Format de sortie

```markdown
## Rapport Recovery
- Dépôts manquants : [N]
- Récupérés depuis remote : [N]
- Récupérés depuis stash local : [N]
- Définitivement perdus : [N]
```

## Exemples d'utilisation
- "Le clone de FLUENCE a disparu — restaure-le" → Cloner depuis remote.
- "Scanne les traces de clones supprimés" → Lancer WAZAA.
- "Quels dépôts du registre ne sont plus sur disque ?" → Comparer.

## Intégration avec l'écosystème
- Dépôts concernés : WAZAA, tous les repos locaux
- Couche EECS : L1_CAUSALITY
- Tags NEXUS : [CONFORME_NEXUS], [HORS_NEXUS]
