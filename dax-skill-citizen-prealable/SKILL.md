---
type: SKILL
version: 1.0.0
status: active
date: "2026-11-26"
intent_hash: 0xDAX_SKILL_CITIZEN_PREALABLE_20261126
layer: L0-CANON
author: gerivdb
source_repo: gerivdb/ENV3-repo
source_path: .kilocode/skills/dax-skill-citizen-prealable/SKILL.md
path: dax-skill-citizen-prealable
name: dax-skill-citizen-prealable
description: "Gate anti-doublon : avant tout script inline ou commande système, interroge DAX (table entities, entity_type='SKILL', status='active') pour vérifier qu'aucun skill canonique existant ne couvre déjà le besoin. Si un skill actif existe, bloque le script inline et invoque le skill canonique via le registre central L4-TOOLS/SKILLS."
trigger: skill_citizen_prealable
anti_triggers: []
gericode_version: "1.0"
stratum: L4-TOOLS
shard_id: G
turn_counter: 1
uuid: dax-skill-citizen-prealable-001
timestamp: "2026-11-26T19:36:00Z"
invariants:
  friction: 0.0
  entropy: 0.0
wal_reference: "WAL-0x243-DAX-SKILL-CITIZEN-PREALABLE-001"
---

# dax-skill-citizen-prealable

## Objectif

Interdire la génération de scripts inline (Python, PowerShell, Bash, Zig) et le lancement de processus résidents ad hoc quand un Skill ou un Citizen existe déjà pour le même besoin dans l'écosystème gerivdb. Les Skills et Citizens sont les unités canoniques d'automatisation et de processus résident ; tout contournement crée de la dette technique, des processus zombies et de la perte de traçabilité.

Ce skill implémente le gate technique de la règle `skill-citizen-prealable` en s'appuyant sur **DAX** (Registre des Registres, strate L1-INFRA) comme couche de vérification tabulaire, en complément du registre central `L4-TOOLS/SKILLS` (`skills-index.json`).

## Déclencheur

Avant tout script inline (Python, PowerShell, Bash, Zig) ou toute commande système :

1. Interroger DAX (`skills_database.db`, table `entities` WHERE `entity_type='SKILL'` AND `status='active'`)
2. Consulter `skills-index.json` de `L4-TOOLS/SKILLS` (registre canonique, source de vérité)
3. Chercher un Skill couvrant le besoin exprimé (par `name`, `intent_hash`, ou `triggers`)
4. Si un Skill existe avec statut `active` → invoquer le skill canonique, interdiction du script inline
5. Si aucun Skill n'existe → créer un Skill suivant le format canonique

## Protocole obligatoire

### 1. Vérification Skill préalable (obligatoire)

Exécuter le script de vérification :

```powershell
python .kilocode/skills/dax-skill-citizen-prealable/check_skill.py --need "<besoin>" --dax-db "D:\DO\WEB\TOOLS\L1-INFRA\DAX\data\skills_database.db" --skills-index "D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\skills-index.json"
```

Le script retourne :
- `EXISTING_SKILL:<nom>` si un skill actif couvre le besoin → bloquer le script inline, invoquer ce skill
- `NO_ACTIVE_SKILL` si aucun skill actif ne couvre le besoin → autoriser la création d'un nouveau skill

### 2. Vérification Citizen préalable (obligatoire)

Avant tout lancement de processus résident (daemon, worker, consumer, bridge) :

1. Consulter `L3-CITIZENS/VEX/vex.yaml` et la table `citizens` de DAX
2. Chercher un Citizen couvrant le besoin (par `name`, `command`, `working_dir`)
3. Si un Citizen existe avec statut `active` → l'invoquer via vex.yaml, interdiction du processus ad hoc
4. Si aucun Citizen n'existe → l'inscrire dans vex.yaml suivant le format canonique

### 3. Concepts et anticoncepts ontologiques

| Concept | Description |
|---------|-------------|
| Skill canonique | Unité d'automatisation réutilisable, déclarée dans skills-index.json (L4-TOOLS) et indexée dans DAX (entities.entity_type='SKILL'), statut 'active', avec frontmatter (intent_hash, triggers, anti_triggers, version) |
| Citizen canonique | Processus résident déclaratif, inscrit dans vex.yaml (L3-CITIZENS/VEX) et indexé dans DAX, statut 'active', avec contrat (name, type, command, working_dir, restart_policy, health_check, lock_file, log_file) |

| Anticoncept | Description |
|-------------|-------------|
| Script inline sans Skill | Script généré alors qu'un Skill existe pour le même besoin (détecté par ce gate) |
| Processus résident ad hoc | Processus lancé manuellement alors qu'un Citizen existe pour le même besoin |

### 4. Preuve d'usage

Avant tout commit résultant d'une opération Skill ou Citizen, produire :

- Le nom du Skill/Citizen invoqué
- Le hash SHA-256 du résultat
- Le code de retour (exit code)
- L'enregistrement dans le WAL (WAL-0x243) et dans la table `entity_usage_log` de DAX

## Contrat de sortie

Chaque opération d'automatisation doit être accompagnée de :

```
[DAX_SKILL_CITIZEN_CHECK] type=<SKILL|CITIZEN|INLINE|AD_HOC> nom=<NOM> existant=<OUI|NON> invoque=<OUI|NON> wal_hash=<SHA256>
```

Si `existant=OUI` et `invoque=NON` (script inline ou processus ad hoc malgré un Skill/Citizen existant) → **BLOQUER**.

## Antipatterns bloqués

- Générer un script inline sans avoir d'abord consulté DAX et skills-index.json
- Créer un skill dans `.kilocode/skills/` dont le nom existe déjà avec statut `active` en L4-TOOLS / DAX
- Lancer un processus résident sans déclaration VEX préalable ni inscription dans DAX
- Invoquer un skill sans enregistrement de preuve d'exécution (hash SHA-256, UTC, exit code)

## Fichiers de référence

- Script de vérification : `.kilocode/skills/dax-skill-citizen-prealable/check_skill.py`
- Règle parente : `.kilocode/rules/skill-citizen-prealable.md`
- Registre central : `D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\skills-index.json`
- Registre tabulaire : `D:\DO\WEB\TOOLS\L1-INFRA\DAX\data\skills_database.db` (table `entities`)
- Design Skill : `gerivdb/SKILLS/designs/skill-ontology/design.yaml`
- IntentHash : 0xDAX_SKILL_CITIZEN_PREALABLE_20261126
- WAL : WAL-0x243-DAX-SKILL-CITIZEN-PREALABLE-001
