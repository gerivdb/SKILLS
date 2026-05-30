---
name: prd-factory
version: "1.0.0"
description: "Compétence pour la production complète d’un PRD : validation croisée des spécifications, vérification de la cohérence OKR, guide de rédaction selon le format canonique (sections 1→17, OKRs, ADRs, etc.). Utiliser quand l’utilisateur mentionne 'PRD production', 'spec cross‑validator', 'OKR consistency', 'PRD canonique'."
triggers: ["PRD production", "spec cross-validator", "OKR consistency", "PRD canonique", "PRD factory"]
layer: "L2_PRODUCTION"
nexusTags: ["PRD_FACTORY"]
prerequisites: []
slotWeight: 1
status: active
changelog:
  - {v: "1.0.0", date: "2026-05-30", notes: "Version initiale"}
---
# PRD Factory

## Domaine et périmètre

Cette compétence guide l’élaboration d’un PRD (Product Requirement Document) conforme aux standards de l’écosystème :

- **Spec‑cross‑validator** : vérifie que toutes les exigences fonctionnelles et non‑fonctionnelles sont couvertes, sans contradictions, et que les références aux autres PRD/EPICs sont correctes.
- **OKR‑consistency‑checker** : s’assure que les objectifs et résultats clés associés au PRD sont alignés avec les OKR du trimestre et de l’année.
- **Guide de rédaction PRD canonique** : fournit le modèle détaillé (sections 1 à 17, incluant vision, objectifs, périmètre, livrables, planning, risques, métriques, annexes, etc.) et les bonnes pratiques de rédaction.

## Méthodologie

### Phase 1 : Collecte des entrées
- Rassembler les besoins métiers, les histoires d’utilisateur, les contraintes techniques et les dépendances externes.
- Récupérer les OKR en cours (département, équipe, produit) depuis le référentiel OKR.
- Obtenir la liste des PRD/EPICs liés (via le registre de dépendances).

### Phase 2 : Validation croisée des spécifications
- Exiger que chaque exigence soit associée à un identifiant unique (ex. : `REQ-001`).
- Vérifier l’absence de duplication fonctionnelle et détecter les exigences conflictuelles (ex. : performances vs latence).
- S’assurer que les références croisées pointent vers des documents existants et à jour (utiliser le `spec‑cross‑validator` interne).

### Phase 3 : Vérification de la cohérence OKR
- Mapper chaque objectif du PRD à un ou plusieurs OKR.
- Calculer le pourcentage de couverture : (objectifs couverts / objectifs totaux) × 100.
- Lever un avertissement si la couverture est < 80 % ou si des OKR majeurs sont omis.

### Phase 4 : Rédaction selon le modèle canonique
- Utiliser le template PRD (sections 1‑17) fourni dans le dépôt `ecosystem/templates/PRD_TEMPLATE.md`.
- Remplir chaque section avec les informations recueillies.
- Ajouter les annexes : maquettes, diagrammes d’architecture, matrices de traçabilité.
- Effectuer une revue orthographique et de style (guide de rédaction interne).

### Phase 5 : Validation finale et signature
- Faire circuler le PRD auprès des parties prenantes (produit, ingénierie, juridique, sécurité) pour recueillir les avis.
- Incorporer les retours et itérer jusqu’à obtention du consensus.
- Générer le PDF final et le déposer dans le référentiel de documentation (`docs/prds/`).
- Enregistrer les métadonnées (version, auteur, date) dans le registre des PRD.

## Règles de décision

- **Règle 1** : Toute exigence fonctionnelle doit être traçable à une histoire d’utilisateur ou à un cas d’utilisation.
- **Règle 2** : Les OKR associés doivent être quantifiables (ex. : augmenter le taux de conversion de 2 %).
- **Règle 3** : Le PRD ne doit pas dépasser 25 pages (hors annexes) afin de rester lisible.
- **Règle 4** : Les sections « Risques » et « Métriques de succès » sont obligatoires.

## Format de sortie

```markdown
## PRD Factory – État
- Spécifications validées : [oui/non]
- Cohérence OKR : [pourcentage]%
- Modèle utilisé : PRD_TEMPLATE_v[version]
- Dernière revue : [date]
- Statut : [DRAFT | REVIEW | APPROVED]
```

## Exemples d’utilisation

- "Générer un PRD pour la nouvelle fonctionnalité de recherche sémantique" → Lancer la PRD Factory avec les besoins recueillis.
- "Vérifier la cohérence des OKR liés au PRD du module paiement" → Utiliser l’OKR‑consistency‑checker.
- "Obtenir le modèle de PRD canonique" → Retourner le contenu du template `PRD_TEMPLATE.md`.

## Intégration avec l’écosystème

- Dépôts concernés : tous les produits qui nécessitent un PRD (ex. : `flux`, `brain`, `candidator`, `geribooking`).
- Couche EECS : L2_PRODUCTION
- Tags NEXUS : [PRD_FACTORY], [SPEC_CROSS_VALIDATOR], [OKR_CHECKER]
