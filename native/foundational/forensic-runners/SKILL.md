---
name: forensic-runners
description: Implémente et orchestre les runners forensiques (ROOTX, RLM-243, TLM-LANG, TIMX, SPIDX, LLUX) pour Agent Manager V9.9. Utilise ce skill quand tu dois déployer, tester, ou invoquer les runners forensiques dans une investigation causale.
version: 1.0.0
intent_hash: 0xSKILL_FORENSIC_RUNNERS_20260810
---

# Forensic Runners

## Objectif
Orchestrer les 6 runners forensiques pour enrichir les missions Agent Manager avec :
- ROOTX : inference causale + trace
- RLM-243 : raisonnement symbolique
- TLM-LANG : normalisation sémantique
- TIMX : index temporel
- SPIDX : recherche sémantique
- LLUX : lookup de contexte

## Déclencheur
- Toute mission de type `forensic_investigation`
- Toute mission de type `causal_analysis`
- Toute mission de type `ontological_check`
- Toute mission de type `temporal_analysis`

## Protocole

### 1. Démarrer les runners
```powershell
# Démarrer tous les runners
.\kilo\orchestrator\runners\start-forensic-runners.ps1

# Arrêter tous les runners
.\kilo\orchestrator\runners\start-forensic-runners.ps1 -Stop
```

### 2. Vérifier la santé
```powershell
# Vérifier que les ports sont ouverts
Get-NetTCPConnection -LocalPort 8810,8811,8812,8813,8814,8815 -ErrorAction SilentlyContinue
```

### 3. Invoquer un runner
```powershell
# Via cognitive-runners-interface.ps1
.\kilo\orchestrator\cognitive-runners-interface.ps1 -MissionId MISSION-001 -RunnerType rootx -Payload $payload
```

### 4. Mapping mission_type → runners
| mission_type | runners |
|---|---|
| forensic_investigation | rootx, rlm-243, timx |
| causal_analysis | rootx, timx |
| ontological_check | rootx, tlm-lang |
| temporal_analysis | timx, rlm-243 |
| semantic_search | spidx, llux |

## Endpoints

| Runner | Port | Endpoint |
|--------|------|----------|
| ROOTX | 8810 | POST /causal/infer/ |
| RLM-243 | 8811 | POST /symbolic/reason/ |
| TLM-LANG | 8812 | POST /lang/normalize/ |
| TIMX | 8813 | POST /temporal/index/ |
| SPIDX | 8814 | POST /semantic/search/ |
| LLUX | 8815 | POST /lookup/context/ |

## Anti-patterns bloquants
- Invoquer un runner sans vérifier qu'il est démarré
- Utiliser les stubs factices de l'ancienne interface
- Ignorer le mode dégradé si un runner est indisponible
- Oublier de logger dans WAL NEXUS

## Référence ADR
- **ADR** : ADR-2026-08-10-009-FORENSIC_RUNNERS
- **IntentHash** : 0xSKILL_FORENSIC_RUNNERS_20260810
- **Dépôt** : gerivdb/GeriCode
- **Statut ADR** : proposed
