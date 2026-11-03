---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_KRS_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/known-repositories-syncer/SKILL.md
---

# Skill - known-repositories-syncer

## Objectif

Assurer que tout nouveau clone de backend (ex: jupyter-server-mcp) est inscrit dans known_repositories.yaml sans derive. Garantit la coherence entre les clones physiques et le registre SOT.

## Declencheur

- Creation d'un nouveau clone de depot.
- Ajout d'un backend MCP ou d'un outil citoyen.
- Modification de known_repositories.yaml.
- Verification de coherence avant tout clone git.

## Entrees

- Chemin vers known_repositories.yaml (SOT).
- Nom du depot (full_name = gerivdb/<REPO>).
- Chemin local (local_path) cible.
- URL remote du depot.

## Sorties

- Mise a jour de known_repositories.yaml avec l'entree du repo.
- Rapport de coherence (conforme / incoherent / manquant).
- Code retour 0 si inscription reussie, 1 si derive detectee, 2 si entree manquante.

## Regles Operationnelles

### 1. Pas de clone sans entree SOT
Tout depot clone doit posseder une entree dans known_repositories.yaml avec un champ local_path valide.

### 2. Verification de la strate L*
Le champ local_path doit correspondre a une strate L* valide (L0-L6). Pas de clone hors strate.

### 3. Verification de l'existence physique
Avant toute inscription, verifier que le dossier local_path existe physiquement sur le disque.

### 4. Pas de derive SOT
Si known_repositories.yaml mentionne un repo qui n'existe pas physiquement, ou inversement, signaler une derive pour intervention HITL.

### 5. Journalisation des inscriptions
Chaque ajout ou modification dans known_repositories.yaml est consigne avec l'horodatage et l'identifiant du depot.
