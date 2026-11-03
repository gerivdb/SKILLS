---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_M3_RS_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/m3-replica-sync/SKILL.md
---

# Skill - m3-replica-sync

## Objectif

Assurer la replication physique des chunks de donnees entre les ~60 voutes NotebookLM du maillage M3-Tree. Garantit qu'une copie physique de chaque chunk critique existe sur au moins deux voutes distinctes pour eviter toute perte de donnee en cas d'indisponibilite d'un noeud. Primitive M3-Tree de replication distribuee.

## Declencheur

- Nouveau chunk critique ajoute a une voute source sans copie de replication.
- Detection d'un chunk existant sur une seule voute (facteur de replication < 2).
- Demande de synchronisation forcee d'un chunk vers ses voutes cibles.
- Maintenance periodique de la redondance physique.

## Entrees

- Identifiant du chunk a repliquer.
- Voute source (detentrice du chunk original).
- Liste des voutes cibles (replicats).
- Facteur de replication minimum (par defaut : 2 copies).

## Sorties

- Confirmation de replication reussie (chunk copie sur toutes les voutes cibles).
- Rapport de copie (taille transferee, temps de copie, voutes cibles atteintes).
- Code retour 0 si replication reussie, 1 si echec partiel, 2 si echec total.

## Regles Operationnelles

### 1. Replication physique obligatoire
Chaque chunk critique doit exister physiquement sur au moins deux voutes distinctes du maillage M3-Tree.

### 2. Verification de l integrite post-copie
Apres chaque copie, verifier que le chunk replique est identique a l'original (comparaison d'empreinte SHA256).

### 3. Respect du facteur de replication
Ne pas considerer une replication comme reussie si le nombre de copies actives est inferieur au facteur configure.

### 4. Gestion des conflits de copie
Si un chunk existe deja sur une voute cible avec un contenu different, ne pas ecraser sans signalement HITL.

### 5. Journalisation
Chaque operation de replication est consignee avec le chunk ID, les voutes source/cibles, la taille et l'horodatage.
