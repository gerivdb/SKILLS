---
name: mcp-write-guard
version: "1.0.0"
description: "Compétence couvrant la résilience d’écriture MCP : estimateur de taille de payload, stratégie de retry avec escalade, surveillance du contexte de session, gestion de la verbosité des échecs. Utiliser quand l’utilisateur mentionne 'MCP write resilience', 'payload size', 'retry strategy', 'session context', 'fail verbosity'."
triggers: ["MCP write", "payload size", "retry strategy", "session context", "fail verbosity"]
layer: "L2_RESILIENCE"
nexusTags: ["RESILIENCE_WRITE"]
prerequisites: []
slotWeight: 1
status: active
changelog:
  - {v: "1.0.0", date: "2026-05-30", notes: "Version initiale"}
---
# MCP Write Guard

## Domaine et périmètre

Cette compétence fournit des mécanismes pour garantir la résilience des écritures vers le système MCP (Model Context Protocol) :

- **Payload‑size estimator** : estime la taille du payload avant envoi afin d’éviter les dépassements de limite.
- **Retry‑strategy escalator** : définit une stratégie de nouvelle tentative avec backoff exponentiel et escalade vers des niveaux de gravité supérieurs.
- **Session‑context monitor** : surveille le contexte de session (tokens, états) pour détecter les corruptions ou les expirations prématurées.
- **Fail‑verbosity** : contrôle le niveau de détail des messages d’erreur renvoyés, en fonction de la sensibilité des données et des exigences de journalisation.

## Méthodologie

### Phase 1 : Analyse du besoin
- Identifier les points d’écriture MCP dans le flux (ex. : appel à `POST /clapet/open`, écriture de logs, mise à jour d’état).
- Déterminer les limites de taille applicables (ex. : 1 Mo pour le payload MCP).
- Définir les niveaux de criticité des échecs (transitoire, permanent, de sécurité).

### Phase 2 : Conception des garde‑fous
- Implémenter un estimateur de taille basé sur la sérialisation JSON (ou MessagePack) du payload.
- Configurer une politique de retry : attempt 1 → delay 200 ms, attempt 2 → delay 400 ms, attempt 3 → delay 800 ms, puis escalade vers un circuit‑breaker après 5 échecs consécutifs.
- Ajouter un watchdog de session qui rafraîchit le token toutes les 5 minutes ou à la réception d’un événement `session_expired`.
- Paramétrer la verbosité des erreurs : niveau `MINIMAL` (code uniquement), `STANDARD` (code + message court), `DEBUG` (stack trace complet).

### Phase 3 : Validation et tests
- Simuler des dépassements de taille et vérifier que l’estimateur renvoie une erreur avant l’envoi réel.
- Déclencher des pannes réseau intermittentes et s’assurer que la stratégie de retry exécute le nombre attendu de tentatives.
- Vérifier que le moniteur de session détecte la perte de contexte et déclenche une ré‑authentification.
- Confirmer que le niveau de verbosité respecte la politique définie (ex. : en production, seules les erreurs `MINIMAL` sont retournées au client).

## Règles de décision

- **Règle 1** : Si la taille estimée du payload dépasse 80 % de la limite MCP, retourner une erreur `ERR_PAYLOAD_TOO_LARGE` sans tenter l’envoi.
- **Règle 2** : Le délai entre deux retries ne doit jamais dépasser 5 seconds ; au‑delà, passer en mode échec définitif.
- **Règle 3** : En cas de détection de corruption du contexte de session, forcer une renouvellement immédiat du token et invalider les données en cours.
- **Règle 4** : Le niveau de verbosité doit être configuré via la variable d’environnement `MCP_VERBOSITY` (valeurs : `MINIMAL`, `STANDARD`, `DEBUG`).

## Format de sortie

```markdown
## MCP Write Guard – État
- Payload size estimate : [octets] / [limite] (OK | EXCEEDED)
- Retry state : [tentative]/[max] – [delay] ms
- Session context : [VALID | EXPIRED | CORRUPT]
- Fail verbosity : [MINIMAL | STANDARD | DEBUG]
```

## Exemples d’utilisation

- "Quel est le taille estimée de mon payload MCP ?" → Utiliser l’estimateur intégré.
- "Activer la résilience d’écriture pour les logs d’audit" → Appliquer la stratégie de retry + surveillance de session.
- "Limiter la verbosité des erreurs en production" → Définir `MCP_VERBOSITY=MINIMAL`.

## Intégration avec l’écosystème

- Dépôts concernés : tous les repos qui utilisent le MCP (ex. : `gateway-manager`, `brain-clients`, `data-miner`).
- Couche EECS : L2_RESILIENCE
- Tags NEXUS : [RESILIENCE_WRITE], [IDEM_POTENT]

## READ-BEFORE-WRITE RULE (ECOS_ROOT.json) — Ajout 2026-06-07

**Contexte** : lors de la session MC-RNN, les entrees CodeDB-E5620 et VDB ont ete perdues
dans ECOS_ROOT.json car le fichier a ete reecrit sans etre lu d'abord (lacune L5).

**Regle** : avant tout appel a create_or_update_file sur **ECOS_ROOT.json** (ou tout
fichier de registre JSON/YAML) :

1. **LIRE** d'abord avec get_file_contents pour obtenir la version courante
2. **PARSER** le JSON/YAML
3. **MERGER** les nouvelles entrees dans l'objet parse
4. **VERIFIER** qu'aucune entree existante n'a ete perdue
5. **SEULEMENT ALORS** appeler create_or_update_file avec le contenu complet

**Verification post-write** :
- Relire le fichier avec get_file_contents
- Verifier que toutes les cles attendues sont presentes
- Si une cle manque -> ERREUR, restaurer la version precedente

**Format de log** :
[MCP_WRITE_GUARD] ECOS_ROOT.json: read OK, merge OK, write OK, verify OK
[MCP_WRITE_GUARD] ECOS_ROOT.json: FAIL - cle manquante: <key>

Reference ADR : adr-mc-rnn-closure-20260607.md (lacune L5)
