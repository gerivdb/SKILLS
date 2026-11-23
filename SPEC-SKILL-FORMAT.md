# Spécification unifiée SKILL.md — Repo Skills L4

**Version** : 1.0.0  
**IntentHash** : 0xSKILL_FORMAT_UNIFIED_20261123  
**Dépôt** : `D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS/`  
**Statut** : accepted  

---

## 1. Objectif de la spécification

Unifier le format des fichiers `SKILL.md` dans le repo Skills L4 pour que :

1. Tout skill soit **découvrable** (nom, description, triggers, catégorie).
2. Tout skill soit **exécutable** (procédure, prérequis, commande de lancement, vérification).
3. Tout skill soit **versionné** et **traçable** (hash, auteur, date, preuves).
4. Tout skill soit **réutilisable cross-shard** (peu être chargé depuis n'importe quel shard ENV2 sans re-planification).
5. La distillation "transcript de shard → SKILL.md" soit mécanique (script `distill-skill.ps1` peut générer ce format).

---

## 2. Structure obligatoire d'un fichier SKILL.md

Chaque skill réside dans son propre dossier sous `D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS/skills/<nom-du-skill>/`.

```
<nom-du-skill>/
├── SKILL.md              # Contrat du skill (obligatoire)
├── EVIDENCE.md           # Preuves d'exécution (obligatoire après promotion)
├── HISTORY.md            # Journal des versions (obligatoire après v0.1.0)
├── scripts/              # Code exécutable (PowerShell, Python, etc.)
├── references/           # Références externes, docs, ADR
└── assets/               # Templates, schémas, configs
```

### 2.1 Frontmatter YAML (obligatoire, en tête du fichier)

```yaml
---
name: <nom-du-skill>              # kebab-case, doit correspondre au nom du dossier
version: "0.1.0"                  # SemVer, commence à 0.1.0
status: draft | active | superseded | archived
type: procedural | episodic | factual | composite
category: <catégorie>             # ex: cdp, profile, git, build, test, ci, memory
intent_hash: 0x<SKILL_MAJUSCULES_YYYYMMDD>
provenance: shard-<ENV_ID> | manual | distilled | imported
source_shard: <ENV2|ENV3|...>     # Shard d'origine si distillé
created_at: "YYYY-MM-DDTHH:MM:SSZ"
updated_at: "YYYY-MM-DDTHH:MM:SSZ"
author: <agent|humain|auto>
triggers:
  - <mot-clé ou pattern qui active ce skill>
  - <ex: "chromium", "profil 2", "cdp">
anti_triggers:
  - <mot-clé ou pattern qui DÉSACTIVE ce skill>
  - <ex: "headless", "profil temporaire", "shard-ENV6">
weight:
  - <poids d'importance du trigger, 1 à 5>
prerequisites:
  - <ex: "Chromium lancé sur port 9222">
  - <ex: "Python 3 avec cdp-use">
verification:
  command: <commande pour vérifier que le skill fonctionne>
  expected_exit_code: 0
  expected_output_contains: <fragment de sortie attendu>
hash_sha256_evidence: <hash du fichier SKILL.md, stocké dans EVIDENCE.md, pas ici pour éviter l'auto-référence circulaire>
supersedes: []
superseded_by: null
tags:
  - <tag1>
  - <tag2>
---
```

### 2.2 Sections du corps Markdown (obligatoires)

#### a) Objectif (`## Objectif`)
Une phrase : ce que fait le skill, dans quel contexte, pour quel usage.

#### b) Localisation (`## Localisation`)
Chemin absolu du dossier du skill sur disque.

#### c) Fichiers du skill (`## Fichiers du skill`)
Liste des fichiers présents dans le dossier avec leur rôle.

#### d) Prérequis (`## Prérequis`)
Ce qui doit être vrai avant d'exécuter le skill (ports, fichiers, variables d'environnement, processus résidents).

#### e) Procédure d'exécution (`## Procédure`)
Étapes numérotées, commande de lancement, exemples d'utilisation.

#### g) Règles de bonne pratique (`## Règles de bonne pratique`)
Ce qu'il ne faut JAMAIS faire avec ce skill (inspiré du format existant chromium-profile-2).

#### h) Vérification (`## Vérification`)
Comment tester que le skill fonctionne (commande, sortie attendue, hash du résultat).

#### i) Historique (`## Historique`)
Lien vers `HISTORY.md` ou résumé des versions.

---

## 3. Modèle de versioning (inspiré AutoSkill)

- Un skill commence à `v0.1.0` (statut `draft`).
- Après validation par le gate (`validate-skill.ps1`), il passe à `v0.1.0` statut `active`.
- Une mise à jour crée `v0.1.1` (merge, pas duplication).
- Un skill remplacé est marqué `superseded` avec `superseded_by` pointant vers le nouveau.
- L'historique complet est dans `HISTORY.md`.

---

## 4. Règle de découverte (progressive disclosure, inspiré hermes-agent + metis)

1. **Discovery** : l'index des skills (nom + catégorie + triggers pondérés + status) est chargé au démarrage d'une session via `skills-index.json`. L'index reste léger : seuls les métadonnées sont lues, pas le corps complet des SKILL.md.
2. **Scoring pondéré** : chaque trigger possède un `weight` (1 à 5). Le score de correspondance d'un skill pour une tâche donnée est la somme des poids des triggers matchés, moins le poids des `anti_triggers` matchés. Seul le(s) skill(s) au score supérieur au seuil est/sont activé(s).
3. **Activation** : le corps complet du `SKILL.md` est chargé UNIQUEMENT quand un trigger correspond à la tâche en cours et qu'aucun anti_trigger n'est matché.
4. **Execution** : les fichiers sous `scripts/`, `references/`, `assets/` ne sont chargés que si la procédure le dirige, avec des chemins absolus explicites (règle `explicit-path-compliance`).

### 4.1 anti_triggers

Chaque skill déclare une liste `anti_triggers` : motifs qui DÉSACTIVENT ce skill même si un trigger est matché. Exemple : un skill CDP ne doit pas s'activer sur une tâche "profil temporaire" ou "shard-ENV6 sans port 9222".

```yaml
triggers:
  - "chromium"      # weight 5
  - "cdp"           # weight 4
anti_triggers:
  - "headless"      # weight 5
  - "profil temporaire"  # weight 3
weight:
  - 5   # pour "chromium"
  - 4   # pour "cdp"
```

---

## 5. Preuve d'exécution (EVIDENCE.md)

Après chaque utilisation réussie du skill, un `EVIDENCE.md` est ajouté dans le dossier du skill :

```markdown
# Preuve d'exécution — <nom-du-skill>

- **Date** : YYYY-MM-DDTHH:MM:SSZ
- **Shard** : ENV2 / ENV3 / ...
- **Commande exécutée** : ...
- **Code de sortie** : 0
- **Sortie brute** : <stdout complet, entre triple backticks>
- **Hash SHA-256 du résultat** : <hash>
- **Fichiers modifiés** : <liste>
- **Validé par** : <agent|humain>
- **Résultat** : `succès` | `échec` | `contourné`
- **Cause racine (si échec)** : <description courte>
- **Score d'utilité mis à jour** : <nombre, ex: +1 ou -1>

### 5.1 Boucle de retour (feedback loop)

Après chaque utilisation d'un skill, qu'elle ait réussi ou échoué, une entrée est ajoutée à `EVIDENCE.md` avec le résultat et la cause racine le cas échéant. Ce score d'utilité alimente le scoring de l'index : un skill dont le score d'utilité tombe sous un seuil est marqué `superseded` ou révisé via `distill-skill.ps1 --base-skill`.
```



---

## 6. Exemple de SKILL.md minimal

```markdown
---
name: chromium-profile-2
version: "1.0.0"
status: active
type: procedural
category: cdp
intent_hash: 0xCHROMIUM_PROFILE_2_20261123
provenance: manual
source_shard: ENV2
created_at: "2026-11-23T03:00:00Z"
updated_at: "2026-11-23T03:00:00Z"
author: humain
triggers:
  - "chromium"
  - "profil 2"
  - "cdp"
  - "9222"
anti_triggers:
  - "headless"
  - "profil temporaire"
weight:
  - 5
  - 4
  - 4
  - 3
prerequisites:
  - "Chromium lancé avec --user-data-dir et --profile-directory=Profile 2"
  - "Port 9222 répond sur http://localhost:9222/json"
verification:
  command: "python -c \"from chromium_cdp_client import ChromiumCDPClient; c=ChromiumCDPClient(); print(c.get_status())\""
  expected_exit_code: 0
  expected_output_contains: "onglets"
hash_sha256_evidence: "<hash calculé et stocké dans EVIDENCE.md>"
supersedes: []
superseded_by: null
tags:
  - "chromium"
  - "cdp"
  - "profil-2"
---

# Skill : chromium-profile-2 — Pilotage CDP de Chromium (profil 2)

## Objectif
Piloter l'instance Chromium déjà ouverte en profil 2 (port 9222) via le Chrome DevTools Protocol (CDP).

## Localisation
`D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\chromium-profile-2/`

## Fichiers du skill
- `chromium_cdp_client.py` — client CDP.
- `SKILL.md` — ce document.
- `test_skill.py` — test unitaire de validation.

## Prérequis
- Chromium lancé avec les flags : --user-data-dir="..." --profile-directory="Profile 2" --remote-debugging-port=9222 --remote-allow-origins=*
- Le port 9222 doit répondre.

## Procédure
1. Importer le module : `sys.path.insert(0, r'D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\chromium-profile-2')`
2. Instancier : `client = ChromiumCDPClient()`
3. Appeler une méthode : `client.open_tab("https://example.com")`

## Règles de bonne pratique
- Ne JAMAIS tuer ou redémarrer le Chromium déjà ouvert.
- Ne JAMAIS ouvrir une nouvelle fenêtre — toujours un nouvel onglet.

## Vérification
Exécuter `test_skill.py` depuis le dossier du skill.

## Historique
Voir `HISTORY.md`.
```

---

## 7. Règles de gouvernance du format

1. **Un skill = un dossier** : jamais deux skills dans le même dossier, jamais un skill sans dossier.
2. **SKILL.md obligatoire** : un dossier sans `SKILL.md` n'est pas un skill valide.
3. **Hash recalculé** : le `hash_sha256` du frontmatter doit correspondre au fichier actuel sur disque (règle Preuve Fraîche).
4. **Pas de paraphrase** : toute référence à un autre skill cite son `SKILL.md` intégralement entre triple backticks avec hash.
5. **Cross-shard** : un skill promu dans `skills/` doit être utilisable depuis n'importe quel shard sans modification de chemin (chemins absolus ou relatifs au dossier du skill).

---

## 8. Références externes intégrées

| Source | Élément repris |
|--------|---------------|
| vercel-labs/skills | Format `SKILL.md` avec frontmatter YAML (`name`, `description`) |
| NousResearch/hermes-agent | `skill_manage` (create/patch/delete), write-approval gate, progressive disclosure |
| ECNU-ICALK/AutoSkill | Versioning `v0.1.0 → v0.1.1`, merge au lieu de duplication, format universel `SKILL.md` |
| palasht75/skilldistill | Workflow review-first : scan → distill → consolidate → overlaps |
| thatdhruv/skillforge | Gate de validation avant promotion (≥3 cas vérifiés, pas de doublon) |

---

## 9. Index de découverte et routage (cristallisation + réinvocation)

Un skill stocké sur disque sans mécanisme d'indexation est une clé dans la poche. Cette section définit comment les skills sont indexés, découverts et réinvoqués d'un shard à l'autre.

### 9.1 Fichier d'index : `skills-index.json`

À la racine du repo Skills (`D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\skills-index.json`), un index central liste tous les skills disponibles. Il est généré par `index-skills.ps1` et consulté avant chaque tâche pour décider quel(s) skill(s) activer.

**Structure :**
```json
{
  "generated_at_utc": "2026-11-23T04:00:00Z",
  "source_repo": "D:\\DO\\WEB\\TOOLS\\L4-TOOLS\\SKILLS",
  "skills": [
    {
      "name": "chromium-profile-2",
      "version": "1.0.0",
      "status": "active",
      "type": "procedural",
      "category": "cdp",
      "intent_hash": "0xCHROMIUM_PROFILE_2_20261123",
      "provenance": "manual",
      "source_shard": "ENV2",
      "path": "skills/chromium-profile-2",
      "triggers": ["chromium", "profil 2", "cdp", "9222"],
      "tags": ["chromium", "cdp", "profil-2"],
      "hash_sha256": "...",
      "created_at": "2026-11-23T03:00:00Z",
      "updated_at": "2026-11-23T03:00:00Z"
    }
  ]
}
```

### 9.2 Génération de l'index — `index-skills.ps1`

Le script scanne `skills/*/SKILL.md`, extrait le frontmatter YAML de chacun, et régénère `skills-index.json`. Il doit être exécuté après toute promotion, modification ou suppression de skill.

### 9.3 Protocole de rappel (routage inter-shards)

Avant toute tâche dans un shard (ENV2, ENV3, etc.) :

1. **Lecture de l'index** : charger `skills-index.json` (ou le régénérer si obsolète).
2. **Corrélation des triggers** : comparer les mots-clés de la demande avec les `triggers` de chaque skill. Un score de pertinence est calculé (nombre de triggers matchés, poids par catégorie).
3. **Activation** : le(s) skill(s) avec le meilleur score sont chargés selon la règle de découverte progressive (découverte → activation → execution).
4. **Journalisation** : chaque activation est consignée (skill activé, trigger matché, shard, horodatage UTC).

**Règle** : un skill en statut `draft` n'est pas activable automatiquement ; seul un skill `active` l'est. Un skill `superseded` pointe vers son remplaçant via `superseded_by`.

### 9.4 Règle de fraîcheur de l'index

L'index doit être régénéré si :
- Un skill est promu de `draft` à `active`
- Un skill est mis à jour (nouvelle version, nouveaux triggers)
- Un skill est marqué `superseded` ou `archived`

**Mécanisme automatique** : `validate-skill.ps1` appelle `index-skills.ps1` à la fin de toute promotion réussie pour garantir que `skills-index.json` reflète l'état réel de `skills/`. Un shard qui lit un index périmé risque d'activer un skill obsolète ou d'en ignorer un nouveau.

---

## 10. Règles de gouvernance globales (synthèse)

1. **Un skill = un dossier** avec `SKILL.md` obligatoire.
2. **Hash recalculé** : le `hash_sha256` du frontmatter doit correspondre au fichier actuel sur disque (règle Preuve Fraîche).
3. **Pas de paraphrase** : toute référence à un autre skill cite son `SKILL.md` intégralement entre triple backticks avec hash.
4. **Cross-shard** : un skill promu dans `skills/` doit être utilisable depuis n'importe quel shard sans modification de chemin.
5. **Index obligatoire** : `skills-index.json` doit refléter l'état réel de `skills/` avant toute réinvocation.
6. **Preuve d'exécution** : chaque utilisation d'un skill génère une entrée `EVIDENCE.md` avec sortie brute, hash et horodatage UTC.

---

**Màj requise si** : modification du format SKILL.md, ajout de la section index, changement de statut d'un skill, ou évolution du modèle de versioning.