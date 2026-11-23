---
type: SKILL
version: "1.0.0"
status: active
intent_hash: 0xSKILL_M3_BUILD_OPTIMIZE_20261122
shard_id: "G"
turn_counter: "1"
timestamp: "2026-11-22T00:45:00Z"
wal_reference: "0x243"
stratum: "L4-TOOLS"
domain: "build-optimization"
invariants:
  friction: 0.0
  entropy: 0.0
---

# Skill : M3 Build Optimize — Build LLUX sur ENV2 (HP Z600)

## Déclencheur
Le build Zig de LLUX (ou tout projet Zig sur ENV2) prend trop de temps (ex: 10 minutes pour 27 couches). Il faut réduire ce temps d'au moins 10x sur le matériel HP Z600 (2× Xeon E5620, 2.4 GHz, 16 threads, 24 Go DDR3 ECC, pas d'AVX2).

## Protocole d'optimisation

### Étape 1 — Identifier le goulot d'étranglement
```powershell
# Mesurer le temps de build actuel
Measure-Command { zig build -Dcpu=westmere -Doptimize=ReleaseFast }
```

### Étape 2 — Lancer avec parallélisme maximal (16 threads)
```powershell
zig build -Dcpu=westmere -Doptimize=ReleaseFast -j 16
```

### Étape 3 — Précompiler les bibliothèques stables
Si certaines bibliothèques ne changent pas, les compiler une seule fois en `.o` et les lier ensuite.

### Étape 4 — Utiliser ReleaseSmall au lieu de ReleaseFast pour le développement
```powershell
zig build -Dcpu=westmere -Doptimize=ReleaseSmall -j 16
```

### Étape 5 — Diviser les gros fichiers .zig
Si un fichier .zig dépasse ~2000 lignes, le diviser en plusieurs fichiers pour permettre la compilation parallèle à l'intérieur d'une même bibliothèque.

## Dépendances
- `m3-tree` : structure de décision pour choisir les optimisations
- `m3-branch` : isolation du travail sur une branche dédiée
- `m3-driver` : le driver zig.exe est le processus à optimiser

## Récapitulatif des gains attendus sur ENV2 (E5620)

| Action | Gain estimé | Temps estimé après |
|--------|-------------|-------------------|
| -j 16 (parallélisme) | 3× à 5× | 2-3 min |
| -O ReleaseSmall (dev) | 3× à 5× | 2-3 min |
| Précompilation libs | 2× à 3× | 2-3 min |
| Division fichiers .zig | 1.5× à 2× | 1-2 min |
| **Cumul** | **10× à 20×** | **30s à 1 min** |

## Fichiers à créer sur ENV2

| Fichier | Rôle |
|---------|------|
| `build-fast.ps1` | Script PowerShell qui lance zig build avec les bons flags |
| `build-fast.zig` | Fichier build.zig optimisé (précompilation des libs stables) |

## Dépendances

- M3 TREE : `unified-design/atoms/m3-tree.md`
- M3 BRANCH : `unified-design/atoms/m3-branch.md`
- M3 DRIVER : `unified-design/atoms/m3-driver-unified-referential.md`
- M3 PRIMUS : `unified-design/atoms/m3-primus.md`
