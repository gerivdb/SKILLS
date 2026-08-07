---
name: close-loop-detector
description: "Détecte la fin d'une session et les boucles sémantiques dans l'écosystème"
version: "1.0.0"
layer: "L4_TRANSVERSAL"
nexusTags: ["SYSTEME", "AUTOMATISATION", "DIAGNOSTIC"]
slotWeight: 1
status: "active"
intent_hash: 0xCLOSE_LOOP_DETECTOR_20260730
scope: ecosystem
guards:
  - agent-budget-check
  - mdu-session-validation
---

# close-loop-detector — Détecteur de boucle sémantique et clôture de session

## Déclencheur
- Commande explicite : `close-loop-detector` ou via le pattern-router avec les mots-clés  
  `"détecter boucle sémantique"`, `"boucle sémantique"`, `"est-ce fini ?"`, `"fermer session"`  
- Peut aussi être invoqué automatiquement à la fin de chaque session via le trigger `session-closeout` (D5).

## Fonctionnement

| Étape | Description |
|------|------------|
| **1. Lecture du contexte** | Interroge : <br>• `INTENT_HASH` courant (via `kilo recall`) <br>• `CHECKPOINT_MDU` (via `gitmcp read --path .kiva/checkpoint`) <br>• Historique des commandes (`gitmcp exec --script "log-commands"`) |
| **2. Analyse de similarité** | Compare l'IntentHash actuel avec les N hashes précédents : <br>• < 5 % de différence → possible loop <br>• Identique → déjà vu <br>• Répétition de mots-clés critiques (`review résoud PR`, `review et merge PR`, `résoud PR`) |
| **3. Convergence des réponses** | Si la réponse du LLM aux dernières 3-5 requêtes est quasi-identique (> 90 % de tokens partagés) → indique stagnation. |
| **4. Vérification de l'état terminal** | Confirme que : <br>• `git status` → `working tree clean` <br>• `git branch --merged` → toutes les branches de feature mergées <br>• Aucun fichier non-tracké (`git ls-files --others --exclude-standard` vide) |
| **5. Décision** | - **BOUCLE DÉTECTÉE** → Retourne `STOP` + rapport détaillé. <br>- **AUCUNE BOUCLE** → Retourne `CONTINUE` + métriques de loop-score (0 = pas de loop, 1 = possible loop). |

## Output (JSON)

```json
{
  "result": "STOP|CONTINUE",
  "loop_score": 0.0-1.0,
  "reason": "string",
  "metrics": {
    "hash_similarity": 0.0-1.0,
    "command_repeat_rate": 0.0-1.0,
    "response_overlap": 0.0-1.0
  },
  "session_state": {
    "working_tree_clean": true,
    "all_prs_merged": true,
    "checkpoint_valid": true
  }
}
```

## Exemple d'utilisation

```bash
# 1️⃣ Détection manuelle
close-loop-detector

# 2️⃣ Détection automatiques à chaque session-closeout
# (automatiquement invoqué par le trigger session-closeout si les guards le souhaitent)

# 3️⃣ Forcer la clôture (si loop détecté)
close session --force
```

## Guards obligatoires

| Guard | Rôle |
|-------|------|
| `agent-budget-check` | S'assure qu'il reste assez de RAM/CPU pour lancer l'analyse. |
| `mdu-session-validation` | Vérifie que le checkpoint MDU est valide avant de considérer la session "terminal". |

## Integration points

| Point d'intégration | Fichier / Emplacement |
|---------------------|-----------------------|
| **Pattern-router** | Ajout de la ligne : <br>`| "detect close-loop", "boucle sémantique", "est-ce fini ?" | **close-loop-detector** (skill universel) |` |
| **Session-closeout (D5)** | Le trigger appelle automatiquement `close-loop-detector` avant de marquer la session comme terminée. |
| **Skill-registry** | Le skill possède son propre entrée `close-loop-detector` dans `REGISTRY.yaml` (ajout automatique via `registry-gen.py`). |

## Validation & Tests

| Test | Description |
|------|------------|
| **Unit-test** | Simuler 3 sessionsSuccessives avec identiques IntentHash → vérifier que `loop_score` > 0.8 et `result="STOP"`. |
| **Integration** | Lancer `close-loop-detector` après un `review résoud PR` complet : doit retourner `CONTINUE` si tout est propre, `STOP` si boucle détectée. |
| **Performance** | Le mécanisme doit s'exécuter en ≤ 2 s sur hardware Z600 (pas de parsing lourd). |