---
type: SPEC
version: 1.0.0
intent_hash: 0xSPEC_FILESYSTEM_PROOF_VERIFIER_20261106
status: proposed
wal_id: 0x243
friction: 0.0
entropy: 0.0
seal: WAL-0x243-SPEC-FS-PROOF-PASS
---

# Spécification — filesystem-proof-verifier

## 1. Objet

Définir une règle interdisant l'utilisation de `Set-Content` (PowerShell) sur les fichiers sources `.py` et exigeant une relecture (hash SHA-256) après toute écriture, pour prévenir la corruption silencieuse de fichiers.

## 2. Contexte

Lors de la Phase 3 du PRD-MOC WiCi, le fichier `scripts/vault_sync_daemon.py` a été corrompu par une commande `Set-Content -Encoding UTF8` de PowerShell qui a inséré des codes d'inversion vidéo (ANSI escape sequences) autour de chaque ligne, provoquant une `IndentationError` à l'exécution.

## 3. Règles obligatoires

### R1 — Interdiction de Set-Content sur .py
Il est interdit d'utiliser `Set-Content`, `Out-File` ou tout cmdlet PowerShell d'écriture en bloc sur un fichier `.py`.

Autorisé : édition ciblée avec l'outil `edit` (remplacement de `oldString` par `newString` uniquement).

### R2 — Relecture obligatoire (hash SHA-256)
Après toute écriture sur un fichier `.py` :
1. Recalculer le hash SHA-256 du fichier.
2. Comparer avec le hash attendu (calculé avant écriture ou de référence).
3. Relire le fichier pour vérifier l'absence de caractères invisibles, espaces en fin de ligne, ou codes ANSI.

### R3 — Vérification post-écriture
Avant tout commit, exécuter `python -m py_compile <fichier.py>` pour vérifier la syntaxe.

## 4. Détection de corruption

Si le fichier contient des séquences `\x1b[` (ESC CSI), des espaces de fin de ligne, ou des caractères non-UTF-8, l'écriture est considérée comme corrompue et doit être annulée (restauration depuis git).

## 5. Référence ADR

- **ADR** : ADR-096-powershell-regex-safety (principe de vérification après remplacement)
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed
