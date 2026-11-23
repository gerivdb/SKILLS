---
name: vex-citizen-enroller
description: Procédure de déclaration d'un daemon de shard (consumer, worker) sous vex.yaml (L3-CITIZENS/VEX), éliminant définitivement les boucles de spawn PowerShell ad hoc et les processus zombies.
---
# vex-citizen-enroller

## Rôle
Enrôler tout processus résident (consumer, worker, bridge, daemon) sous le citoyen VEX (`D:\DO\WEB\TOOLS\L3-CITIZENS\VEX\vex.yaml`), afin qu'il soit supervisé, supervisable et auto-redémarré. Interdit le lancement sauvage en terminal interactif sans déclaration VEX.

## Cause racine
Les daemons lancés manuellement via `python scripts/shard_a_consumer.py` créent des processus orphelins (8 instances `shard_a_consumer.py` trouvées simultanément), des verrous `.kilo/locks/consumer_A.lock` orphelins, et aucune supervision de santé.

## Contrat obligatoire

### 1. Todo fichier VEX avant lancement
Tout processus résident doit avoir une entrée dans [`vex.yaml`](file:///D:\DO\WEB\TOOLS\L3-CITIZENS\VEX\vex.yaml) avec :
- `name` : nom du citoyen (ex: `env3-shard-a-consumer`)
- `type` : `citizen`
- `command` : commande de lancement
- `working_dir` : répertoire de travail
- `auto_start` : true/false
- `restart_policy` : `on-failure` ou `always`
- `max_restarts` : nombre max de redémarrages
- `health_check` : commande ou fichier de health check
- `lock_file` : chemin du verrou (ex: `.kilo/locks/consumer_A.lock`)
- `log_file` : chemin du fichier de logs

### 2. Procédure d'enrôlement
1. Créer l'entrée YAML dans `vex.yaml`.
2. Tester le lancement manuel.
3. Activer `auto_start: true` après validation.
4. Le citizen `CITIZEN-ENV6-LIAISON` surveille le cycle de vie.

### 3. Purge des processus orphelins
Avant tout lancement, vérifier qu'aucune instance orpheline du même processus ne tourne (ps -f | grep). Tuer les orphelins avant de redémarrer sous VEX.

## Critères de succès
- Aucun processus `shard_a_consumer.py` lancé hors déclaration VEX.
- Au plus une instance active par nom de citizen.
- Tout processus résident a un verrou associé et un fichier de log.

## Antipatterns bloqués
- `python scripts/shard_a_consumer.py` lancé manuellement sans déclaration VEX.
- Plusieurs instances du même consumer simultanées.
- Verrou `.kilo/locks/consumer_A.lock` orphelin sans processus détenteur vivant.