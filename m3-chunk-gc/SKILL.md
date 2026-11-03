---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_M3_CGC_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/m3-chunk-gc/SKILL.md
---

# Skill - m3-chunk-gc

## Objectif

Nettoyage des chunks orphelins ou dupliques apres elagage ou migration dans le maillage des ~60 voutes NotebookLM. Empeche l'accumulation de chunks morts qui consomment de l'espace et complexifient les requetes. Primitive M3-Tree de garbage collection des chunks.

## Declencheur

- Detection de chunks orphelins (sans voute proprietaire identifiable).
- Detection de chunks dupliques sur plusieurs voutes sans raison de replication.
- Demande de nettoyage apres une operation d'elagage (epsilon-pruning).
- Nettoyage periodique des chunks morts.

## Entrees

- Liste des chunks candidats au nettoyage.
- Seuil d'inactivite (nombre de jours sans acces avant consideration comme mort).
- Facteur de replication minimal (ne pas supprimer si en dessous).
- Liste des voutes a scanner.

## Sorties

- Rapport de nettoyage (chunks supprimes, espace libere, voutes concernees).
- Code retour 0 si nettoyage reussi, 1 si aucun chunk a nettoyer, 2 si echec partiel.

## Regles Operationnelles

### 1. Detection de chunks orphelins
Identifier les chunks qui n'ont plus de voute proprietaire dans le maillage M3-Tree.

### 2. Detection de duplications excessives
Identifier les chunks dupliques au-dela du facteur de replication configure.

### 3. Verification avant suppression
Ne jamais supprimer un chunk si cela ferait tomber le nombre de copies en dessous du facteur de replication minimal.

### 4. Nettoyage par batch
Traiter les chunks par batch pour eviter de surcharger le systeme pendant le nettoyage.

### 5. Journalisation
Chaque suppression de chunk est consignee avec le chunk ID, les voutes concernees, l'espace libere et l'horodatage.
