---
name: task-automator
description: "Windows Task Scheduler, schtasks, polling automation. Use when user mentions 'Task Scheduler', 'schtasks', 'polling'."
---
|

# task-automator
|
# Task Automator

## Domaine et périmètre

Ce skill couvre l'**automatisation de tâches Windows** :
- Windows Task Scheduler (planification de scripts PowerShell)
- `schtasks` (création, modification, suppression de tâches)
- Polling automation (vérification périodique de dépôts, CI, health)
- Intégration avec KIVA-CLI pour la CI locale sur Z600

## Méthodologie

### Phase 1 : Identification de la tâche
- Déterminer la fréquence (horaire, quotidienne, hebdomadaire, au démarrage).
- Identifier le script ou la commande à exécuter.
- Vérifier les prérequis (permissions, chemins, variables d'environnement).

### Phase 2 : Création de la tâche
- Utiliser `schtasks` ou le module PowerShell `ScheduledTasks`.
- Configurer le déclencheur (trigger), l'action, et les conditions.
- Tester la tâche manuellement avant de la planifier.

### Phase 3 : Monitoring
- Vérifier l'historique d'exécution (`schtasks /query /v`).
- Configurer les notifications en cas d'échec.
- Maintenir un registre des tâches actives.

## Règles de décision
- **Règle 1** : Les tâches de polling doivent respecter un intervalle minimum de 15 minutes.
- **Règle 2** : Les scripts doivent être idempotents (pas d'effet de bord si relancés).
- **Règle 3** : Les tâches critiques (health-check, backup) doivent avoir une notification d'échec.

## Format de sortie

```markdown
## Tâche Planifiée
- Nom : [nom]
- Fréquence : [description]
- Commande : `[commande]`
- Statut : [activée | désactivée]
- Dernier run : [date | jamais]
```

## Exemples d'utilisation
- "Planifie un health-check toutes les heures" → Créer la tâche.
- "Liste les tâches actives" → `schtasks /query /v`.
- "Crée un polling GitHub API toutes les 30 min" → Configurer.

## Intégration avec l'écosystème
- Dépôts concernés : KIVA-CLI, DevTools
- Couche EECS : L4_ORCHESTRATION
- Tags NEXUS : [CONFORME_NEXUS]

