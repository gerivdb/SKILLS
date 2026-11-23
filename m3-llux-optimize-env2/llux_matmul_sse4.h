#ifndef LLUX_MATMUL_SSE4_H
#define LLUX_MATMUL_SSE4_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stddef.h>
#include <stdint.h>

/* ============================================================================
 * LUX MATMUL SSE4.2 — Multiplication de matrice optimisée pour HP Z600
 * (Xeon E5620, SSE4.2, 16 threads logiques, cache L3 12 Mo)
 *
 * Préconditions :
 *   - Toutes les matrices sont en row-major (ligne par ligne)
   - Les données sont alignées sur 16 octets pour les accès SIMD
   - Les dimensions doivent être positives
 *
 * Retour : 0 si succès, code d'erreur sinon
 * ========================================================================== */

/* Produit matrice-matrice C = A x B
 *
 * A : matrice (rows x k), row-major
 * B : matrice (k x cols), row-major
 * C : matrice (rows x cols), row-major (pré-allouée)
 *
 * Utilise SSE4.2 pour le traitement vectoriel (4 floats par opération).
 * Multi-threadé avec le nombre de threads spécifié.
 */
int llux_matmul_sse4(
    const float *A,   /* matrice A, taille rows*k */
    const float *B,   /* matrice B, taille k*cols */
    float *C,         /* matrice C, taille rows*cols (sortie) */
    int rows,         /* lignes de A */
    int k,            /* colonnes de A / lignes de B */
    int cols,         /* colonnes de B */
    int num_threads   /* nombre de threads (recommandé : 16 sur E5620) */
);

/* Version simplifiée pour un seul thread (débogage) */
int llux_matmul_sse4_single(
    const float *A,
    const float *B,
    float *C,
    int rows,
    int k,
    int cols
);

/* Test de bon fonctionnement : vérifie que le matmul donne le bon résultat
 * Retourne 0 si tout va bien, non-zéro sinon */
int llux_matmul_sse4_self_test(void);

/* Nombre de threads recommandé pour la machine actuelle */
int llux_recommended_threads(void);

#ifdef __cplusplus
}
#endif

#endif /* LLUX_MATMUL_SSE4_H */