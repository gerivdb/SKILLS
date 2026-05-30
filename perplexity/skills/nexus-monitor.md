---
name: nexus-monitor
description: "φ-CPS scoring, ecosystem health, production readiness, drift detection. Use when user mentions 'φ-CPS', 'santé écosystème', 'production readiness', 'drift'."
version: "1.0.0"
changelog:
  - {v: "1.0.0", date: "2026-05-30", notes: "Version initiale"}
triggers: []
layer: "L0_UNKNOWN"
nexusTags: ["CONFORME_NEXUS"]---
|
# NEXUS Monitor

## Domaine et périmètre

Ce skill couvre le **monitoring de l'écosystème** gerivdb :
- Scoring φ-CPS (conformité constitutionnelle des dépôts et fichiers)
- Santé de l'écosystème (repos actifs, CI status, dépendances)
- Production readiness (prêt pour la production ?)
- Drift detection (dérive par rapport aux standards)

## Méthodologie

### Phase 1 : Collecte des métriques
- Scanner tous les dépôts du registre ECOS_ROOT.
- Récupérer le statut CI de chaque dépôt.
- Calculer le score φ-CPS pour chaque dépôt (formule : cohérence × autonomie × conformité).

### Phase 2 : Analyse
- Identifier les dépôts en dessous du seuil φ-CPS (4.559).
- Détecter la dérive structurelle (fichiers hors place, standards non respectés).
- Évaluer la production readiness (CI vert, tests passants, docs à jour).

### Phase 3 : Rapport et alertes
- Générer le dashboard de santé.
- Alerter sur les dépôts critiques (φ-CPS < 4.0).
- Proposer des actions correctives.

## Règles de décision
- **Règle 1** : φ-CPS ≥ 4.559 = conforme constitutionnel.
- **Règle 2** : Un dépôt avec CI rouge depuis > 7 jours = alerte.
- **Règle 3** : La dérive structurelle détectée doit être corrigée sous 48h.

## Format de sortie

```markdown
## Dashboard NEXUS
- Dépôts actifs : [N]
- φ-CPS moyen : [X.XXX]
- Dépôts critiques : [N]
- CI vert : [N]/[N]
- Drift détecté : [N] dépôts
```

## Exemples d'utilisation
- "Quel est l'état de santé de l'écosystème ?" → Dashboard complet.
- "Quel dépôt a le φ-CPS le plus bas ?" → Lister et classer.
- "Détecte la dérive dans FLUENCE" → Audit structurel.

## Intégration avec l'écosystème
- Dépôts concernés : NEXUS, tous les dépôts gerivdb
- Couche EECS : L1_CAUSALITY
- Tags NEXUS : [CONFORME_NEXUS], [À_VALIDER_NEXUS]
