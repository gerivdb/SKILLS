---
type: SKILL
version: "1.0.0"
status: active
intent_hash: 0xSKILL_M3_LLUX_OPTIMIZE_ENV2_20261122
shard_id: "G"
turn_counter: "1"
timestamp: "2026-11-22T01:25:00Z"
wal_reference: "0x243"
stratum: "L4-TOOLS"
domain: "performance-optimization"
invariants:
  friction: 0.0
  entropy: 0.0
---

# Skill : M3 Build Optimize — Implémentation complète LLUX sur ENV2

## Problème

L'inférence LLaMA sur votre HP Z600 (2× Xeon E5620, 2.4 GHz, SSE4.2, 24 Go DDR3) tourne à ~0,3-0,5 tok/s. Le build est rapide, mais l'inférence est lente car :
- Le CPU n'a **pas d'AVX2** (SSE4.2 max)
- Le matmul tourne probablement en **séquentiel** sur un seul cœur
- Pas de tiling adapté au cache L3 (12 Mo)

## Ce que ce skill implémente

### 1. Matmul SSE4.2 multi-threadé
Un produit matrice-matrice optimisé pour le cache L3 (12 Mo) et parallèlisé sur les 16 threads logiques du E5620.

### 2. Remplacement du matmul dans le forward pass
Remplace la boucle séquentielle par le matmul parallèle.

### 3. Réutilisation des buffers
Pas d'allocation à chaque forward.

## Fichiers créés

| Fichier | Rôle |
|---------|------|
| `llux_matmul_sse4.c` | Implémentation C du matmul SSE4.2 multi-threadé |
| `llux_matmul_sse4.h` | Header avec déclarations |
| `build_fast.ps1` | Script de compilation optimisée |
| `benchmark_llux.py` | Script de mesure du débit |

## Étapes d'intégration

### Étape 1 : Copier les fichiers dans votre repo LLUX

```powershell
# Depuis la racine de votre repo LLUX
cp D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\m3-llux-optimize-env2\llux_matmul_sse4.c src/
cp D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\m3-llux-optimize-env2\llux_matmul_sse4.h src/
cp D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\m3-llux-optimize-env2\build_fast.ps1 .
```

### Étape 2 : Intégrer le matmul dans votre forward pass

Dans votre fichier `transformer.zig` (ou équivalent), remplacez l'appel au matmul séquentiel par l'appel à `llux_matmul_sse4` :

```zig
// Avant (séquentiel)
for (matrice_A, 0..rows) |row, i| {
    for (matrice_B[0], 0..cols) |_, j| {
        var sum: f32 = 0;
        for (matrice_A[i], 0..k) |val, k_idx| {
            sum += val * matrice_B[k_idx][j];
        }
        resultat[i][j] = sum;
    }
}

// Après (SSE4.2 multi-threadé)
llux_matmul_sse4(
    matrice_A.ptr,      // pointeur vers matrice A (rows x k)
    matrice_B.ptr,      // pointeur vers matrice B (k x cols)
    resultat.ptr,       // pointeur vers résultat (rows x cols)
    rows,               // lignes de A
    k,                  // colonnes de A / lignes de B
    cols,               // colonnes de B
    16,                 // nombre de threads (E5620 = 16)
);
```

### Étape 3 : Compiler et tester

```powershell
# Dans le répertoire de votre repo LLUX
.\build_fast.ps1
```

Puis mesurez le débit :
```powershell
python benchmark_llux.py --model chemin/vers/modele.gguf --prompt "votre texte"
```

---

## Fichier : llux_matmul_sse4.h

---
