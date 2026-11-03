---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_M3_IA_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/m3-intervault-auth/SKILL.md
---

# Skill - m3-intervault-auth

## Objectif

Authentification et autorisation inter-voutes dans le maillage des ~60 NotebookLM. Controle d'acces granulaire entre voutes du meme maillage pour empecher qu'une voute compromise n'accede aux donnees d'une autre sans droit. Primitive M3-Tree de securite inter-voutes.

## Declencheur

- Tentative d'acces d'une voute A aux chunks d'une voute B sans autorisation.
- Demande d'octroi ou de revocation de droits d'acces inter-voutes.
- Verification des permissions avant replication d'un chunk entre voutes.
- Audit des acces inter-voutes pour conformite securite.

## Entrees

- Voute source (demandeur d'acces).
- Voute cible (detentrice des donnees).
- Chunk ou ensemble de chunks demandes.
- Type d'acces demande (lecture / ecriture / replication).
- Jeton d'authentification ou certificat de la voute source.

## Sorties

- Autorisation ou refus d'acces (accorde / refuse).
- Rapport d'audit (voute source, voute cible, chunks, decision, horodatage).
- Code retour 0 si acces autorise, 1 si acces refuse, 2 si authentification echouee.

## Regles Operationnelles

### 1. Authentification mutuelle
Toute demande d'acces inter-voutes doit etre authentifiee des deux cotes (voute source et voute cible).

### 2. Controle d'acces granulaire
Les permissions sont definies par paire de voutes et par type d'acces (lecture, ecriture, replication). Une voute ne peut pas acceder aux donnees d'une autre sans droit explicite.

### 3. Propagation conditionnelle
La replication d'un chunk vers une voute cible est conditionnee a l'autorisation d'ecriture de cette voute sur le chunk source.

### 4. Revocation immediate
Toute revocation de droits prend effet immediatement sur toutes les voutes du maillage.

### 5. Journalisation d'audit
Chaque demande d'acces inter-voutes est consignee avec la source, la cible, les chunks, la decision et l'horodatage pour tracabilite de securite.
