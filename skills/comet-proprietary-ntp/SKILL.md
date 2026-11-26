---
name: comet-proprietary-ntp
version: "0.1.0"
status: draft
type: procedural
category: cdp
intent_hash: 0xCOMET_PROPRIETARY_NTP_20261126
provenance: imported
source_shard: ENV2
created_at: "2026-11-26T06:53:00Z"
updated_at: "2026-11-26T06:53:00Z"
author: Kilo (Shard G, ENV2)
triggers:
  - "ntp"
  - "new tab page"
  - "preconnect"
  - "proprietary"
  - "homepage"
  - "comet_web_resources"
anti_triggers:
  - "headless"
  - "profil temporaire"
  - "CDN externe"
weight:
  - 5
  - 5
  - 4
  - 4
  - 4
  - 5
prerequisites:
  - "CDN du projet accessible (equivalent de pplx-next-static-public.perplexity.ai, frontend-cdn.perplexity.ai, r2cdn.perplexity.ai)"
  - "Polices proprietaires disponibles"
  - "Chromium Profil 2 sur port 9222"
verification:
  command: "python scripts/verify_ntp_html.py"
  expected_exit_code: 0
  expected_output_contains: "ntp_valide"
hash_sha256_evidence: "<hash recalcule sur le fichier actuel sur disque, stocke dans EVIDENCE.md>"
supersedes: []
superseded_by: null
tags:
  - "comet"
  - "ntp"
  - "new-tab-page"
  - "preconnect"
  - "cdp"
  - "homepage"
---

# Skill : comet-proprietary-ntp — New Tab Page propriétaire avec preconnect CDN

## Objectif

Générer une New Tab Page propriétaire avec preconnect vers les CDN du projet, preload des polices, thème clair/sombre, et meta de versioning (`min-version`, `version`, `web-resources-build`). Ce skill phagocyte le modèle de NTP de Comet.exe (`comet_web_resources/spa/ntp.html`) pour le projet de navigateur Chromium personnalisé.

## Localisation

`D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\skills\comet-proprietary-ntp/`

## Fichiers du skill

- `SKILL.md` — ce document (contrat du skill)
- `spa/ntp.html` — New Tab Page propriétaire
- `spa/index.html` — Application principale
- `sidecar/index.html` — Panneau latéral (data-erp="sidecar")
- `scripts/verify_ntp_html.py` — vérification de la structure HTML des pages NTP
- `references/comet-ntp-html.html` — copie de référence de `spa/ntp.html` extrait de Comet

## Prérequis

- CDN du projet accessible (équivalent de `pplx-next-static-public.perplexity.ai`, `frontend-cdn.perplexity.ai`, `r2cdn.perplexity.ai`)
- Polices propriétaires disponibles (PPLX-Sans, FKGroteskNeue ou équivalents du projet)
- Chromium Profil 2 sur port 9222

## Procédure d'exécution

1. Créer `spa/ntp.html` avec `preconnect` vers les 3 CDN du projet.
2. Ajouter `preload` des polices critiques (PPLX-Sans, FKGroteskNeue ou équivalents du projet).
3. Définir `theme-color` light `#FCFCF9`, dark `#100E12` (ou charte projet).
4. Ajouter meta `min-version`, `version`, `web-resources-build` pour cache invalidation.
5. Créer `spa/index.html` (application principale) avec la même structure.
6. Créer `sidecar/index.html` (panneau latéral, `data-erp="sidecar"`).
7. Définir comme New Tab Page via CDP.
8. Sceller le résultat dans le WAL 0x243 (hash SHA-256 + timestamp UTC).
9. Générer `EVIDENCE.md` avec la sortie brute, le hash et l'horodatage.

## Règles de bonne pratique

- Pas de CDN externe (règle Local-First du DESIGN SYSTEM souverain).
- Tout est hébergé ou inline.
- Respecter le DESIGN SYSTEM souverain (tokens de design, couleurs, typographie, espacement).
- Thème clair/sombre intégré avec `prefers-color-scheme`.
- Meta de versioning pour cache invalidation.
- Respecter l'invariant ALLUMÉ du M3TREE : le port CDP 9222 reste actif pendant toute l'opération.

## Vérification

Exécuter `python scripts/verify_ntp_html.py` depuis le dossier du skill. Code de sortie attendu : 0. Sortie doit contenir `ntp_valide`.

## Historique

- v0.1.0 (2026-11-26) : création initiale, phagocytose de l'extrait Comet.exe comet_web_resources.

## Références

- `docs/ETUDE-COMET-EXE-NAVIGATION-CDP.md` (ENV3-repo, hash `5562D990...`)
- `docs/M3-PHAGOCYTOSE-COMET-EXE-NAVIGATION-CDP.md` (ENV3-repo, hash `F1D20F06...`)
- `SPEC-SKILL-FORMAT.md` (L4-TOOLS/SKILLS)
- `design_system.md` (ENV3-repo/.kilocode/rules/)
- `rule-proof-recalculation.md` (ENV3-repo/.kilocode/rules/)
