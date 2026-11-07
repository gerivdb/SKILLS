---
type: SPEC
version: 1.0.0
intent_hash: 0xSPEC_LINTER_FAKE_UUID_20261106
status: proposed
wal_id: 0x243
friction: 0.0
entropy: 0.0
seal: WAL-0x243-SPEC-LINTER-PASS
---

# Spécification — spec-linter

## 1. Objet

Définir une règle de validation (`spec-linter`) qui bloque tout commit git contenant des identifiants factices, des placeholders non résolus, ou des sceaux Merkle générés sans hash réel dans les dépôts du métacluster GERIVDB.

## 2. Déclencheur

Avant tout `git commit` sur une branche de travail (`feat/*`, `fix/*`, `docs/*`) dans un dépôt ENV2/ENV3 touchant :
- `WAL/*` (fichiers de journalisation)
- `scripts/*` (scripts d'exécution)
- `*.md` (documents de spécification)
- `*.json` (registres, manifests)

## 3. Règles de validation

### R1 — UUIDs factices interdits
Tout commit contenant une chaîne correspondant au pattern :
```
00000000-0000-0000-0000-000000000000
```
doit être refusé.

### R2 — Placeholders non résolus interdits
Tout commit contenant une chaîne correspondant au pattern :
```
16be1ada-808b-4ba1-9064-7a3de2a56103
```
ou tout UUID incluant des séquences répétées de `0` ou `a` indiquant un placeholder non remplacé, doit être refusé.

### R3 — Sceaux Merkle générés sans hash réel
Tout fichier `WAL/*` ou `*.json` contenant un champ `merkle_root`, `merkle_fingerprint` ou `seal` dont la valeur ne provient pas d'un hash SHA-256 réel calculé sur le contenu doit être refusé.
- Valeur rejetée : `"MERKLE_00000000_0x243"`, `"WAL-0x243-PLIX-CODEC-PASS"` sans hash associé, chaîne vide.

### R4 — Pré-commit obligatoire
Le `spec-linter` doit s'exécuter en pre-commit sur tous les fichiers stagés. Si une règle est violée, le commit est bloqué avec message d'erreur indiquant la règle et le fichier concerné.

## 4. Exceptions

Aucune exception. Un placeholder doit être remplacé par une valeur réelle avant tout commit.

## 5. Référence ADR

- **ADR** : ADR-091-hitl-gate-for-clone (principe de vérification avant mutation)
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed
