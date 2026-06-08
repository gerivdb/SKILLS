---
name: z600-hardware
description: "HP Z600 constraints (2× Xeon E5620, 18 GB DDR3, no GPU), Owl Alpha SLM CPU-only, RAM budget 4 agents. Use when user mentions 'Z600', 'RAM', 'CPU-only', 'Owl Alpha', 'parallel agents', 'worktrees'."
version: "1.0.0"
changelog:
  - {v: "1.0.0", date: "2026-06-08", notes: "Créé — contraintes hardware Z600 pour KiloCode"}
triggers: ["Z600", "RAM", "CPU-only", "Owl Alpha", "parallel agents", "worktrees"]
layer: "L4_TOOL"
nexusTags: ["CONFORME_NEXUS"]
trit_primitive: TritOptimize
---
# Z600 Hardware Constraints

## Contexte

Le Z600 (HP workstation, 2010) est la machine principale pour KiloCode et les agents SLM. Contraintes matérielles strictes.

## Spécifications

| Composant | Valeur | Impact |
|-----------|--------|--------|
| CPU | 2× Xeon E5620 (8C/16T @ 2.4 GHz) | Pas d'AVX, pas de GPU |
| RAM | 18 GB DDR3 ECC | Max 4 agents simultanés (~3 GB/agent) |
| Stockage | SSD 1 To (C:), SSD 2 To (D:) | Worktrees sur D:\, source sur C: |
| GPU | Quadro 4000 (Fermi) | Inutilisable pour ML moderne |
| OS | Windows 10 | PowerShell 7+, git, Python 3.12 |

## Budget RAM pour agents

| Configuration | RAM utilisée | Restant OS |
|---------------|-------------|-----------|
| 1 agent | ~3 GB | ~15 GB |
| 2 agents | ~6 GB | ~12 GB |
| 4 agents | ~12 GB | ~6 GB ← limite pratique |
| 6 agents | ~18 GB | ~0 GB ← RISQUE SWAP |

**Règle : ne jamais dépasser 4 agents simultanés.**

## Contraintes Owl Alpha (SLM local)

| Paramètre | Limite |
|-----------|--------|
| Context window | ~4000 tokens (pratique: 2000) |
| Vitesse inférence | ~200 tokens/sec CPU-only |
| Prompt max | 200 tokens (fiable), 500 (limite) |
| Batch | Privilégier batch > séquentiel |

## Règles de décision

- **Règle 1** : 4 agents max en parallèle (RAM)
- **Règle 2** : Prompts < 200 tokens (contexte SLM)
- **Règle 3** : Tâches atomiques, déterministes (pas d'inférence complexe)
- **Règle 4** : Worktrees sur D:\ (pas C:\ — espace disque)
- **Règle 5** : Supprimer les worktrees après merge

## Intégration

- KiloCode Agent Manager : `maxAgents: 4` dans kilo.json
- Worktrees git : `git worktree add ../WORKTREE-{name} main`
- RAM monitoring : `Get-CimInstance Win32_OperatingSystem | Select FreePhysicalMemory`

## Référence

- Skill : `L4-TOOLS/SKILLS/skills/kilocode-worktree-agent/SKILL.md`
- Prompt design : `L4-TOOLS/SKILLS/skills/slm-local-prompt-design/SKILL.md`
