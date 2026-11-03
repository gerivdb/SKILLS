---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_RHIG_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/registry-hash-integrity-guard/SKILL.md
---

# Skill - registry-hash-integrity-guard

## Objectif

Resout l'Impense 2 : verifie la signature SHA256 de REGISTRY.yaml contre menu.yaml au chargement. Garantit l'integrite du registre des skills avant toute utilisation.

## Declencheur

- Chargement de REGISTRY.yaml au demarrage du systeme.
- Modification de REGISTRY.yaml ou menu.yaml.
- Verification d'integrite avant utilisation des skills.

## Entrees

- Chemin vers REGISTRY.yaml.
- Chemin vers menu.yaml.
- Signature SHA256 attendue de REGISTRY.yaml.

## Sorties

- Rapport d'integrite (conforme / incoherent / corrompu).
- Code retour 0 si integrite verifiee, 1 si signature invalide, 2 si fichier manquant.

## Regles Operationnelles

### 1. Verification de la signature SHA256
Au chargement de REGISTRY.yaml, calculer son hash SHA256 et le comparer a la reference dans menu.yaml.

### 2. Rejet en cas d'incoherence
Si les hash ne correspondent pas, REGISTRY.yaml est considere comme corrompu et le chargement est bloque.

### 3. Alerting
En cas d'incoherence, alerter l'administrateur pour restauration depuis une sauvegarde connue.

### 4. Journalisation
Chaque verification d'integrite est consignee avec le hash calcule, le hash attendu et l'horodatage.

### 5. Escalade
Si l'integrite ne peut pas etre restauree, signaler pour intervention HITL.
