---
name: nexus-registry-sync
description: "ECOS_ROOT synchronization, autodiscover, missing repositories. Use when user mentions 'ECOS_ROOT sync', 'registre', 'autodiscover', 'dépôts manquants'."
version: "1.0.0"
changelog:
  - {v: "1.0.0", date: "2026-05-30", notes: "Version initiale"}
triggers: []
layer: "L0_UNKNOWN"
nexusTags: ["CONFORME_NEXUS"]
---
|
# NEXUS Registry Sync

## Domaine et périmètre

Ce skill couvre la **synchronisation du registre ECOS_ROOT** :
- ECOS_ROOT.json (registre central des dépôts gerivdb)
- Autodiscovery (détection automatique de nouveaux dépôts sur GitHub)
- Détection des dépôts manquants (dans le registre mais pas sur disque, ou inversement)
- Synchronisation bidirectionnelle (registre ↔ remotes ↔ locaux)

## Méthodologie

### Phase 1 : Scan
- Lire ECOS_ROOT.json et lister les dépôts enregistrés.
- Scanner les remotes GitHub (API) pour détecter les nouveaux dépôts.
- Comparer avec les clones locaux (D:\DO\WEB).

### Phase 2 : Analyse des écarts
- Dépôts dans le registre mais pas sur GitHub → marquer [HORS_NEXUS].
- Dépôts sur GitHub mais pas dans le registre → proposer l'ajout.
- Dépôts locaux mais pas dans le registre → autodiscover.

### Phase 3 : Synchronisation
- Mettre à jour ECOS_ROOT.json avec les ajouts/suppressions.
- Cloner les dépôts manquants localement.
- Documenter les changements dans le changelog.

## Règles de décision
- **Règle 1** : ECOS_ROOT.json est la source de vérité — toujours le mettre à jour en dernier.
- **Règle 2** : Un dépôt inactif depuis 90 jours est marqué [INACTIF] (pas supprimé).
- **Règle 3** : L'autodiscover ne s'applique qu'aux dépôts `gerivdb/*`.

## Format de sortie

```markdown
## Rapport Sync
- Dépôts dans le registre : [N]
- Nouveaux dépôts détectés : [N]
- Dépôts manquants : [N]
- Dépôts inactifs : [N]
- ECOS_ROOT mis à jour : [oui | non]
```

## Exemples d'utilisation
- "Synchronise ECOS_ROOT avec GitHub" → Scan complet + update.
- "Détecte les dépôts manquants" → Comparer registre vs local.
- "Ajoute le dépôt X au registre" → Autodiscover + ajout.

## Intégration avec l'écosystème
- Dépôts concernés : NEXUS, ECOS_ROOT, DevTools
- Couche EECS : L1_CAUSALITY
- Tags NEXUS : [CONFORME_NEXUS], [INACTIF], [HORS_NEXUS]
