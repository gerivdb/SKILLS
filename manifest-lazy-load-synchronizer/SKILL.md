---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_MLLS_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/manifest-lazy-load-synchronizer/SKILL.md
---

# Skill - manifest-lazy-load-synchronizer

## Objectif

Resout la derive d'index entre les 112 skills du MANIFEST.json et les 239 dossiers reels de L4-TOOLS/SKILLS. Synchronise le manifeste avec le filesystem et met en place le chargement paresseux (lazy-load) des skills.

## Declencheur

- Derive detectee entre MANIFEST.json et les dossiers SKILL.md sur disque.
- Chargement du systeme de skills au demarrage.
- Demande de synchronisation manuelle du registre des skills.

## Entrees

- Chemin vers MANIFEST.json.
- Chemin vers le dossier L4-TOOLS/SKILLS.
- Liste des dossiers contenant un SKILL.md.

## Sorties

- MANIFEST.json mis a jour avec toutes les skills manquantes.
- Rapport de synchronisation (ajoutes / supprimes / inchanges).
- Code retour 0 si synchronisation reussie, 1 si conflit non resolu.

## Regles Operationnelles

### 1. Scan du filesystem
Scanner recursivement tous les dossiers de L4-TOOLS/SKILLS contenant un fichier SKILL.md.

### 2. Comparaison avec MANIFEST.json
Comparer la liste des skills sur disque avec celles indexees dans MANIFEST.json.

### 3. Ajout des skills manquantes
Ajouter a MANIFEST.json toutes les skills presentes sur disque mais absentes du manifeste, avec leur frontmatter extrait du SKILL.md.

### 4. Suppression des entrees orphelines
Marquer comme orphelines les entrees de MANIFEST.json qui n'ont plus de dossier correspondant sur disque.

### 5. Mise a jour du compteur
Mettre a jour skillsCount dans MANIFEST.json pour refleter le nombre reel de skills.

### 6. Journalisation
Chaque ajout, suppression ou modification est consigne avec le nom de la skill et l'horodatage.
