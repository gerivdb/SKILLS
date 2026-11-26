---
name: comet-embedded-extensions
version: "0.1.0"
status: draft
type: procedural
category: cdp
intent_hash: 0xCOMET_EMBEDDED_EXTENSIONS_20261126
provenance: imported
source_shard: ENV2
created_at: "2026-11-26T06:45:00Z"
updated_at: "2026-11-26T06:45:00Z"
author: Kilo (Shard G, ENV2)
triggers:
  - "comet"
  - "extensions embarquees"
  - "external_extensions.json"
  - "CRX"
  - "install extension"
  - "chromadium extensions embarquees"
anti_triggers:
  - "headless"
  - "profil temporaire"
  - "playwright launch"
  - "profil jetable"
weight:
  - 5
  - 5
  - 4
  - 4
  - 4
  - 3
prerequisites:
  - "Chromium lance sur Profil 2, port 9222 repondant"
  - "Fichiers CRX disponibles (perplexity.crx, comet_web_resources.crx, agents.crx)"
  - "Registre external_extensions.json accessible"
verification:
  command: "python scripts/verify_extensions_installed.py"
  expected_exit_code: 0
  expected_output_contains: "extensions_activees"
hash_sha256_evidence: "<hash recalcule sur le fichier actuel sur disque, stocke dans EVIDENCE.md>"
supersedes: []
superseded_by: null
tags:
  - "comet"
  - "extensions-embarquees"
  - "cdp"
  - "crx"
  - "profil-2"
---

# Skill : comet-embedded-extensions — Gestion des extensions Chromium embarquées par défaut

## Objectif

Lire le registre `external_extensions.json` de Comet.exe, installer les 3 extensions CRX (Comet, Comet Web Resources, comet-agent) avec leurs IDs fixes, versions externes et update_url dans un navigateur Chromium Profil 2 via CDP. Ce skill phagocyte le modèle d'extensions embarquées de Perplexity pour le projet de navigateur Chromium personnalisé.

## Localisation

`D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\skills\comet-embedded-extensions/`

## Fichiers du skill

- `SKILL.md` — ce document (contrat du skill)
- `scripts/install_extensions.py` — installation des 3 CRX via CDP avec IDs fixes
- `scripts/read_external_extensions.py` — lecture du registre `external_extensions.json`
- `scripts/verify_extensions_installed.py` — vérification que les extensions sont actives via CDP management.getAll
- `references/comet-external-extensions.json` — copie de référence du registre Comet (extrait de `default_apps\external_extensions.json`)

## Prérequis

- Chromium lancé sur Profil 2, port 9222 répondant sur `http://localhost:9222/json/version`
- Fichiers CRX disponibles : `perplexity.crx`, `comet_web_resources.crx`, `agents.crx`
- Registre `external_extensions.json` accessible (copie dans `references/`)

## Procédure d'exécution

1. Lire `external_extensions.json` pour récupérer la mapping ID → version externe → fichier CRX.
2. Pour chaque entrée, appeler CDP pour installer l'extension avec son ID fixe (pas de réattribution d'ID).
3. Vérifier l'activation via `management.getAll` : chaque extension doit apparaître avec `enabled: true`.
4. Sceller le résultat dans le WAL 0x243 (hash SHA-256 + timestamp UTC).
5. Générer `EVIDENCE.md` avec la sortie brute, le hash et l'horodatage.

## Règles de bonne pratique

- Ne JAMAIS modifier l'ID d'une extension (IDs fixes canoniques : `mcjlamohcooanphmebaiigheeeoplihb`, `mjdcklhepheaaemphcopihnmjlmjpcnh`, `npclhjbddhklpbnacpjloidibaggcgon`).
- Ne JAMAIS lancer Chromium avec `--headless`.
- Ne JAMAIS utiliser un profil temporaire (`--user-data-dir=C:\Temp\`).
- Utiliser l'`update_url` commun (`https://www.perplexity.ai/rest/browser/update-crx?channel=stable`) pour les mises à jour.
- Respecter l'invariant ALLUMÉ du M3TREE : le port CDP 9222 reste actif pendant toute l'opération.

## Vérification

Exécuter `python scripts/verify_extensions_installed.py` depuis le dossier du skill. Code de sortie attendu : 0. Sortie doit contenir `extensions_activees`.

## Historique

- v0.1.0 (2026-11-26) : création initiale, phagocytose de l'extrait Comet.exe.

## Références

- `docs/ETUDE-COMET-EXE-NAVIGATION-CDP.md` (ENV3-repo, hash `5562D990...`)
- `docs/M3-PHAGOCYTOSE-COMET-EXE-NAVIGATION-CDP.md` (ENV3-repo, hash `F1D20F06...`)
- `SPEC-SKILL-FORMAT.md` (L4-TOOLS/SKILLS)
- `rule-dom-empiricism.md` (ENV3-repo/.kilocode/rules/)
- `rule-proof-recalculation.md` (ENV3-repo/.kilocode/rules/)
