---
name: github-config
version: "2.2.0"
description: "GITHUB_TOKEN, gh auth, scopes, Actions settings, rate-limit, gestion des gros fichiers (push_files vs create_or_update, split‑payload, SHA‑management). Use when user mentions 'GITHUB_TOKEN', 'gh auth', 'scopes', 'Settings Actions', 'large files', 'push_files', 'create_or_update'."
triggers: ["GITHUB_TOKEN", "gh auth", "scopes", "Settings Actions", "large files", "push_files", "create_or_update"]
layer: "L1_CAUSALITY"
nexusTags: ["CONFORME_NEXUS"]
prerequisites: ["gh CLI >=2.0"]
slotWeight: 1
status: active
changelog:
  - {v: "2.2.0", date: "2026-06-03", notes: "Ajout SCAN_GATE — règle obligatoire avant tout listing de repos (anti-ERR_001/ERR_002)"}
  - {v: "2.1.0", date: "2026-05-30", notes: "Ajout gestion rate‑limit avec repli et stratégie gros fichiers"}
---
# GitHub Config

## Domaine et périmètre

Ce skill couvre la **configuration GitHub** pour l'écosystème gerivdb :
- GITHUB_TOKEN (création, rotation, scopes)
- Authentification `gh auth` (login, logout, status)
- Scopes et permissions (repo, workflow, admin:org)
- Settings Actions (permissions au niveau dépôt/organisation)
- Rate-limits GitHub API (monitoring, contournement)
- **Gestion des gros fichiers** : choix entre `push_files` et `create_or_update`, découpage en chunks, gestion des SHA de commit.

## SCAN_GATE — Règle obligatoire avant tout listing

> **IntentHash**: `0xSCAN_GATE_20260603`
> **Référence**: LLM_BOOT_PROTOCOL.md (GATE-0, GATE-1, GATE-2) dans gerivdb/LLM-REPO

Avant d'appeler `search_repositories` ou `list_repositories` sur gerivdb/* :

1. **Vérifier si known_repositories.yaml a été chargé dans ce contexte**
   - Si oui → utiliser known_repositories.yaml, **pas l'API**
   - Si non → charger known_repositories.yaml EN PREMIER, puis répondre

2. **search_repositories avec perPage=100 n'est autorisé QUE pour**
   - valider que known_repositories.yaml est à jour (max 1x par session)
   - **Jamais** pour lister les repos gerivdb dans une réponse

3. **Avant toute proposition de création de repo** (GATE-1) :
   - grep known_repositories.yaml pour le nom proposé
   - grep known_repositories.yaml pour le besoin fonctionnel
   - Si match → INTERDIT de proposer un nouveau repo (ERR_001)

4. **Ignorer les repos archivés** (ERR_005) :
   - La section ARCHIVE_GERI_CMS contient 104 repos dormants
   - Ne jamais les inclure dans les scans de repos actifs

## Méthodologie

### Phase 1 : Diagnostic
- Vérifier l'état de l'auth : `gh auth status`.
- Contrôler les scopes du token actuel : `gh auth token`.
- Vérifier les rate-limits : `gh api /rate_limit`.

### Phase 2 : Configuration
- Configurer le GITHUB_TOKEN avec les scopes requis.
- Ajuster les Settings Actions (permissions GITHUB_TOKEN).
- Configurer les webhooks et secrets CI si nécessaire.

### Phase 2bis : Gestion des gros fichiers
- Déterminer si le fichier dépasse le seuil recommandé (ex. : 100 Mo pour `push_files` ou 25 Mo pour `create_or_update` selon les limites GitHub).
- Si oui, privilégier `push_files` avec division du payload en chunks de 8 Mo chacune, en calculant le SHA de chaque chunk et en reconstituant le fichier côté serveur via un workflow dédié.
- Si non, utiliser `create_or_update` qui est plus simple et crée un seul commit.
- En cas de mise à jour fréquente, envisager un schéma de versionnage basé sur les tags Git plutôt que sur les commits afin de réduire la pression sur les références.

### Phase 3 : Validation
- Tester l'accès aux dépôts cibles.
- Vérifier que les workflows Actions se déclenchent correctement.
- Documenter la configuration (token expiry, scopes).

## Règles de décision
- **Règle 1** : Le GITHUB_TOKEN doit avoir au minimum les scopes `repo` et `workflow`.
- **Règle 2** : Les tokens expirent après 90 jours — planifier la rotation.
- **Règle 3** : Les rate-limits sont de 5000 requêtes/heure (auth) ou 60 (non-auth).
- **Règle 4** : Pour les fichiers > 100 Mo, utiliser obligatoirement `push_files` avec chunking ; sinon, `create_or_update` est autorisé.
- **Règle 5** : Après chaque opération, vérifier le SHA résultant avec `gh api repos/:owner/:repo/git/blobs/:sha` pour garantir l'intégrité.
- **Règle 6 (SCAN_GATE)** : known_repositories.yaml est la source canonique pour les repos gerivdb. L'API GitHub ne sert qu'à lire le contenu d'un repo déjà connu.

## Format de sortie

```markdown
## Config GitHub
- Auth : [OK | ERREUR]
- Scopes : [liste]
- Rate-limit : [N]/5000 restantes
- Token expiry : [date]
- Gros fichier stratégie : [PUSH_FILES | CREATE_OR_UPDATE]
- Taille du dernier transfert : [octets]
- SCAN_GATE : [APPLIED | SKIPPED]
```

## Exemples d'utilisation
- "Vérifie l'état de gh auth" → `gh auth status`.
- "Les workflows IRIS échouent — vérifie les permissions" → Inspecter Settings Actions.
- "Quel est mon rate-limit restant ?" → `gh api /rate_limit`.
- "Je dois déposer un binaire de 250 Mo" → Utiliser la stratégie `push_files` avec chunking.
- "Mettre à jour un fichier de configuration de 2 Ko" → Utiliser `create_or_update`.
- "Liste les repos gerivdb" → **Utiliser known_repositories.yaml, PAS l'API** (SCAN_GATE).

## Intégration avec l'écosystème
- Dépôts concernés : tous les repos gerivdb
- Couche EECS : L1_CAUSALITY
- Tags NEXUS : [CONFORME_NEXUS]
- Référence croisée : LLM_BOOT_PROTOCOL.md (gerivdb/LLM-REPO)
