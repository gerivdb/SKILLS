---
name: comet-universal-content-script
version: "0.1.1"
status: active
type: procedural
category: cdp
intent_hash: 0xCOMET_UNIVERSAL_CONTENT_SCRIPT_20261126
provenance: imported
source_shard: ENV2
created_at: "2026-11-26T06:48:00Z"
updated_at: "2026-11-26T06:48:00Z"
author: Kilo (Shard G, ENV2)
triggers:
  - "content script"
  - "universel"
  - "ISOLATED world"
  - "all_urls"
  - "observation DOM"
  - "comet-agent"
anti_triggers:
  - "headless"
  - "profil temporaire"
  - "data-message-author-role"
  - "attribut suppose"
weight:
  - 5
  - 5
  - 4
  - 4
  - 5
  - 5
prerequisites:
  - "Extension avec host_permissions: <all_urls>"
  - "Content scripts declares dans manifest.json"
  - "Chromium Profil 2 sur port 9222"
verification:
  command: "python scripts/verify_content_injection.py"
  expected_exit_code: 0
  expected_output_contains: "content_injecte"
hash_sha256_evidence: "<hash recalcule sur le fichier actuel sur disque, stocke dans EVIDENCE.md>"
supersedes: []
superseded_by: null
tags:
  - "comet"
  - "content-script"
  - "universel"
  - "isolated-world"
  - "cdp"
  - "observation-dom"
---

# Skill : comet-universal-content-script — Content script universel d'observation DOM

## Objectif

Générer un content script universel injecté sur `<all_urls>` en world ISOLATED (document_start), avec exclusion des domaines internes (`*.perplexity.ai/sidecar/*`, `localhost:*/sidecar*`), à partir du pattern comet-agent de Comet.exe. Ce skill permet l'observation DOM universelle et l'injection d'assistant contextuel.

## Localisation

`D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\skills\comet-universal-content-script/`

## Fichiers du skill

- `SKILL.md` — ce document (contrat du skill)
- `scripts/content.js` — script de contenu universel (observation DOM)
- `scripts/events.js` — capture d'événements (clics, soumissions, changements d'URL)
- `scripts/content.css` — styles injectés
- `scripts/verify_content_injection.py` — vérification de l'injection via CDP
- `references/comet-agent-manifest.json` — copie de référence du manifest comet-agent

## Prérequis

- Extension avec `host_permissions: <all_urls>`
- Content scripts déclarés dans `manifest.json`
- Chromium Profil 2 sur port 9222

## Procédure d'exécution

1. Générer `manifest.json` avec `content_scripts` sur `<all_urls>`, `exclude_matches` internes, `world: ISOLATED`, `run_at: document_start`.
2. Générer `content.js` (observation DOM via MutationObserver).
3. Générer `events.js` (capture d'événements : clics, soumissions de formulaires, changements d'URL).
4. Générer `content.css` (styles injectés isolés).
5. Charger l'extension non empaquetée dans Chromium Profil 2.
6. Vérifier l'injection sur une page de test via CDP.
7. Sceller le résultat dans le WAL 0x243 (hash SHA-256 + timestamp UTC).
8. Générer `EVIDENCE.md` avec la sortie brute, le hash et l'horodatage.

## Règles de bonne pratique

- Utiliser des sélecteurs de rôle (classes CSS observées), jamais d'attributs supposés (`data-message-author-role` absent sur DeepSeek).
- Filtrer par rôle assistant (blocs `.f9bf7997` / `[class*="f9bf"]`) pour toute corrélation de réponse.
- Assertion d'ACK par regex ancrée `^\[ENV6\]\s+ACK\s+`, jamais `includes()`.
- Exclure les domaines internes (`*.perplexity.ai/sidecar/*`, `localhost:*/sidecar*`) des content scripts universels.
- Respecter l'invariant ALLUMÉ du M3TREE : le port CDP 9222 reste actif pendant toute l'opération.

## Vérification

Exécuter `python scripts/verify_content_injection.py` depuis le dossier du skill. Code de sortie attendu : 0. Sortie doit contenir `content_injecte`.

## Historique

- v0.1.0 (2026-11-26) : création initiale, phagocytose de l'extrait Comet.exe comet-agent.

## Références

- `docs/ETUDE-COMET-EXE-NAVIGATION-CDP.md` (ENV3-repo, hash `5562D990...`)
- `docs/M3-PHAGOCYTOSE-COMET-EXE-NAVIGATION-CDP.md` (ENV3-repo, hash `F1D20F06...`)
- `SPEC-SKILL-FORMAT.md` (L4-TOOLS/SKILLS)
- `rule-dom-empiricism.md` (ENV3-repo/.kilocode/rules/)
- `rule-non-subchain-assertions.md` (ENV3-repo/.kilocode/rules/)
- `rule-proof-recalculation.md` (ENV3-repo/.kilocode/rules/)
