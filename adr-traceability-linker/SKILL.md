---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_ATL_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/adr-traceability-linker/SKILL.md
---

# Skill - adr-traceability-linker

## Objectif

Lier automatiquement une modification de code a son Intent (.geri/INTENTS/) et a son Architecture Decision Record (.geri/ADR/). Garantit la traceabilite complete entre le code, l'intent et la decision architecturale.

## Declencheur

- Modification de code dans un depot GeriCode.
- Creation d'un Intent dans .geri/INTENTS/.
- Creation d'un ADR dans .geri/ADR/.
- Verification de coherence traceability avant commit.

## Entrees

- Chemin vers le fichier de code modifie.
- Chemin vers le dossier .geri/INTENTS/.
- Chemin vers le dossier .geri/ADR/.
- Identifiant de l'Intent ou de l'ADR cible.

## Sorties

- Lien de traceabilite entre code, Intent et ADR.
- Rapport de coherence (valide / incoherent / orphelin).
- Code retour 0 si traceabilite etablie, 1 si lien manquant, 2 si incoherence.

## Regles Operationnelles

### 1. Toute modification de code liee a un Intent
Aucune modification de code significative ne peut etre commitee sans etre liee a un Intent dans .geri/INTENTS/.

### 2. Tout Intent lie a un ADR
Tout Intent doit etre lie a un Architecture Decision Record dans .geri/ADR/. Un Intent orphelin est signale.

### 3. Verification de coherente avant commit
Avant tout commit, le skill verifie que chaque fichier modifie possede un lien traceability valide vers un Intent et un ADR.

### 4. Rejet en cas de lien manquant
Si un fichier modifie n'est lie a aucun Intent ou ADR, le commit est bloque avec un message d'erreur precis.

### 5. Journalisation des liens
Chaque lien traceabilite est consigne dans un registre de gouvernance avec l'horodatage et l'identifiant du commit.
