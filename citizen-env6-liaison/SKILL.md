---
name: citizen-env6-liaison
description: Processus citoyen persistant sous VEX : maintient le canal ENV3→ENV6 ouvert, surveille les nouveaux messages ENV6 et alerte ENV3.
---
# citizen-env6-liaison

## Rôle
Processus léger persistant qui maintient le canal ENV3→ENV6 ouvert via CDP (port 9222), vérifie périodiquement les nouveaux messages entrants dans la conversation `df87f8dd-8998-4279-bcd7-b667932e959c`, et alerte ENV3 quand ENV6 répond.

## Pourquoi ce citizen est nécessaire
Aucun processus ne maintient actuellement le canal ENV6 ouvert entre les sessions. Les transmissions précédentes étaient des one-shot sans suivi de réponse. ENV6 peut répondre à tout moment ; sans citizen, la réponse est manquée.

## Rôles et responsabilités
1. **Maintenir le canal ouvert** : connexion CDP persistante à `http://127.0.0.1:9222`.
2. **Surveiller la conversation cible** : `df87f8dd-8998-4279-bcd7-b667932e959c`.
3. **Détecter les nouveaux messages** : comparaison de hash des messages vus vs nouveaux.
4. **Alerter ENV3** : quand un nouveau message d'ENV6 est détecté, notifier (log + fichier d'alerte `e2e_output/env6-liaison-alert.jsonl`).
5. **Rate-limit explicite** : intervalle configurable (défaut 30 s).
6. **Critère d'alerte strict** : nouveau message entrant uniquement, pas de heartbeat, pas de bruit système.

## Dépendances
- Skill `env6-communication-verified` (cycle L3 : envoi → vérif DOM → attente réponse → relecture).
- Skill `env6-dom-probe` (vérification de présence dans le DOM).
- Skill `cdp-react-input` (injection dans React via `page.keyboard.type`).
- Skill `adversarial-assertion-gate` (rejet des faux positifs).

## Contrat de sortie
Écriture dans `e2e_output/env6-liaison-alert.jsonl` :
```json
{"ts": "...", "shard": "A", "role": "assistant", "hash": "...", "text": "..."}
```

## Statut
Déclaré sous VEX via `config/vex/vex_shard_a_consumer.yaml`. Auto-start en attente de validation HITL.

## Antipatterns bloqués
- Polling fréquent sans rate-limit (recrée le bruit E4).
- Alerte sur heartbeat ou bruit système.
- Muter le fichier de registre SOT sans bail de gouvernance.