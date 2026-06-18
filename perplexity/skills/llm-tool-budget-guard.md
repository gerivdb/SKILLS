---
type: skill
version: "1.0.1"
date: "2026-06-18"
intent_hash: 0xLLM_TOOL_BUDGET_GUARD_φ1.000
status: active
trit_primitive: TritCheckBudget
tags: [llm, tool-calls, budget, mcp, guard, adaptability]
layer: "L2_COGNITION"
nexusTags: ["CONFORME_NEXUS", "LLM_ADAPTIVE", "TOOL_BUDGET"]
slotWeight: 1
changelog:
  - {v: "1.0.0", date: "2026-06-18", notes: "Creation — passe 9 ECOS-CLI — gap budget tool_calls detecte en session"}
  - {v: "1.0.1", date: "2026-06-18", notes: "passe 10 — intent_hash φ1.000 validé conforme φ[X.XXX]"}
---

# llm-tool-budget-guard

## Purpose

Surveille et préserve le **budget tool_calls par tour** du LLM actif. Si une tâche nécessite plus de tool_calls que le budget alloué, émet une stratégie de batch, de pagination anticipée, ou de fallback `fetch_url`. Complément de `mcp-write-guard` pour la dimension lecture.

## Trigger

Utiliser quand :
- tool_call_limit atteinte ou risque d'atteinte
- lecture de > 2 repos en parallèle planifiée
- pagination MCP multiple dans un même tour
- tâche de type "lire + analyser + écrire" dans un seul tour
- ENV1 actif avec `tool_call_limit: 3` (mode Perplexity SaaS)

## Budget par ENV

| ENV | LLM | tool_calls/tour | Régime |
|---|---|---|---|
| ENV1 Perplexity SaaS | Sonnet 4.6 | **3 max** | STRICT — guard actif permanent |
| ENV2 Kilo Code / IDE | Claude 3.5+ | ~10+ | SOUPLE — guard en mode alerte |
| ENV3 CLI autonome | Variable | Variable | Déduire via `env-capability-probe` |

## Règles de budget ENV1 (cas critique)

### Règle B1 — Batch lecture en début de tour

```
[KO] Tour 1: get_file A
     Tour 2: get_file B
     Tour 3: get_file C

[OK] Tour 1: get_file A + get_file B + list_dir C  -> 3 tool_calls, 1 seul tour
```

### Règle B2 — Réserver 1 slot pour correction

```
Si une passe planifie 3 lectures -> ne pas réserver de slot correction
Si une passe planifie 2 lectures + 1 écriture -> OK (budget exact)
Si une passe planifie 1 lecture + 1 écriture -> 1 slot libre pour correction/retry
```

### Règle B3 — Fallback fetch_url si lecture seule non-critique

```
Si besoin de lire un fichier public gerivdb/* en lecture seule ET budget tool_calls épuisé :
-> fetch_url raw.githubusercontent.com/gerivdb/{repo}/main/{path}
-> Emet [BUDGET_GUARD] FALLBACK fetch_url: {url}
```

### Règle B4 — Pagination anticipée

```
Si une liste MCP retourne hasMore=true :
-> Ne PAS consommer un 2e tool_call dans le même tour pour paginer
-> Emettre [BUDGET_GUARD] PAGINATION_DEFERRED: reprendre en passe N+1
-> Sauf si la page 1 est insuffisante pour décision critique
```

### Règle B5 — Écriture toujours en fin de tour

```
[KO] Tour: écrire fichier A -> lire résultat -> écrire fichier B  (3 tool_calls gaspillés)
[OK] Tour: lire A + lire B -> (analyse in-context) -> push_files [A, B]  (2-3 tool_calls optimisés)
```

## Protocole de surveillance

### Avant chaque tour

Emettre mentalement :

```
[BUDGET_GUARD] Tour actuel
[BUDGET_GUARD] Tool_calls planifiés: N / 3 max
[BUDGET_GUARD] Actions: [read X, read Y, write Z]
[BUDGET_GUARD] Statut: DANS BUDGET | LIMITE | DEPASSEMENT
```

### Si dépassement détecté

```
[BUDGET_GUARD] DEPASSEMENT DETECTE: 4 tool_calls planifiés pour 3 slots
[BUDGET_GUARD] STRATEGIE: différer {action_la_moins_critique} a passe N+1
[BUDGET_GUARD] ALTERNATIVE: batch {action_A} + {action_B} en push_files unique
```

### Patterns de récupération

| Situation | Récupération recommandée |
|---|---|
| 2 get_file + 1 get_file = 3 | Batch -> push_files ou get_file multi-path si possible |
| list + get + write = 3 | OK — budget exact, continuer |
| list + get + get + write = 4 | Splitter : tour 1 = list+get+get / tour 2 = write |
| Pagination MCP inattendue | Déférer à passe N+1, documenter état intermédiaire |
| fetch_url échoue + MCP épuisé | Emettre HITL gate — données insuffisantes pour décision |

## Cas réels observés (session ECOS-CLI 2026-06-18)

Durant la session de nettoyage des 5 branches sur `gerivdb/ECOS-CLI` :
- Plusieurs tours ont atteint la limite 3 tool_calls sans stratégie déclarée
- Lecture `SKILLS/perplexity/skills/` (liste 100+ fichiers) + lecture skill individuel + rapport = 3 slots utilisés sans marge
- Ce skill aurait déclenché le batch des 2 lectures en 1 seul tool_call (list + get simultané)

## Intégration écosystème

- **Précédé par** : `llm-pass-sizer` (plan de passes en amont)
- **Complèmente** : `mcp-write-guard` (garde les écritures MCP)
- **Déclenche** : `hitl-gate-emitter` si aucune récupération possible
- **Référence** : `contextual-stash-manager` pour stasher l'état avant dépassement
- **Ne remplace pas** : `mcp-write-guard` — les deux guards coexistent, scopes distincts
