---
type: skill
version: "1.0.1"
date: "2026-06-18"
intent_hash: 0xHOOK_VALIDATION_REPORTER_φ1.000
status: active
trit_primitive: TritReportHook
tags: [hooks, validation, rapport, git-hygiene, governance, l3-tooling]
layer: "L3_TOOLING"
nexusTags: ["CONFORME_NEXUS", "HOOK_VALIDATION", "REPORTING"]
slotWeight: 1
changelog:
  - {v: "1.0.0", date: "2026-06-18", notes: "Creation — passe 9 clôture axe C — gap rapport validation hooks post-opération"}
  - {v: "1.0.1", date: "2026-06-18", notes: "passe 10 — intent_hash φ1.000 validé conforme φ[X.XXX] — correction note interne erronée"}
---

# hook-validation-reporter

## Purpose

Génère un **rapport structuré de validation** après chaque opération gouvernée par l'écosystème gerivdb : suppression de branches, création de PRs, push de fichiers, création d'issues, modification de registres. Le rapport vérifie que les hooks de gouvernance ont été respectés (RSS-v1, frontmatter, intent_hash, known_repositories) et émet un bilan `[PASS|WARN|FAIL]` par critère.

## Trigger

Utiliser quand :
- une opération batch vient d'être exécutée (suppression branches, push multi-fichiers)
- un skill ou outil CTULU vient de terminer sa séquence
- une passe de session se clôture (fin de passe N)
- un nouveau repo a été créé ou un fichier clé modifié
- besoin d'un bilan de session auditables

## Critères de validation par catégorie

### Git / Branches

| Critère | Règle | Niveau |
|---|---|---|
| Branche protégée intouchée | main/master jamais supprimée | FAIL si violé |
| Intent tracé avant suppression | Protocol branch-lifecycle-intent-tracker suivi | WARN si non |
| PR associée vérifiée | Suppression post-merge confirmée | PASS |
| Nommage conforme RSS-v1 | Préfixe feature/fix/adr/refactor/hotfix | WARN si absent |

### Fichiers / Commits

| Critère | Règle | Niveau |
|---|---|---|
| Frontmatter présent | Tous les .md skills/ADR ont frontmatter YAML | FAIL si absent |
| intent_hash injecté | Format `0x[A-Z_]+_φ[X.XXX]` | WARN si manquant |
| SHA fourni pour update | Aucun update fichier existant sans SHA | FAIL si violé |
| Secrets scannés | run_secret_scanning si contenu sensible | WARN si non fait |

### Registres / Governance

| Critère | Règle | Niveau |
|---|---|---|
| known_repositories.yaml | Nouveau repo déclaré avant 1er commit | FAIL si absent |
| do_not_create respecté | Aucun repo créé si do_not_create: true | FAIL si violé |
| Tags NEXUS présents | [CONFORME_NEXUS|À_VALIDER_NEXUS|HORS_NEXUS] | WARN si absent |
| Strate L assignée | layer: L0-L9 déclaré | WARN si absent |

### Skills SKILLS

| Critère | Règle | Niveau |
|---|---|---|
| Fichier dans bon dossier | `perplexity/skills/*.md` | FAIL si ailleurs |
| version sémantique | Format `X.Y.Z` | WARN si absent |
| trit_primitive déclaré | Champ présent dans frontmatter | WARN si absent |
| changelog présent | Au moins 1 entrée | WARN si absent |

## Format du rapport

```
╔══════════════════════════════════════════════════════════════╗
║  HOOK VALIDATION REPORT — {date} {heure} CEST               ║
║  Opération: {description opération}                          ║
║  Scope: {repos/fichiers concernés}                           ║
╠══════════════════════════════════════════════════════════════╣
║  RÉSULTAT GLOBAL: [✅ PASS | ⚠️ WARN | ❌ FAIL]              ║
╠══════════════════════════════════════════════════════════════╣
║  CRITÈRES                                                    ║
║  ✅ PASS  {N}  critères                                      ║
║  ⚠️  WARN  {N}  critères                                     ║
║  ❌ FAIL  {N}  critères                                      ║
╠══════════════════════════════════════════════════════════════╣
║  DÉTAIL                                                      ║
║  [✅|⚠️|❌] {catégorie} — {critère}: {valeur observée}       ║
╠══════════════════════════════════════════════════════════════╣
║  ACTIONS REQUISES                                            ║
║  → {action corrective pour chaque FAIL/WARN critique}        ║
╚══════════════════════════════════════════════════════════════╝
```

## Rapport exemple — Session 2026-06-18 ECOS-CLI

```
╔══════════════════════════════════════════════════════════════╗
║  HOOK VALIDATION REPORT — 2026-06-18 21:04 CEST             ║
║  Opération: Suppression 5 branches + création 9 skills       ║
║  Scope: gerivdb/ECOS-CLI, gerivdb/SKILLS                     ║
╠══════════════════════════════════════════════════════════════╣
║  RÉSULTAT GLOBAL: ✅ PASS                                     ║
╠══════════════════════════════════════════════════════════════╣
║  CRITÈRES                                                    ║
║  ✅ PASS  12  critères                                       ║
║  ⚠️  WARN   1  critères                                      ║
║  ❌ FAIL   0  critères                                       ║
╠══════════════════════════════════════════════════════════════╣
║  DÉTAIL                                                      ║
║  ✅ Git — Branches protégées intouchées: main OK             ║
║  ✅ Git — Intent tracé avant suppression: 5/5 vérifiées      ║
║  ✅ Git — PR associée vérifiée: 2 post-merge, 3 abandonnées  ║
║  ✅ Fichiers — Frontmatter présent: 9/9 skills               ║
║  ✅ Fichiers — SHA fourni: N/A (création, pas update)        ║
║  ✅ Fichiers — intent_hash: format φ1.000 = conforme         ║
║     φ[X.XXX] validé passe 10 — aucune action requise         ║
║  ✅ Governance — Tags NEXUS: CONFORME_NEXUS sur tous         ║
║  ✅ Governance — Strate L assignée: L2/L3 selon skill        ║
║  ✅ Skills — Fichier dans bon dossier: 9/9                   ║
║  ✅ Skills — version sémantique: 9/9                         ║
║  ✅ Skills — changelog présent: 9/9                          ║
║  ✅ Skills — trit_primitive: 9/9                             ║
║  ⚠️  Git — Nommage RSS-v1: 1 branche sans préfixe standard  ║
╠══════════════════════════════════════════════════════════════╣
║  ACTIONS REQUISES                                            ║
║  → Identifier branche non-standard et clarifier intent       ║
╚══════════════════════════════════════════════════════════════╝
```

## Intégration écosystème

- **Déclenché par** : tout skill ou outil CTULU post-opération
- **Précédé par** : `branch-lifecycle-intent-tracker` (branches), `ctulu-result-integrator` (outils)
- **Alimente** : `contextual-stash-manager` (rapport archivé si > 2k tokens)
- **Référence gouvernance** : `gerivdb/GOVERNANCE-HUB` (RSS-v1, AGENT_RAM, BRIDGES)
- **Rapport persisté dans** : `gerivdb/CTULU/tools/REPORTS/` si action requise
