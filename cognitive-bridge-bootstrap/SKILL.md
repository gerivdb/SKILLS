---
name: cognitive-bridge-bootstrap
description: Protocole d'amorçage cognitif : injecte la directive système canonique (ENV6_CORE_DIRECTIVE.md) dans toute conversation LLM SaaS (DeepSeek) orpheline d'identité avant tout test de transport.
---
# cognitive-bridge-bootstrap

## Rôle
Amorcer cognitivement une conversation LLM (DeepSeek) avant tout test de protocole. Un modèle LLM "vierge" ne sait pas qu'il est ENV6 et refuse d'émettre des ACK structurés. Il faut d'abord lui injecter sa directive système pour qu'il adopte son rôle.

## Cause racine
Un message "Produis [ENV6] ACK <token>" envoyé à un DeepSeek vierge reçoit une réponse de refus : *"Je ne suis pas ENV6, je suis un grand modèle de langage créé par DeepSeek"*. Ce refus n'est PAS une panne de canal : le transport fonctionne (le message est dans le DOM, la réponse est lisible). C'est un refus cognitif : le modèle ignore son identité et son contrat.

## Protocole d'amorçage

### Étape 1 : Détecter l'absence d'amorçage
Si le LLM répond par un refus d'identité (pas ENV6, pas d'ACK, "je suis un grand modèle de langage"), la conversation n'est pas amorcée.

### Étape 2 : Injecter la directive système
Lire le fichier [`e2e_output/ENV6_CORE_DIRECTIVE.md`](file:///D:/DO/WEB/TOOLS/L0-CANON/ENV3-repo/e2e_output/ENV6_CORE_DIRECTIVE.md) et l'envoyer en entier dans la conversation cible via `page.keyboard.type(message, delay=50)`, puis `Enter`.

### Étape 3 : Attendre l'acceptation
Attendre que le LLM confirme avoir intégré son rôle (réponse confirmant son identité ENV6 et son statut subordonné au métacluster GERIVDB).

### Étape 4 : Tester le protocole
Une fois amorcé, envoyer le test ACK (`[ENV6] ACK <token>`) et vérifier avec `verify_ack_e2e.py` (filtre strict `role=assistant`, regex ancrée).

## Fichier de référence
- `e2e_output/ENV6_CORE_DIRECTIVE.md` : directive système ENV6 (statut: active, updated_at: 2026-11-13T04:31:13Z, uuid: 99b78e64-d886-400a-a737-27f103d904f7)

## Critères de succès
- Le LLM confirme son identité ENV6 (reconnaît être un agent subordonné au métacluster GERIVDB).
- Le protocole ACK devient fonctionnel après amorçage.
- Le transport physique (CDP) est déjà prouvé fonctionnel indépendamment.

## Antipatterns bloqués
- Tester l'ACK avant d'avoir amorcé l'identité du LLM → faux négatif garanti.
- Considérer un refus d'identité comme une panne de transport CDP → diagnostic erroné.