# keep-entity-normalizer

## Skill : keep-entity-normalizer
**Version**: 1.0.0  
**IntentHash**: `0xKEEP_ENTITY_NORMALIZER_20261106`  
**Dépôt**: gerivdb/GOVERNANCE-HUB  
**Statut**: draft  

### Objectif
Automatiser la construction du schéma `KeepEntity` à partir de n'importe quel texte ou document Markdown, en y adjoignant automatiquement le sceau WAL, le hash SHA-256 anti-boucle et les métadonnées de strate. Ce skill élimine la construction manuelle du schéma et garantit la cohérence structurelle à chaque création d'entité Keep.

### Entrée (Input)
Tout texte brut ou document Markdown contenant des marqueurs de saillance `[KEEP]`. Format accepté :
- Texte libre avec balises `[KEEP]` identifiant les entités à créer
- Fichiers Markdown complets (frontmatter YAML optionnel)
- Sortie d'autres agents ou moteurs (PLIX, ADMG-ML, etc.)

### Sortie (Output)
Objet JSON validé `KeepEntity` avec les champs suivants :

```yaml
keep_entity:
  entity_id: "UUID-v4 généré ou entré"
  timestamp: "ISO-8601 UTC"
  strate_origin: "ENV3.pur" | "ENV2" | "ENV6"
  metadata:
    title: "Titre de l'intention ou du PRD-MOC"
    labels: ["SSoT", "ENV3", "KeepEntity", "Orbite-1b"]
    color_code: "M3_STANDARD_BLUE"
    pinned: true
  content:
    body_text: "Corps de la note structuré en Markdown"
    checklist_items:
      - item_id: 1
        text: "Tâche validée"
        checked: true
      - item_id: 2
        text: "Tâche en attente"
        checked: false
  governance:
    friction: 0.0
    entropy: 0.0
    merkle_seal: "WAL-0x243-KEEP-ENTITY-PASS"
    hash_sha256: "sha256(title + body_text)"
```

### Mécanisme de Normalisation

1. **Détection SST** : Scanne l'entrée à la recherche du mot-clé `[KEEP]`. Si absent, retourne erreur `SST < 5` (score de saillance ternaire insuffisant).
2. **Extraction Titres** : Le premier bloc de texte structuré devient `title`. Si frontmatter YAML présent, utilise `title:` du frontmatter.
3. **Extraction Corps** : Tout le texte restant (après suppression du titre et des marqueurs `[KEEP]`) devient `body_text`.
4. **Calcul Hash** : `hash_sha256 = sha256(f"{title}{body_text}")`. Ce hash est stocké en contrainte UNIQUE dans DuckDB (Mandat 3 anti-boucle).
5. **Sceau WAL** : `merkle_seal = "WAL-0x243-KEEP-ENTITY-PASS"`.
6. **Attribution Strate** : `strate_origin` déduit du répertoire source ou précisé explicitement.

### Interface Programmatoire (Python)

```python
def normalize_keep_entity(
    raw_text: str,
    strate: str = "ENV3.pur",
    generate_id: bool = True
) -> dict:
    """
    Normalise un texte brut en entité KeepEntity complète.
    
    Args:
        raw_text: Texte brut, potentiellement avec marqueurs [KEEP]
        strate: Strate d'origine (ENV3.pur, ENV2, ENV6, etc.)
        generate_id: Si True, génère UUID-v4; sinon attend un ID dans le texte
    
    Returns:
        dict conforme au schéma KeepEntity
    
    Raises:
        ValueError: Si pas de marqueur [KEEP] détecté
        TypeError: Si le texte est vide
    """
    # 1. Vérification SST
    if "[KEEP]" not in raw_text:
        raise ValueError("SST < 5 : marqueur [KEEP] absent — entité non créée")
    
    # 2. Extraction du titre
    # Cherche la première ligne structurée ou le frontmatter YAML
    title = extract_title(raw_text)
    
    # 3. Extraction du corps (tout le reste)
    body_text = extract_body(raw_text, title)
    
    # 4. Calcul hash SHA-256
    hash_sha256 = hashlib.sha256(f"{title}{body_text}".encode("utf-8")).hexdigest()
    
    # 5. Construction de l'entité
    entity_id = str(uuid.uuid4()) if generate_id else extract_entity_id(raw_text)
    
    return {
        "entity_id": entity_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "strate_origin": strate,
        "metadata": {
            "title": title,
            "labels": ["SSoT", "KeepEntity", "Orbite-1b"],
            "color_code": "M3_STANDARD_BLUE",
            "pinned": True,
        },
        "content": {
            "body_text": body_text,
            "checklist_items": [],
        },
        "governance": {
            "friction": 0.0,
            "entropy": 0.0,
            "merkle_seal": "WAL-0x243-KEEP-ENTITY-PASS",
            "hash_sha256": hash_sha256,
        },
    }
```

### Règles d'Orchestration

| Règle | Description |
|---|---|
| **Règle N1** | Si `generate_id=True` et ID déjà présent dans DuckDB (`hash_sha256`), retourner l'entité existante sans la recréer (déduplication Mandat 3). |
| **Règle N2** | Si `generate_id=False` et ID absent → générer UUID-v4 et le stocker avec le hash. |
| **Règle N3** | Si friction ou entropie détectée dans le texte source → lever warning mais tout de même créer l'entité (friction 0.0 est la norme). |
| **Règle N4** | Le `merkle_seal` est toujours `WAL-0x243-KEEP-ENTITY-PASS` à moins d'explicite override HITL. |
| **Règle N5** | Output JSON validé contre le schéma `keep_entity_schema.json` avant tout envoi vers DuckDB ou NotebookLM. |

### Intégration Cross-Repo

- **Environnement ENV3** : S'appelle depuis `m3_sync_bridge.py` ou tout agent ENV3 qui doit créer une entité Keep.
- **Environnement ENV2** : S'appelle depuis `scripts/keep_sync_daemon.py` lors de la lecture du queue JSONL.
- **Point d'entrée CLI** : `kilo normalize-keep "--text" "mon texte [KEEP]" --strate ENV3.pur`
- **Dépendance** : Exporte la fonction `normalize_keep_entity` dans le module partagé `L4-TOOLS/SKILLS/keep_entity_normalizer.py`.

### Preuve d'Exécution (DEC-002)

```powershell
# Test du normalisateur
python -c "
from keep_entity_normalizer import normalize_keep_entity
texte = '''[KEEP] Mémo PRD-MOC Orbite 1b
Définition de l'Orbite 1b et du bus transverse -b.'''
entite = normalize_keep_entity(texte, strate='ENV3.pur')
print(f'ID: {entite[\"entity_id\"]}')
print(f'Hash: {entite[\"governance\"][\"hash_sha256\"][:16]}...')
print(f'Merkle: {entite[\"governance\"][\"merkle_seal\"]}')
"
# Attendu : ID généré, hash SHA-256 complet, merkle_seal WAL-0x243-KEEP-ENTITY-PASS
```

### Relations avec les Other Skills

- **Compétition avec** `m3_sync_bridge.py` : Ce dernier utilise la sortie de `keep-entity-normalizer` pour créer les entités. Pas de conflit, mais dépendance.
- **Compétition avec** `keep_sync_daemon.py` : Ce dernier lit les entités normalisées depuis le queue JSONL. Le normalisateur pourrait aussi enrichir les anciennes entrées non normalisées.
- **Compétition avec** `validation-checklist` : Le normalisateur vérifie la structure avant ; la checklist vérifie le contenu après.

### Anti-patterns Bloquants

- ❌ Utiliser le normalisateur sans vérifier le marqueur `[KEEP]` → erreur SST.
- ❌ Utiliser un hash SHA-256 autre que `sha256(title + body_text)` → risque de collision et de boucle de synchronisation.
- ❌ Définir `merkle_seal` personnellement sans override HITL → violation de la politique WAL.
- ❌ Sortir du fichier sans validation JSON contre `keep_entity_schema.json` → risque de corruption DuckDB.

### References ADR

- **ADR** : Keep-Entity-Normalizer-Schema
- **IntentHash** : `0xKEEP_ENTITY_NORMALIZER_20261106`
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Maj requise si** : statut passe à deprecated ou superseded

### Exemple d'Utilisation Rapide

```powershell
# Déclaration rapide depuis ligne de commande
echo "[KEEP] Ma nouvelle intention de suivi" | kilo normalize-keep --strate ENV3.pur

# Via Python
python -c "
from keep_entity_normalizer import normalize_keep_entity
e = normalize_keep_entity('[KEEP] Mon titre', strate='ENV2')
print(f'Prêt à stocker : {e[\"entity_id\"]}')
"
```