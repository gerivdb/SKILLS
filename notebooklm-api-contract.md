---
type: SPEC
version: 1.0.0
intent_hash: 0xSPEC_NBMLM_API_CONTRACT_20261106
status: proposed
wal_id: 0x243
friction: 0.0
entropy: 0.0
seal: WAL-0x243-SPEC-NBMLM-PASS
---

# Spécification — notebooklm-api-contract

## 1. Objet

Spécifier l'interface stricte de la bibliothèque `notebooklm-py` v0.8.6 pour toute synchronisation vers NotebookLM depuis le métacluster GERIVDB (ENV2/ENV3).

## 2. Contexte

Lors de la Phase 3 du PRD-MOC WiCi, le `vault-sync-daemon` a échoué 3 fois à cause d'une mauvaise instanciation du client :
- `client_cls(auth=dict)` refusé : `AuthTokens` attendu, pas un dict simple.
- `await NotebookLMClient.from_storage(...)` déprécié : forme canonique `async with` obligatoire.
- `auth.storage_path` requis : l'objet auth doit exposer l'attribut `storage_path`.

## 3. Règles obligatoires

### R1 — Authentification
L'authentification doit s'effectuer exclusivement via un objet `AuthTokens` obtenu par `notebooklm.auth.load_auth_from_storage(path)` où `path` est un objet `pathlib.Path` (pas un `str`).

Interdit : passer un `dict` brut en paramètre `auth` de `NotebookLMClient`.

### R2 — Initialisation du client
Le client doit être instancié uniquement via la forme canonique :
```python
async with NotebookLMClient.from_storage(str(storage_state_path)) as client:
    ...
```

Interdit :
- `NotebookLMClient(auth=dict)` sans `storage_path`
- `await NotebookLMClient.from_storage(...)` (forme legacy dépréciée, supprimée en v1.0)

### R3 — Ajout de source texte
L'ajout de texte dans un carnet doit utiliser :
```python
await client.sources.add_text(
    notebook_id=notebook_id,
    title=title,
    content=content,
    wait=False,
)
```

### R4 — Vérification avant exécution
Avant tout appel `add_text`, vérifier que `client.sources` et `client.sources.add_text` existent (non `None`).

## 4. Version cible

- `notebooklm-py` : 0.8.6 (installé dans le venv RAGX de ENV2)
- Python : 3.12+

## 5. Référence ADR

- **ADR** : ADR-098-test-handler-first (principe : lire le handler avant d'écrire les tests/appels)
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed
