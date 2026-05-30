---
name: base243
description: "Base-243 converter, Ladybird, ternary, Tauri, portage. Use when user mentions 'base 243', 'convertisseur', 'Ladybird', 'ternaire'."
version: "1.0.0"
changelog:
  - {v: "1.0.0", date: "2026-05-30", notes: "Version initiale"}
triggers: []
layer: "L0_UNKNOWN"
nexusTags: ["CONFORME_NEXUS"]
---
|
# Base 243

## Domaine et périmètre

Ce skill couvre la conversion et manipulation en **base 243** (ternaire équilibré, 3⁵ = 243 états) :
- Conversion base-243 ↔ décimal ↔ binaire
- Encodage/décodage de données en ternaire
- Intégration avec PLIX (substrat vidéo ternaire) et CODEC-243
- Portage et compatibilité (Ladybird, Tauri, Z600)

## Méthodologie

### Phase 1 : Identification du besoin
- Déterminer le sens de conversion (entrée → base-243 ou base-243 → sortie).
- Identifier le format source (binaire, décimal, hex, texte).
- Vérifier les contraintes matérielles (Z600 = CPU-only, pas d'AVX).

### Phase 2 : Conversion
- Appliquer l'algorithme de conversion base-243 (pentades de 5 trits).
- Gérer l'arrondi stochastique pour les valeurs non-exactes.
- Vérifier l'intégrité du résultat (round-trip test).

### Phase 3 : Livraison
- Fournir le résultat dans le format demandé.
- Documenter les pertes de précision éventuelles.
- Proposer des optimisations si pertinent (SIMD logiciel, lookup tables).

## Règles de décision
- **Règle 1** : Base-243 = ternaire équilibré (-1, 0, +1) — ne pas confondre avec du binaire.
- **Règle 2** : Pour PLIX, chaque pixel = 3 canaux × 5 trits = 15 trits par pixel.
- **Règle 3** : Sur Z600 sans AVX, privilégier les lookup tables précalculées.

## Format de sortie

```markdown
## Conversion Base-243
- Entrée : [valeur] (format : ...)
- Résultat : [valeur en base-243]
- Précision : [exacte | arrondi stochastique]
```

## Exemples d'utilisation
- "Convertis 256 en base-243" → Donner la représentation en pentades.
- "Encode ce texte en ternaire" → Fournir l'encodage.
- "Comment PLIX utilise le base-243 ?" → Expliquer les pentades vidéo.

## Intégration avec l'écosystème
- Dépôts concernés : PLIX, CODEC-243, VEC-243, GOV-243
- Couche EECS : L3_EMERGENCE
- Tags NEXUS : [CONFORME_NEXUS], [DÉRIVÉ]