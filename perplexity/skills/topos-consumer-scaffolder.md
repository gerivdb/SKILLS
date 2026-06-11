---
name: topos-consumer-scaffolder
description: "A partir d'un topos.yaml cible + d'un role agent (security/audit/validation/ops), genere le fichier consumer Python complet avec load_topos(), process(), emit_report(). Frameworkable comme template parametrise. Pattern detecte dans N+16 (4 consumers TOPOS identiques)."
version: "1.0.0"
triggers:
  - "scaffolder consumer"
  - "creer consumer topos"
  - "topos consumer"
  - "generer consumer"
  - "nouveau consumer agent"
layer: "L1b"
nexusTags: ["CONFORME_NEXUS", "TOPOS", "SCAFFOLDER"]
status: "active"
changelog:
  - {v: "1.0.0", date: "2026-06-11", notes: "Creation — pattern detecte dans N+16 (SABRE, MirrorFish, CoPaw, Alfred)"}
slotWeight: 1
trit_primitive: TritDoConfig
---

# TOPOS-CONSUMER-SCAFFOLDER — Generation de consumers TOPOS

## Domaine et perimetre

Ce skill genere un fichier consumer Python complet a partir d'un role agent et d'un profil TOPOS. Le pattern a ete detecte dans N+16 ou 4 consumers TOPOS (SABRE, MirrorFish, CoPaw, Alfred) ont ete crees avec une structure identique.

## Template de generation

### Entree

- `agent_name` : nom de l'agent consumer (ex: "SABRE", "MirrorFish")
- `role` : role du agent (security / audit / validation / ops)
- `source_path` : chemin vers le topos.yaml source
- `output_format` : format de sortie (JSON / YAML / dict)

### Sortie

Fichier Python `<agent_name>/bridges/topos_<role>_consumer.py` avec :

```python
class Topos<Role>Consumer:
    def __init__(self, source_path: str):
        self.source_path = source_path
        self._data = None

    def load_topos(self) -> dict:
        """Charge le topos.yaml source."""
        ...

    def validate(self) -> dict:
        """Valide le profil contre le schema."""
        ...

    def process(self) -> dict:
        """Traite les donnees selon le role."""
        ...

    def emit_report(self) -> dict:
        """Emet le rapport final."""
        ...
```

## Methodologie

### Phase 1 — Identifier le role

Selon le role, le consumer implemente differentes logiques :
- **security** : audit de securite, detection de flags, backup
- **audit** : ingestion de profils, alimentation audit trail
- **validation** : validation contre schema, metriques de couverture
- **ops** : lecture de matrice EECS, vue operationnelle

### Phase 2 — Generer le fichier

1. Creer l'arborescence `<agent>/bridges/`
2. Generer le fichier Python avec le template parametre
3. Ajouter les tests unitaires `<agent>/tests/bridges/test_topos_consumer.py`
4. Ouvrir la PR

### Phase 3 — Verifier

- Le fichier compile sans erreur
- Les tests passent
- Le consumer peut charger un topos.yaml de test

## Regles de decision

- **Regle 1** : Tous les consumers heritent de la meme interface de base
- **Regle 2** : Le role determine la methode `process()` specifique
- **Regle 3** : Les tests sont generes automatiquement avec le consumer

## Integration

- **Declencheur** : Creation d'un nouveau repo agent, ajout d'un bridge TOPOS
- **Dependances** : Acces GitHub API pour verifier l'existence du repo cible
- **Pattern source** : N+16 (SABRE, MirrorFish, CoPaw, Alfred)
