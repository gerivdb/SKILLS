---
name: argus-tracker
description: "ARGUS project phases, delta registry, propagation, KIVA scheduler. Use when user mentions 'ARGUS', 'delta registry', 'propagation', 'Phase 4'."
version: "1.0.0"
changelog:
  - {v: "1.0.0", date: "2026-05-30", notes: "Version initiale"}
triggers: []
layer: "L0_UNKNOWN"
nexusTags: ["CONFORME_NEXUS"]
trit_primitive: TritObserve
---
# Argus Tracker

## Domaine et périmètre

ARGUS est le moteur de propagation de changements dans l'écosystème gerivdb. Ce skill couvre :
- Le suivi des phases projet (Phase 1 à Phase 4)
- Le registre des deltas (changements détectés entre états)
- La propagation contrôlée des modifications inter-dépôts
- L'ordonnancement via KIVA scheduler

## Méthodologie

### Phase 1 : Diagnostic de phase
- Déterminer la phase actuelle du projet ARGUS.
- Lister les deltas en attente dans le registre.
- Vérifier l'état du scheduler KIVA (tâches planifiées, runs en cours).

### Phase 2 : Analyse des deltas
- Calculer l'impact de chaque delta (dépendants, conflits, ordre).
- Vérifier la cohérence du registre avec ECOS_ROOT.
- Identifier les blocages (dépendances circulaires, prérequis manquants).

### Phase 3 : Propagation
- Ordonnancer les deltas via KIVA scheduler.
- Exécuter la propagation phase par phase (dry-run puis réel).
- Valider chaque étape avant de passer à la suivante.

## Règles de décision
- **Règle 1** : Jamais de propagation sans dry-run préalable.
- **Règle 2** : Les deltas P0 (constitutionnels) nécessitent une validation φ-CPS avant propagation.
- **Règle 3** : Un delta qui échoue 3 fois est marqué BLOCKED et notifie.

## Format de sortie

```markdown
## Statut ARGUS
- Phase actuelle : Phase [N]
- Deltas en attente : [N]
- Deltas propagés : [N]
- Blocages : [liste]
```

## Exemples d'utilisation
- "Quelle est la phase actuelle d'ARGUS ?" → Afficher le statut.
- "Propage le delta #42 vers DevTools" → Ordonnancer et exécuter.
- "Liste les deltas bloqués" → Scanner le registre.

## Intégration avec l'écosystème
- Dépôts concernés : KIVA-CLI, NEXUS, ECOS_ROOT
- Couche EECS : L2_COMPOSITION
- Tags NEXUS : [CONFORME_NEXUS], [BLOQUÉ]