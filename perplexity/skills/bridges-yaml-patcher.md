---
name: bridges-yaml-patcher
description: "Lit BRIDGES.yaml, identifie les bridges a transitionner, patch les statuts, verifie que les fichiers de code correspondants existent reellement, emet le commit. Inclut validation pre-transition."
version: "1.0.0"
triggers:
  - "patcher bridges"
  - "maj bridges yaml"
  - "transitionner bridge"
  - "update bridge status"
layer: "L2_COMPOSITION"
nexusTags: ["CONFORME_NEXUS", "BRIDGES_YAML", "PATCHER"]
status: "active"
changelog:
  - {v: "1.0.0", date: "2026-06-11", notes: "Creation — pattern repete 8 fois dans N+13 a N+22"}
slotWeight: 1
trit_primitive: TritDoConfig
---

# BRIDGES-YAML-PATCHER — Patch de BRIDGES.yaml

## Domaine et perimetre

Ce skill patch les statuts des bridges dans BRIDGES.yaml avec validation pre-transition : verifier que les fichiers de code correspondants existent reellement avant de valider la transition.

## Methodologie

### Phase 1 — Lire et identifier

```
GET gerivdb/GOVERNANCE-HUB/BRIDGES.yaml
→ Identifier les bridges a transitionner (liste fournie)
→ Pour chaque bridge, lire le champ component
```

### Phase 2 — Valider l'existence du code

Pour chaque transition candidate :
```
GET gerivdb/<repo>/<component_path>
→ Si 200 + taille > 100 bytes → code existe → VALIDE
→ Si 400 → code absent → BLOQUE la transition
```

### Phase 3 — Patcher

Pour chaque transition valide :
1. Modifier `status` dans BRIDGES.yaml
2. Mettre a jour `meta.active_count`, `meta.defined_count`, etc.
3. Mettre a jour `meta.last_updated`
4. Incrementer `meta.version` (patch semver)
5. Emettre le commit

### Phase 4 — Rapport

```
[BRIDGES_PATCHER] Transitions validees : N
[BRIDGES_PATCHER] Transitions bloquees : N (code manquant)
[BRIDGES_PATCHER] BRIDGES.yaml v<X> → v<X+1>
```

## Regles de decision

- **Regle 1** : Jamais de transition sans verification de l'existence du code
- **Regle 2** : Mettre a jour les compteurs meta systematiquement
- **Regle 3** : Un seul commit par groupe de transitions
- **Regle 4** : Distinct de nexus-registry-sync (gere les repos, pas les bridges)

## Integration

- **Declencheur** : Fin de session d'implementation
- **Dependances** : Acces GitHub API
- **Complementaire de** : bridge-lifecycle-manager
