---
type: skill
version: "1.0.0"
status: active
intent_hash: 0xSKILL_M3_TEST_TEMPLATE_INJECTOR_20261119
---

# skill.m3.test-template-injector — Génération de templates de tests d'intégration

## Objectif

Générer un fichier de test d'intégration standardisé (`test_*.py`) à partir d'un template éprouvé, adapté à un module client spécifique (classe, factory, endpoint, nom de module).

Ce skill est le deuxième maillon de la chaîne autopoïétique : il produit des fichiers de test prêts à être exécutés, basés sur le template validé de `ROOTX/src/test_causal_validator.py`.

## Déclencheur

Toute demande de génération de tests d'intégration pour un module client HTTP existant, ou toute exécution planifiée après détection d'un nouveau client sans test associé.

## Règles obligatoires

### 1. Entrée unique
Le skill reçoit les paramètres suivants :
- `module_name` : nom du module client (ex: `curriculum_validator`)
- `factory_name` : nom de la fonction factory (ex: `build_curriculum_validator`)
- `class_name` : nom de la classe principale (ex: `CurriculumValidator`)
- `endpoint_port` : port du serveur MVP (ex: `8040`)
- `depot` : nom du dépôt cible (ex: `RLM-CONFIG`)

### 2. Template éprouvé (ZCF-0.0)
Le fichier généré doit être basé sur le template éprouvé de `ROOTX/src/test_causal_validator.py` avec les substitutions suivantes :
- `CausalValidator` → `class_name`
- `build_causalvalidator` → `factory_name`
- `validate_causal` → méthode de validation du module
- `8030` → `endpoint_port`
- Nom du fichier : `test_<module_name>.py`

### 3. Zéro dépendance externe
Le test généré utilise exclusivement `unittest`, `sys`, `os`, `urllib` (stdlib uniquement).

### 4. Trois scénarios couverts
Chaque test généré doit couvrir :
1. `test_health_ok` : vérifie que le serveur MVP répond `{"status": "ok"}`
2. `test_<méthode>_success` : flux nominal avec payload de test
3. `test_<méthode>_connection_refused` : résilience face à un serveur injoignable (port faux)

### 4. Emplacement de sortie
Le fichier est écrit dans `<depot>/src/test_<module_name>.py`.

## Contrat de sortie

Le skill produit un fichier `test_<module_name>.py` contenant :
- Imports stdlib uniquement
- Classe `Test<Classe>Integration(unittest.TestCase)`
- Méthode `setUp` pointant vers l'endpoint MVP
- 3 méthodes de test (health, succès, connexion refusée)
- Bloc `if __name__ == '__main__': unittest.main(verbosity=2)`

## Antipatterns bloqués

- Ne jamais générer de code avec des dépendances externes (pip, requests, etc.).
- Ne jamais modifier le code source du module client (il est déjà fonctionnel).
- Ne jamais regrouper plusieurs tests dans un seul fichier (un fichier = un module).
- Ne jamais committer automatiquement (réservé à l'orchestrateur).

## Fichier de référence

- Template : `D:\DO\WEB\TOOLS\L4-TOOLS\ROOTX\src\test_causal_validator.py`
- Skill consommateur : `citizen.test-generator` (à créer)

## Référence ADR

- **ADR** : ADR-2026-11-19-001-autopoietic-stub-eradication
- **IntentHash** : 0xAUTOPOIETIC_STUB_ERADICATION_20261119
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed
