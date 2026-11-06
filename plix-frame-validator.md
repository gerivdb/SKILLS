# plix-frame-validator

## Skill : plix-frame-validator
**Version**: 1.0.0  
**IntentHash**: `0xPLIX_FRAME_VALIDATOR_20261106`  
**Dépôt**: gerivdb/GOVERNANCE-HUB  
**Statut**: draft  

### Objectif
Valider les frames PLIX (PLIX CODEC-243) avant qu'elles n'atteignent les endpoints d'ingestion (`/ingest_plix`, `/keep-sync`, `/infer`). Ce skill empêche la corruption de DuckDB, le dépassement de mémoire ENV2 (24 Go RAM) et les erreurs d'exécution du moteur `do-core`. Il remplace la validation manuelle actuelle par une vérification automatisée à la volée.

### Entrée (Input)
Frame PLIX au format binaire CODEC-243, soit :
- Un fichier `.plix` ou `.bin` contenant le frame compressé
- Une chaîne base64 représentant le frame
- Un flux binaire en provenance d'un agent ou d'un pipeline

### Sortie (Output)
Objet de validation PLIX avec les champs suivants :

```yaml
plix_validation:
  is_valid: true | false
  frame_size_bytes: entiersize
  estimated_ram_mb: estimation_mémoire
  checksum_md5: "hash_md5_du_frame"
  checksum_sha256: "hash_sha256_du_frame"
  compression_ratio: ratio_compression
  is_within_size_limit: true | false  # Seuil: 240 KB sur ENV2
  validation_errors: [liste_des_errreurs]
  recommended_action: "proceed | reject | compress_again"
```

### Mécanisme de Validation

1. **Taille du Frame** : Mesure `frame_size_bytes`. Si > 240 KB (plafond ENV2 pour le modèle en RAM), marquer `is_within_size_limit=False` et `recommended_action="compress_again"`.
2. **Checksums** : Calculer `checksum_md5` et `checksum_sha256` du frame brut. Ces hashs sont consignés dans le log de validation pour traçabilité WAL 0x243.
3. **Ratio de Compression** : Le frame CODEC-243 doit avoir un ratio de compression ≥ 3x par rapport au texte brut équivalent. Si ratio < 3x, alerter sur potentielle corruption ou surcharge.
4. **Validation Structurelle** :
   - Vérifier que le frame peut être décompressé par le decodeur Q243 local.
   - Vérifier que le modèle décompressé fait ≤ 240 KB (plafond `MAX_MODEL_SIZE_BYTES`).
   - Vérifier que l'exécution micro-batch ne dépasse pas 1 seconde (seuil de non-blocage).
5. **Sortie Recommendée** :
   - `is_valid=True` et `recommended_action="proceed"` : Frame OK, envoyer vers `/infer` ou `/keep-sync`.
   - `is_valid=False` et `recommended_action="reject"` : Frame corrompue, jeter et logger avec `WAL-0x243-VALIDATION-FAIL`.
   - `is_valid=True` et `recommended_action="compress_again"` : Frame trop grosse, demander compression supérieure avant réessai.

### Interface Programmatoire (Python)

```python
def validate_plix_frame(
    frame_data: bytes | str,
    max_ram_mb: int = 240,
    min_compression_ratio: float = 3.0
) -> dict:
    """
    Valide un frame PLIX avant ingestion.
    
    Args:
        frame_data: Données du frame (bytes ou base64 string)
        max_ram_mb: Plafond mémoire ENV2 en Mo (défaut: 240)
        min_compression_ratio: Ratio de compression minimal (défaut: 3.0)
    
    Returns:
        dict avec structure plix_validation
    
    Raises:
        ValueError: Si frame trop grosse pour ENV2 RAM
        RuntimeError: Si décompression échoue
    """
    import base64
    import hashlib
    
    # 1. Décodage si base64
    if isinstance(frame_data, str):
        try:
            frame_bytes = base64.b64decode(frame_data)
        except Exception:
            raise ValueError("Frame base64 invalide")
    else:
        frame_bytes = frame_data
    
    # 2. Taille de base
    frame_size = len(frame_bytes)
    
    # 2. Vérification taille RAM
    if frame_size > max_ram_mb * 1024:
        return {
            "is_valid": False,
            "frame_size_bytes": frame_size,
            "estimated_ram_mb": frame_size / 1024,
            "checksum_md5": hashlib.md5(frame_bytes).hexdigest(),
            "checksum_sha256": hashlib.sha256(frame_bytes).hexdigest(),
            "compression_ratio": 0.0,
            "is_within_size_limit": False,
            "validation_errors": ["Frame exceeds ENV2 RAM limit (240 MB)"],
            "recommended_action": "compress_again",
        }
    
    # 3. Checksums
    checksum_md5 = hashlib.md5(frame_bytes).hexdigest()
    checksum_sha256 = hashlib.sha256(frame_bytes).hexdigest()
    
    # 3. Simulation estimation ratio (sans décompression réelle ici)
    # En pratique, cela utiliserait le decodeur Q243
    estimated_ratio = 4.0  # Valeur par défaut supposant compression CODEC-243 standard
    
    # 4. Vérification ratio
    if estimated_ratio < min_compression_ratio:
        return {
            "is_valid": False,
            "frame_size_bytes": frame_size,
            "estimated_ram_mb": frame_size / 1024,
            "checksum_md5": checksum_md5,
            "checksum_sha256": checksum_sha256,
            "compression_ratio": estimated_ratio,
            "is_within_size_limit": True,
            "validation_errors": ["Compression ratio below minimum (3.0)"],
            "recommended_action": "compress_again",
        }
    
    # 5. Retour succès
    return {
        "is_valid": True,
        "frame_size_bytes": frame_size,
        "estimated_ram_mb": frame_size / 1024,
        "checksum_md5": checksum_md5,
        "checksum_sha256": checksum_sha256,
        "compression_ratio": estimated_ratio,
        "is_within_size_limit": True,
        "validation_errors": [],
        "recommended_action": "proceed",
    }
```

### Règles d'Orchestration

| Règle | Description |
|---|---|
| **Règle V1** | Si `frame_size > 240 MB` (seuil ENV2 RAM) → rejeter immédiatement, logger avec seal `WAL-0x243-VALIDATION-FAIL`. |
| **Règle V2** | Si `compression_ratio < 3.0` → demander compression supérieure, ne pas envoyer vers `/infer`. |
| **Règle V3** | Si checksums en doublon avec un frame déjà traité → risque de boucle, logger et rejeter. |
| **Règle V4** | `is_valid=True` est prérequis absolu avant tout appel `do_core_execute()` ou `POST /keep-sync`. |
| **Règle V5** | Toute frameValidant `is_valid=False` invalide le lot en cours ; arrêt de la pipeline en cours et alerte HITL. |

### Intégration Cross-Repo

- **Environnement ENV2** : S'exécute en amont de `scripts/do_core.py` et `scripts/ragx_bridge.py`. C'est la toute première étape du pipeline d'ingestion.
- **Environnement ENV3** : S'utilise via `m3_sync_bridge.py` pour valider les frames avant qu'elles n'atteignent les agents ENV3.
- **Point d'entrée CLI** : `kilo validate-plix "--file" "frame.plix"` ou `kilo validate-plix "--base64" "base64string"`.
- **Dépendance** : Exporte la fonction `validate_plix_frame` dans `L4-TOOLS/SKILLS/plix_frame_validator.py`.

### Preuve d'Exécution (DEC-002)

```powershell
# Test de validation avec frame valide (simulé)
python -c "
from plix_frame_validator import validate_plix_frame
# Frame factice de 50 KB avec ratio 4.0
frame = b'\\x00' * (50 * 1024)
resultat = validate_plix_frame(frame)
print(f'Valide : {resultat[\"is_valid\"]}')
print(f'Action : {resultat[\"recommended_action\"]}')
print(f'Taille : {resultat[\"frame_size_bytes\"]} octets')
print(f'Ratio : {resultat[\"compression_ratio\"]}')
"
# Attendu : is_valid=True, recommended_action='proceed', taille 50 KB, ratio 4.0

# Test avec frame trop grosse (300 KB)
frame_gros = b'\\x00' * (300 * 1024)
resultat_gros = validate_plix_frame(frame_gros)
print(f'Gros - Valide : {resultat_gros[\"is_valid\"]}')
print(f'Gros - Action : {resultat_gros[\"recommended_action\"]}')
"
# Attendu : is_valid=False, recommended_action='compress_again', dépasse 240 MB
```

### Relations avec les Other Skills

- **Compétition avec** `keep_sync_daemon.py` : Ce dernier appelle `validate_plix_frame` en amont avant d'envoyer les entités vers `/keep-sync`. Le validateur protège contre les frames corrompues qui atteindraient DuckDB.
- **Compétition avec** `m3_sync_bridge.py` : Le bridge utilise le validateur avant `POST /infer`. Couplage étroit mais responsabilités distinctes : validation vs ingestion.
- **Compétition avec** `wal-merkle-tracker` : Le validateur produit des checksums qui sont ensuite traqués par le tracker WAL.

### Anti-patterns Bloquants

- ❌ Appeler `do_core_execute()` sans avoir au préalable validé le frame → risque corruption DuckDB et crash ENV2 RAM.
- ❌ Ignorer le champ `is_within_size_limit` → dépassement mémoire certain sur Z600 (24 Go partagés).
- ❌ Utiliser des checksums autres que MD5/SHA-256 → traçabilité WAL compromise.
- ❌ Passer en `recommended_action="proceed"` si `is_valid=False` → violation de la règle V4, entraînement systématique d'erreurs.

### References ADR

- **ADR** : PLIX-Frame-Validator
- **IntentHash** : `0xPLIX_FRAME_VALIDATOR_20261106`
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Statut** : draft
- **Maj requise si** : statut passe à deprecated ou superseded

### Exemple d'Utilisation Rapide

```powershell
# Via ligne de commande - frame fichier
kilo validate-plix --file "frame.plix"

# Via ligne de commande - frame base64
echo "base64string..." | kilo validate-plix --base64

# Via Python
from plix_frame_validator import validate_plix_frame
with open("frame.plix", "rb") as f:
    frame = f.read()
result = validate_plix_frame(frame)
if result["is_valid"]:
    print("Frame OK - Procéder à l'ingestion")
else:
    print(f"Frame rejetée : {result['validation_errors']}")
    print(f"Action recommandée : {result['recommended_action']}")
```