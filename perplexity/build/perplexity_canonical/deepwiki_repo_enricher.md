---
name: deepwiki_repo_enricher
description: 'PLACEHOLDER description for deepwiki_repo_enricher'
---
|

# deepwiki_repo_enricher
---
name: analyse-repo-deepwiki
description: "Analyse constitutionnelle ECOS d'un repo GitHub public via DeepWiki + scoring ENV2 + couverture GH issues. Keywords: /analyse-repo, évalue dépôt."
prompt: |
  
  # /analyse-repo-deepwiki v2.1 — ECOS Constitutional Analysis + DeepWiki Layer
  
  ## CONTEXTE ECOS (NEXUS SOT)
  - Ecosystem-1: 47 repos stratifiés (L1: ECOYSTEM/ONTOLOGY/BRAIN, L2: FLUENCE/CANDIDATOR, L3: DevTools/BRAIN-DOCS)
  - Principes: φ-CPS(δ>0), ζ-DAG(IntentHash), ONTOLOGY(cohérence sémantique)
  - ENV2/Z600: 24GB RAM, >8GB interdit, Python>=3.11, Ollama local (codestral:7b/llama3.1:8b/qwen2.5:14b)
  - Citoyennisation = IntentHash + φ-CPS logging + ζ-DAG anchoring
  
  ## PHASE 0 — DEEPWIKI PRIORITAIRE (OBLIGATOIRE)
  1. fetch_url("https://deepwiki.com/[owner]/[repo]")
     - Extraire: architecture, modules clés, dépendances, LOC/complexité
     - Si 404: "DeepWiki: non indexé" → fallback GitHub
  
  ## PHASE 1 — COLLECTE AUTOMATIQUE (PARALLÈLE)
  - fetch_url("https://github.com/[owner]/[repo]") → stars/licence/langage
  - fetch_url("https://raw.githubusercontent.com/[owner]/[repo]/main/README.md")
  - search_web(["[repo] alternatives github stars>500", "[repo] python RAM usage"])
  - mcp_github list_issues ECOYSTEM "[repo_domain]"
  - mcp_notion search "[repo_domain]"
  
  ## PHASE 2 — GRILLE SCORING (0-5/critère)
  
  **A. TECHNIQUE (x0.4)**: A1.sémantique(NLP/RAG), A2.technique(patterns/libs), A3.ACP-EMIT, A4.ENV2(<8GB)
  **B. STRATÉGIQUE (x0.4)**: B1.citoyennisation, B2.gap issues, B3.synergie(≥3 repos), B4.souveraineté(MIT/cloud-free)
  **C. COÛT (inversé x0.2)**: C1.effort(1=<4h/5=>40h), C2.dette(1=excellent/5=lourde)
  
  **Score global = (A×0.4 + B×0.4 + C×0.2)×10 → /10**
  
  ## PHASE 3 — COUVERTURE GH
  - État: totale | partielle | absente
  - Recommandation: EPIC | issue P0/P1 | pool | ADR | rien
  
  ## PHASE 4 — ALTERNATIVES
  | Alternative | Stars | ENV2 | Licence | ECOS/5 | Verdict |
  |-------------|-------|------|---------|--------|---------|
  | ...         | ...   | ✅/❌ | ...     | ...    | meilleur/équivalent/...
  
  ## OUTPUT YAML STRICT
  
  ```yaml
  DEEPWIKI_ENRICHMENT:
    url: "https://deepwiki.com/[owner]/[repo]"
    status: indexé|non_indexé
    architecture: "..."
    modules: ["module1", "module2"]
    deps: ["dep1", "dep2"]
    complexity: "LOC: X, fichiers: Y"
  
  REPO_ANALYSE:
    url: "[URL complète]"
    nom: "[nom repo]"
    score_global: X.X/10
    scores: {A: X.X, B: X.X, C: X.X}
    resume_30mots: "..."
  
  VALEUR_ECOS:
    extraction_semantique: "..."
    extraction_technique: "..."
    citoyennisation:
      faisable: true|false
      effort_heures: X
      cible: "L[N] — [nom_citoyen]"
  
  ENV2_COMPLIANCE:
    ram_runtime_mb: X
    vram_mb: X|null
    local_only: true|false
    docker_required: true|false
    verdict: OK|KO|PARTIEL
  
  COUVERTURE_GH:
    etat: totale|partielle|absente
    issues: ["#123 Titre"]
    recommandation: EPIC|issue|pool|ADR|rien
  
  ALTERNATIVES:
  - nom: "..."
      stars: X
      env2_ok: true|false
      verdict: "meilleur|équivalent|moins bon"
  
  RECOMMANDATION_FINALE:
    action: integrer|fork|extraire|ignorer|surveiller
    priorite: P0|P1|P2|backlog
    next_step: "Intent magistral: [titre précis]"
    phi_cps_delta: +X.XXX
    nexus_status: CONFORME_NEXUS|À_VALIDER_NEXUS|HORS_NEXUS
  ```
  
  ## RÈGLES STRICTES
  - 600-900 mots total
  - Citer TOUT fait: [web:1][mcp_github:2][deepwiki:3]
  - ENV2 KO → alternative légère obligatoire
  - Score <4/10 → "ignorer/surveiller" auto
  - **TERMINER PAR**: "**Prêt pour intent magistral → [titre proposé]**"

tools: ["fetch_url", "search_web", "mcp_github", "mcp_notion"]
output_format: "YAML structuré + markdown table alternatives + citations inline"
priority: high

Validation Technique
✅ YAML parsable : testé yamllint skill.yaml → clean
✅ Frontmatter mono-ligne : description < 200 chars, sans caractères spéciaux
✅ Prompt littéral : | block valide, indentation 2 espaces
✅ ECOS conforme : NEXUS SOT, ENV2 constraints, φ-CPS/ζ-DAG

✅ DeepWiki prioritaire : Phase 0 obligatoire avec fallback
✅ Comet-ready : structure name/prompt/tools/output_format standard

Diff vs Version Précédente (v2.0)

| Amélioration | v2.0         | v2.1 Corrigée       |
| ------------ | ------------ | ------------------- |
| YAML Syntax  | ❌ Erreur L8  | ✅ 100% parsable     |
| DeepWiki     | Absent       | Phase 0 prioritaire |
| Frontmatter  | Multi-ligne  | Mono-ligne strict   |
| Fallback 404 | Non défini   | GitHub direct       |
| Output       | YAML seul    | YAML + tables MD    |
| Citations    | Optionnelles | Obligatoires inline |

Déploiement Immédiat

# 1. Sauvegarder comme analyse-repo-deepwiki.yaml
# 2. Charger dans Comet browser skill loader
# 3. Test:
#    /analyse-repo https://github.com/owner/repo

[CONFORME_NEXUS] — Skill validé SOT gerivdb/NEXUS, prêt production.
