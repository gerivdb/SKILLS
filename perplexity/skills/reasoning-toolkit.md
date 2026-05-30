---
name: reasoning-toolkit
version: "1.0.0"
description: "Fused skill combining Fermi‑legacy (hardware/performance expert for FERMI‑EVER, CodeDB‑E5620, LYCOS) and Scientific Method (hypothesis validation, NEXUS protocol). Use when user mentions any of the original triggers."
triggers: ["FERMI", "CodeDB-E5620", "LYCOS", "Xeon E5620", "GPU Fermi", "AVX", "LXC Z600", "SSE4.2", "Poincaré", "Feynman", "méthode scientifique", "hypothèse"]
layer: "L5_META"
nexusTags: ["CONFORME_NEXUS", "HYPOTHÈSE_NON_CONFIRMÉE"]
prerequisites: []
slotWeight: 1
status: active
changelog:
  - {v: "1.0.0", date: "2026-05-30", notes: "Fusion of fermi-legacy.md and scientific-method.md"}
---
# Reasoning Toolkit (Fused)

This skill merges the two original reasoning‑related skills:

* **Fermi Legacy** – legacy hardware and performance expert for Fermi‑ever, CodeDB‑E5620, Lycos; provides guidance on GPU Fermi, Xeon E5620 (SSE4.2 only), LXC containers on Z600, etc.
* **Scientific Method** – covers the application of the scientific method to the ecosytem: hypothesis validation, NEXUS protocol, Feynman/Pokincar techniques, anomaly detection, and actionable recommendations.

The unified skill provides a single entry point for any request relating to legacy hardware performance optimisation or scientific‑method‑based analysis and validation.

## Domaine et périmètre
(Combined from the two sources – see original files for full details.)

## Méthodologie
(Combined from the two sources – see original files for full details.)

## Règles de décision
(Combined from the two sources – see original files for full details.)

## Format de sortie
(Combined from the two sources – see original files for full details.)

## Exemples d'utilisation
(Combined from the two sources – see original files for full details.)

## Intégration avec l'écosystème
- Dépôts concernés : FERMI-EVER, CodeDB-E5620, LYCOS, NEXUS, BRAIN (as per original skills)
- Couche EECS : L5_META (primary)
- Tags NEXUS : [CONFORME_NEXUS], [HYPOTHÈSE_NON_CONFIRMÉE]