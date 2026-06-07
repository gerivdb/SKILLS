---
name: env-capability-probe
description: "Detection des capacites reelles de l'ENV actif AVANT de creer un pipeline CI. Verifie la presence des binaires (zig, python, node, docker, git) et genere un rapport de compatibilite. Utiliser avant toute creation de pipeline KIVA-CLI ou ajout de step CI."
version: "1.0.0"
triggers:
  - "creation pipeline CI"
  - "nouveau step CI"
  - "pipeline run echoue"
  - "step skippe sans raison"
  - "avant zig build"
layer: "L4_ORCHESTRATION"
nexusTags: ["CONFORME_NEXUS", "ENV_PROBE", "PRE_CONDITION"]
status: "active"
changelog:
  - {v: "1.0.0", date: "2026-06-07", notes: "Creation — remede P12 lacune env-capability-probe manquant"}
prerequisites:
  - "Acces shell PowerShell (ENV2) ou bash (ENV3)"
slotWeight: 1
---

# ENV-CAPABILITY-PROBE — Sonde de capacités'environnement

## Domaine et perimetre

Ce skill detecte les capacites reelles de l'ENV actif **avant** de creer un pipeline CI qui les suppose. Il repond a la question :

> "Est-ce que l'outil X est disponible sur cette machine pour le pipeline Y ?"

Cree suite a la session MC-RNN ou le step `zig build test` a ete silencieusement skippe (lacune L3/P12) car Zig n'etait pas disponible sur ENV1.

## Protocole

### Phase 1 — Identifier l'ENV actif

| ENV | Machine | OS | Acces shell |
|---|---|---|---|
| ENV1 | Perplexity SaaS | Cloud | API GitHub uniquement (pas de shell local) |
| ENV2 | HP Z600 | Windows PowerShell | Complet (zig, python, git, etc.) |
| ENV3 | Mistral local | Linux | Complet |

**Regle** : Si ENV1 (SaaS), aucun binaire local n'est disponible. Les steps CI doivent etre executes via l'API GitHub ou skippe.

### Phase 2 — Sonde systematique

Pour chaque outil requis par le pipeline, executer :

```powershell
# Zig
zig version          # Attendu: "0.14.0" ou superieur

# Python
python --version     # Attendu: "3.10" ou superieur

# Node.js
node --version       # Attendu: "18" ou superieur

# Docker
docker version       # Attendu: version valide

# Git (local)
git --version        # Attendu: "2.x"

# Git (API)
gh auth status       # Attendu: "Logged in"
```

### Phase 3 — Generer le rapport

```
[ENV_PROBE] ENV identifie: ENV2 (HP Z600, Windows)
[ENV_PROBE] zig: PRESENT v0.14.0
[ENV_PROBE] python: PRESENT 3.11
[ENV_PROBE] node: ABSENT
[ENV_PROBE] docker: ABSENT
[ENV_PROBE] git: PRESENT 2.42
[ENV_PROBE] recommandation: steps node/docker doivent etre SKIP ou delegues
```

### Phase 4 — Appliquer au pipeline

Pour chaque outil ABSENT :
- Dans le pipeline YAML : ajouter `when: "env.get('SKIP_<OUTIL>', '0') != '1'"`
- Dans le skill d'installation : documenter comment installer l'outil
- Alternative : deleguer le step a un ENV qui dispose de l'outil

## Cas d'usage MC-RNN

Le pipeline `mc-rnn-ci.yaml` contient un step `codedb-bench` qui utilise `zig build test`.
Ce step ete cree sans verifier que Zig etait disponible sur ENV1.
Resultat : step silencieusement skippe, 15 tests Zig jamais valides sur la machine cible.

Avec ce skill, avant de creer le step :
```
[ENV_PROBE] ENV1: zig ABSENT
[ENV_PROBE] DECISION: step zig delegue a ENV2 ou marque SKIP_ZIG=1
```

## Integration ecosysteme

- **Declencheur** : Avant toute creation de pipeline CI
- **Complement de** : `pre-push-path-audit` (verifie les remotes), `branch-audit-cleanup` (verifie les branches)
- **Reference ADR** : adr-mc-rnn-closure-20260607.md (lacune L3/P12)
