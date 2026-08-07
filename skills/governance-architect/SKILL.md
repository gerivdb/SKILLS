---
name: governance-architect
description: >
  Questionnement architectural par 4 mathemes attracteurs (M1-M4).
  Active ce skill avant toute creation d'artefact de gouvernance (PRD, ADR, INTENT, EPIC,
  design, workflow) pour verifier les liens causaux entre mathematiques, personas L0,
  repos et patterns. Remplace la hierarchie N-1->N6 par un topos de constellations.
version: 1.0.0
intent_hash: 0xSKILL_GOVERNANCE_ARCHITECT_20260805
---

# Governance Architect

## Declencheur

Toute action qui :
- Cree ou modifie un artefact de gouvernance (PRD, ADR, INTENT, EPIC, MOC)
- Definit une architecture ou un design
- Cree un workflow, un pipeline, un script d'orchestration
- Ajoute ou modifie un pattern, un atome, un citizen
- Necessite une validation cross-repo

## Protocole - 4 Questions Obligatoires

### Q1 (M1 - Continuite) : Topologie

```
Quelle est la structure du probleme ?
- Quels sont les objets (ENV, repos, artifacts) ?
- Quels sont les morphismes (deploiements, transformations, workflows) ?
- Quels sont les invariants (symetries, cycles, points fixes) ?
- Comment les objets se recollent-ils en un faisceau coherent ?
```

**Livrable** : Graphe ASCII ou Mermaid des objets/morphismes.

### Q2 (M2 - Information) : Mesure

```
Quelle est la mesure d'information pertinente ?
- Ou est l'entropie ? (H = -Sigma p_m log2 p_m)
- Quelle est la complexite ? (Kolmogorov)
- Quels sont les signaux vs le bruit ?
- Comment mesurer la derive semantique ?
```

**Livrable** : Metriques H, K, seuils d'alerte.

### Q3 (M3 - Transformation) : Execution

```
Comment transformer l'information en action verifiable ?
- Quel est le morphisme d'execution ?
- Comment verifier la correctitude ? (Hoare, Milner)
- Quel est le rollback ? (F-1oF = id)
- Quelles sont les contraintes ENV2 ? (SSE4.2, 24Go, <50ms)
```

**Livrable** : Specification d'execution + rollback + contraintes.

### Q4 (M4 - Finalite) : Gouvernance

```
Quel est le contrat de gouvernance et de transmission ?
- Quelles personas L0 sont activees ?
- Quel est le contrat Default-FAIL ?
- Comment transmettre le savoir ? (documentation, verse, atome)
- Quel est le lien ADR/INTENT/PRD ?
```

**Livrable** : Mapping personas -> mathemes -> repos -> patterns.

## Regles Causalite

1. **Tout artifact DOIT etre rattachable a un matheme.**
   Si aucun M1-M4 ne s'applique -> STOP, demander HITL.

2. **Tout matheme DOIT avoir au moins une persona L0 dans VERSES/verses/.**
   Si persona manquante -> creer verse + atome + citizen avant de continuer.

3. **Toute persona L0 DOIT etre referencee dans unified-design/atoms/ ET REPO-STANDARDS/norms/.**
   Si reference manquante -> creer/mettre a jour.

4. **Aucun workflow ne peut demarrer sans calcul de quorum par matheme.**
   ```
   Q(R) = ceil(Sigma_{i=1..4} w_i(M_i actives) x 0.75)
   ```
   Si Q(R) < seuil -> STOP.

5. **La distance de Wasserstein entre distributions de patterns actives**
   **dans chaque couple de mathemes DOIT etre <= 0.5.**
   Si W > 0.5 -> alerte, demander mediateur.

6. **La topologie grothendieckienne est l'orchestration par defaut.**
   Chaque ENV = objet, chaque deploiement = morphisme,
   `F_KEEL` = faisceau coherent sur le site TOPOS.

7. **Default-FAIL** : Un critere ne passe a `true` QUE si preuve tangible
   (hash, log, diff, test_output).

## Mapping Patterns -> Mathemes

| Pattern | Matheme(s) |
|---------|------------|
| @constructive | M3 |
| @entropy | M2 |
| @knuth+@mem_bound | M2 |
| @feynman+@dimension | M3 |
| @lurie_higher_topos | M4 |
| @lafforgue_langlands | M4 |
| @voevodsky_motifs | M4 |
| @vapnik_vc | M2 |
| @mackay_bayes | M2 |
| @scholkopf_kernel | M2 |
| @learning | M2 |
| @jordan_stat | M2 |
| @schmidhuber_metalearn | M2 |
| @symmetry+@topos_rollback | M1 |
| @dijkstra_graph | M1 |
| @berry_causal | M1 |
| @mandelbrot_fractal | M1 |
| @wolfram_automata | M1 |
| @julia_iteration | M1 |
| @feigenbaum_bifurcation | M1 |
| @nash_equilibrium | M1 |
| @bellman_dynamic | M1 |
| @hoare_contract | M3 |
| @milner_types | M3 |
| @sifakis_components | M3 |
| @mccarthy_metalang | M3 |
| @numa | M3 |
| @turing | M3 |
| @feynman | M3 |
| @kolmogorov | M2 |
| @deploy+@compile | M3 |
| @usecase | M4 |
| @sdk | M4 |
| @illusie_fantechi_doc | M4 |
| @audit | M4 |
| @perf | M3 |
| @sse4_only+@zig_0.14 | M3 |
| @korx_372b+@kbin_context | M3 |
| @q243_format+@piano_diff | M1 |
| @boinc_p2p | M3 |
| @cold_start_2s+@causal_latency_50ms | M1 |
| @rlm_243 | M3 |
| @db_schema_v1.0 | M4 |
| @acid_tx_v1.0 | M4 |
| @crm_workflow_v1.0 | M4 |
| @office_export_v1.0 | M4 |

## Workflow d'Implementation

```yaml
wf create_artifact
resonate M4
vote grothendieck deligne hassani
exec write_prd
ckpt save_metadata
audit check_quorum
merge go
```

## Verification

Avant toute implementation, executer `architectural-questionnaire.ps1` :
- Q1 : Topologie
- Q2 : Entropie H <= 0.6
- Q3 : Rollback F-1oF = id
- Q4 : Personas L0 presentes

## References

- **ADR** : ADR-MATHEMES-PERSONAS-ORCHESTRATION-2026-08-05
- **INTENT** : INTENT-MATHEMES-PERSONAS-ORCHESTRATION-2026-08-05
- **META-DESIGN** : unified-design/docs/MATHEMES-FRAMEWORK.md
- **KEEL PRD-005** : TOPOS comme categorie de sites Grothendieck
- **SCI-VERSE** : VERSES/verses/sci-verse.md
