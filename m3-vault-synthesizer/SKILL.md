---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_M3_VS_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/m3-vault-synthesizer/SKILL.md
---

# Skill - m3-vault-synthesizer

## Objectif

Automatiser l'aggregation continue des ~60 voutes NotebookLM pour alimenter dynamiquement le contexte des agents sans saturer les limites de tokens. Extension naturelle du Zot Compressor. Primitive M3-Tree de synthese inter-vault en temps reel.

## Declencheur

- Nouvelle source documentaire ajoutee dans une vault NotebookLM.
- Demande de synthese transversale sur plusieurs vaults simultanement.
- Saturation proche de la limite de tokens du contexte agent.
- Mise a jour d'un document source dans une voute referencee.

## Entrees

- Liste des IDs de vaults NotebookLM a aggreger.
- Requete de synthese (sujet, mots-cles, profondeur de recherche).
- Budget de tokens disponible pour le contexte resultant.
- Filtre de pertinence (score minimum de similarite semantique).

## Sorties

- Synthese agrigee des vaults cibles (texte compresse, citations incluses).
- Rapport de consommation de tokens (avant / apres compression).
- Code retour 0 si synthese reussie, 1 si aucune source pertinente, 2 si budget tokens insuffisant.

## Regles Operationnelles

### 1. Agregation transversale
Interroger plusieurs vaults NotebookLM en parallel et fusionner les resultats en une seule synthese coherent.

### 2. Compression contextuelle
Appliquer le Zot Compressor pour reduire la taille du texte synthese tout en preservant les informations critiques.

### 3. Respect du budget de tokens
Si le budget de tokens est atteint avant la fin de la synthese, arreter et retourner le resultat partiel avec un avertissement.

### 4. Filtrage par pertinence
Exclure les sources dont le score de similarite semantique est inferieur au seuil configure.

### 5. Journalisation
Chaque operation de synthese est consignee avec les vaults sollicitees, le nombre de tokens consommes et l'horodatage.
