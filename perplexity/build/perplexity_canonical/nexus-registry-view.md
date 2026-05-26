---
name: nexus-registry-view
description: "Dashboard, herd view, registry status. Use when user mentions 'dashboard troupeau', 'vue registre', 'tableau de bord'."
---
|

# nexus-registry-view
|
# NEXUS Registry View

## Domaine et périmètre

Ce skill couvre la **visualisation du registre** ECOS_ROOT :
- Dashboard de l'écosystème (vue d'ensemble de tous les dépôts)
- Herd view (vue par groupe : L1-Gouvernance, L3-Citoyen, L4-DevTools)
- Statut de chaque dépôt (actif, inactif, manquant, non conforme)
- Métriques agrégées (φ-CPS moyen, CI status, couverture docs)

## Méthodologie

### Phase 1 : Collecte
- Lire ECOS_ROOT.json.
- Pour chaque dépôt : récupérer le statut CI, la date de dernier commit, le φ-CPS.
- Agréger par couche EECS (L1 à L5).

### Phase 2 : Construction du dashboard
- Générer un tableau Markdown par couche.
- Calculer les métriques agrégées.
- Identifier les anomalies (CI rouge, φ-CPS bas, dépôts inactifs).

### Phase 3 : Présentation
- Formater le dashboard en Markdown.
- Proposer des filtres (par couche, par statut, par métrique).
- Exporter si nécessaire (CSV, JSON).

## Règles de décision
- **Règle 1** : Le dashboard doit être lisible dans un chat (pas de tableau trop large).
- **Règle 2** : Les dépôts critiques (φ-CPS < 4.0) sont surlignés.
- **Règle 3** : La herd view regroupe par couche EECS, pas par ordre alphabétique.

## Format de sortie

```markdown
## Dashboard Écosystème

### L1-Gouvernance (4 dépôts)
| Dépôt | Statut | φ-CPS | CI |
|-------|--------|-------|-----|
| ECOYSTEM | ✅ | 4.82 | 🟢 |
| BRAIN | ✅ | 4.71 | 🟢 |

### Résumé
- Total : [N] dépôts
- Actifs : [N]
- φ-CPS moyen : [X.XXX]
- Alertes : [N]
```

## Exemples d'utilisation
- "Affiche le dashboard de l'écosystème" → Vue complète.
- "Montre-moi la herd view L3-Citoyen" → Filtrer par couche.
- "Quels dépôts sont en alerte ?" → Lister les critiques.

## Intégration avec l'écosystème
- Dépôts concernés : NEXUS, ECOS_ROOT
- Couche EECS : L1_CAUSALITY
- Tags NEXUS : [CONFORME_NEXUS]

