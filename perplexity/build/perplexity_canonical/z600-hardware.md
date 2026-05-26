---
name: z600-hardware
description: "HP Z600, E5620, Fermi GPU, AVX limitations, WASM bypass, Zig, LXC. Use when user mentions 'Z600', 'E5620', 'Fermi', 'AVX', 'WASM', 'Zig', 'LXC'."
---
|

# z600-hardware
|
# Z600 Hardware

## Domaine et périmètre

Ce skill couvre le **matériel HP Z600** et ses contraintes :
- HP Z600 (Xeon E5620, 24 GB RAM ECC DDR3, pas d'AVX)
- GPU Quadro 4000 Fermi 2 Go (à éviter, no-gpu par défaut)
- Compilation Zig sans AVX (CodeDB-E5620, LYCOS)
- VM1 (VirtualBox, Ubuntu 22.04, LXC)
- KIVA-CLI comme pipeline CI local
- Tâches planifiées Windows (Task Scheduler)

## Méthodologie

### Phase 1 : Diagnostic matériel
- Vérifier la compatibilité CPU (E5620 = Westmere, pas d'AVX, SSE4.2 seulement).
- Vérifier l'état du GPU (Quadro 4000 Fermi, souvent en erreur).
- Vérifier la RAM disponible (< 8 GB pour les applis légères).

### Phase 2 : Optimisation
- Proposer des solutions CPU-only (llama.cpp, Zig no-AVX).
- Configurer les bypass WASM-SIMD pour le matériel legacy.
- Activer KIVA-CLI pour la CI locale (pas GitHub Actions).

## Règles de décision
- **Règle 1** : Toujours privilégier le CPU sur GPU Fermi (trop instable).
- **Règle 2** : Zig sans AVX = CodeDB-E5620 ou LYCOS.
- **Règle 3** : KIVA-CLI remplace GitHub Actions pour la CI locale.

## Format de sortie

```markdown
## Diagnostic matériel
- CPU : ...
- RAM : ...
- GPU : ...
- Recommandation : ...
```

## Exemples d'utilisation
- "Mon Z600 peut-il faire tourner un LLM ?" → Évaluer les options CPU.
- "Corrige le crash WASM-SIMD" → Appliquer les bypass Zig.
- "Configure KIVA-CLI pour la CI locale" → Activer le pipeline.

## Intégration avec l'écosystème
- Dépôts concernés : KIVA-CLI, CodeDB-E5620, LYCOS, FERMI-EVER
- Couche EECS : L1_CAUSALITY
- Tags NEXUS : [CONFORME_NEXUS], [DÉRIVÉ]

