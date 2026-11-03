---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_M3_SV_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/m3-snapshot-versioning/SKILL.md
---

# Skill - m3-snapshot-versioning

## Objectif

Versioning des snapshots de voutes dans le maillage des ~60 NotebookLM. Permet de revenir en arriere sur un etat precedent d'une voute en cas de corruption ou de modification erronee. Primitive M3-Tree de versioning des snapshots.

## Declencheur

- Demande de creation d'un snapshot d'une voute avant modification majeure.
- Detection de corruption d'une voute necessitant un retour a un etat anterieur.
- Listage des snapshots disponibles pour une voute donnee.
- Restauration d'une voute a un snapshot specifique.

## Entrees

- Identifiant de la voute (vault_index i dans [1, 60]).
- Nom ou identifiant du snapshot cible (pour restauration).
- Corbeille de retention (nombre de snapshots a conserver par voute).
- Horodatage du snapshot souhaite.

## Sorties

- Snapshot cree (identifiant, horodatage, taille).
- Voute restauree a l'etat du snapshot (confirmation).
- Liste des snapshots disponibles pour une voute.
- Code retour 0 si operation reussie, 1 si snapshot non trouve, 2 si echec d'operation.

## Regles Operationnelles

### 1. Creation de snapshot avant modification
Avant toute modification majeure d'une voute, creer automatiquement un snapshot pour permettre un retour en arriere.

### 2. Retention limitee
Conserver uniquement les N derniers snapshots par voute (configurable, par defaut : 10) pour eviter l'accumulation infinie.

### 3. Restauration ciblee
Permettre la restauration d'une voute entiere ou d'un chunk specifique a partir d'un snapshot.

### 4. Verification d'integrite
Verifier l'integrite du snapshot avant toute restauration (comparaison d'empreinte).

### 5. Journalisation
Chaque creation, restauration ou suppression de snapshot est consignee avec la voute, l'identifiant du snapshot et l'horodatage.
