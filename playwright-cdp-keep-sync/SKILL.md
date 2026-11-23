---
type: SKILL
version: 1.0.0
status: active
intent_hash: 0xPLAYWRIGHT_CDP_KEEP_SYNC_20261119
wal_reference: "WAL-0x243-PLAYWRIGHT_CDP_KEEP_SYNC-001"
repo: gerivdb/D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\playwright-cdp-keep-sync
cible: D:\DO\WEB\TOOLS\ENV2\sync_keep.py
stratum: L4-TOOLS
---

# Skill : Playwright CDP Keep Sync — Consignation Keep Causal sur ENV2

## Objectif

Synchroniser une note `[CAUSAL]` depuis Flatnotes (ENV2) vers Google Keep via attachement CDP au profil Chromium déjà ouvert sur `127.0.0.1:9222`, sans lancer de nouveau profil et sans intermédiaire IA.

## Déclencheur

Toute demande de création ou de mise à jour d'une note Google Keep à partir d'un fichier `[CAUSAL]` généré par ENV2, via le script local `D:\DO\WEB\TOOLS\ENV2\sync_keep.py`.

## Prérequis

1. Chromium ouvert avec le port de débogage distant sur `127.0.0.1:9222` (`chrome.exe --remote-debugging-port=9222`).
2. Playwright installé (`pip install playwright`).
3. Fichier `[CAUSAL]` présent dans `D:\DO\WEB\TOOLS\L0-CANON\ENV3-repo\m3-state/`.
4. Session Google Keep authentifiée dans le profil Chromium attaché.

## Fonctionnement

Le script `D:\DO\WEB\TOOLS\ENV2\sync_keep.py` :
1. Lit le dernier fichier `REF-CAUSAL*.md` depuis Flatnotes `m3-state/`.
2. S'attache au profil Chromium existant via `connect_over_cdp("http://127.0.0.1:9222")`.
3. Ouvre `https://keep.google.com/` (ou réutilise l'onglet déjà ouvert).
4. Injecte le titre et le corps via JavaScript directe sur les éléments `div[aria-label='Titre']` et `div[role='textbox']`.
5. Sauvegarde la note (touche Entrée).

## Sortie brute attendue

```
[INFO] Fichier cible identifié : D:\DO\WEB\TOOLS\L0-CANON\ENV3-repo\m3-state\REF-CAUSAL-*.md
[INFO] Titre : REF-CAUSAL-*
[INFO] Corps : N caractères prêts à l'injection.
[INFO] Attachement au profil Chromium sur 127.0.0.1:9222...
[SUCCÈS] Attachement réussi.
[INFO] Session actuelle détectée sur : https://keep.google.com/
[INFO] Déjà sur Google Keep, réutilisation de l'onglet.
[INFO] Injection du contenu via JavaScript directe...
[INFO] Résultat injection JS : titre=True, corps=True
[INFO] Sauvegarde de la note...
[SUCCÈS FINAL] Note [CAUSAL] injectée avec succès dans Google Keep via CDP.
[JALON] Consignation Keep Causal sur ENV2 : CLÔTURÉ ET SOUVERAIN.
```

## Fichiers employés durant la conversation

- `D:\DO\WEB\TOOLS\ENV2\sync_keep.py` : script d'exécution (Playwright CDP).
- `D:\DO\WEB\TOOLS\ENV2\.env` : fichier de configuration (placeholders, non utilisé par la version finale Playwright).
- `D:\DO\WEB\TOOLS\L0-CANON\ENV3-repo\m3-state\REF-CAUSAL-KEEP-ALTERNATIVES-ENV2-v3.md` : fichier source `[CAUSAL]` injecté.

## Références

- Port CDP : `http://127.0.0.1:9222/json/version` (HTTP 200).
- Chrome version cible : 147.0.7727.55.
- M3 : Friction 0.0, Entropie 0.0, Atomicité respectée.
