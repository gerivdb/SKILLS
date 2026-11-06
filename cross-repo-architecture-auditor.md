# cross-repo-architecture-auditor

## Skill : cross-repo-architecture-auditor
**Version**: 1.0.0  
**IntentHash**: `0xCROSS_REPO_AUDITOR_20261106`  
**Dépôt**: gerivdb/GOVERNANCE-HUB  
**Statut**: draft  

### Objectif
Auditer la cohérence architecturale entre ENV3 (spécifications, PRD-MOC, SOT) et ENV2 (implémentation locale, code réel, DuckDB schema). Ce skill détecte les dérives déclaratives, les écarts de schéma, les IDs faux (comme le faux NotebookLM ID `16be1ada-...`), et toute divergence qui pourrait entraîner des boucles de synchronisation ou des pertes de données. Il s'exécute automatiquement après toute modification cross-repo et avant tout push vers ENV0.

### Entrée (Input)
L'auditeur accepte plusieurs types d'entrée :
- **Diff de modifications** : `git diff` récent ou patch file.
- **Registre cible** : Chemin vers `gerivdb/GOVERNANCE-HUB/known_repositories.yaml`.
- **État local** : Chemin vers l'implémentation ENV2 en cours (`D:\DO\WEB\TOOLS\L0-CANON\ENV3-repo`).
- **Mode comparaison** : `env3_vs_env2`, `sot_vs_impl`, `id_vs_code`, `full_audit`.

### Sortie (Output)
Rapport d'audit architecturale structuré :

```yaml
cross_repo_audit:
  audit_id: "UUID-v4"
  timestamp: "ISO-8601 UTC"
  mode: "env3_vs_env2 | sot_vs_impl | id_vs_code | full_audit"
  
  ecarts_identifies:
    - type: "ID_faux | Schema_divergence | Path_erroné | WAL_mismatch"
      gravité: "critical | warning | info"
      description: "Description détaillée de l'écart"
      localisation: "Fichier/ligne/colonne concernée"
      recommandation: "Action corrective suggérée"
  
  conformite_global:
    score_conformite: percentage 0-100
    frottement_engendré: "0.0 | > 0.0 si écarts non résolus"
    entropie_engendrée: "0.0 | > 0.0 si écarts non résolus"
    statut: "compatible | dérive_détectée | critical"
  
  actions_recommandees:
    - type: "mettre_a_jour_id | corriger_schéma | synchroniser_registry | commit_avertissement"
      priorité: "high | medium | low"
      description: "Action à engager"
  
  sceau_wal: "WAL-0x243-CROSS-REPO-AUDIT-PASS"
```

### Mécanisme d'Audit

1. **Chargement SOT** : Lecture de `gerivdb/GOVERNANCE-HUB/known_repositories.yaml`. Extraction de tous les IDs, schémas, paths déclarés.
2. **Inspection Implémentation** : Analyse statique du code ENV2 en cours. Recherche des patterns d'IDs, schémas DuckDB, paths de fichiers, URLs de services.
3. **Comparaison par Type** :
   - **ID_faux** : Tout ID connu (NotebookLM, KeepEntity, UUID) présent dans le code ENV2 mais introuvable ou différent dans le SOT GOVERNANCE-HUB.
   - **Schema_divergence** : Schéma DuckDB (`inference_runs`, `keep_entities`) diffère de la définition dans le PRD-MOC ou les migrations.
   - **Path_erroné** : Paths locaux codés en dur qui divergent des paths déclarés dans `known_repositories.yaml`.
   - **WAL_mismatch** : Sceaux WAL incohérents entre migrations, scripts et code réel.
4. **Calcul du Score de Conformité** :
   - Part de départ: 100%
   - Moins 10% par écart critical détecté
   - Moins 5% par écart warning détecté
   - Plus 0% par info notées
   - Résultat: `score_conformite` final.
5. **Génération du Rapport** : Fichier Markdown avec tous les écarts, localisations et recommandations. Signature WAL `WAL-0x243-CROSS-REPO-AUDIT-PASS`.

### Interface Programmatoire (Python)

```python
def audit_cross_repo(
    mode: str = "full_audit",
    sot_path: str = "gerivdb/GOVERNANCE-HUB/known_repositories.yaml",
    impl_path: str = None,
    generate_report: bool = True
) -> dict:
    """
    Effectue un audit cross-repo ENV3 vs ENV2.
    
    Args:
        mode: Type d'audit à effectuer.
        sot_path: Chemin vers le registre SOT (GOVERNANCE-HUB).
        impl_path: Chemin vers l'implémentation ENV2 (défaut: répertoire courant).
        generate_report: Si True, génère le rapport Markdown.
    
    Returns:
        dict structure cross_repo_audit.
    
    Raises:
        FileNotFoundError: Si le fichier SOT introuvable.
        ValueError: Si mode invalide.
    """
    import yaml
    import json
    import hashlib
    from pathlib import Path
    
    # 1. Chargement SOT
    sot_file = Path(sot_path)
    if not sot_file.exists():
        raise FileNotFoundError(f"Fichier SOT introuvable : {sot_path}")
    
    with open(sot_file, "r", encoding="utf-8") as f:
        sot_content = yaml.safe_load(f)
    
    # Extraction des IDs et schémas du SOT
    sot_ids = extract_sot_ids(sot_content)
    sot_schemas = extract_sot_schemas(sot_content)
    sot_paths = extract_sot_paths(sot_content)
    
    # 2. Inspection implémentation
    if impl_path is None:
        impl_path = Path(".")
    else:
        impl_path = Path(impl_path)
    
    if not impl_path.exists():
        raise FileNotFoundError(f"Chemin implémentation introuvable : {impl_path}")
    
    # Analyse statique du code ENV2
    impl_ids = extract_impl_ids(impl_path)
    impl_schemas = extract_impl_schemas(impl_path)
    impl_paths = extract_impl_paths(impl_path)
    
    # 3. Comparaison
    ecarts = []
    
    # --- Vérification des IDs ---
    for id_name, id_value in sot_ids.items():
        if id_name in impl_ids:
            if impl_ids[id_name] != id_value:
                ecarts.append({
                    "type": "ID_faux",
                    "gravité": "critical",
                    "description": f"ID '{id_name}' différent : SOT={id_value}, ENV2={impl_ids[id_name]}",
                    "localisation": "Code ENV2 référence " + id_name,
                    "recommandation": "Mettre à jour l'ID dans le code pour correspondre au SOT",
                })
    
    # --- Vérification des schémas ---
    for schema_name, schema_def in sot_schemas.items():
        if schema_name in impl_schemas:
            if impl_schemas[schema_name] != schema_def:
                ecarts.append({
                    "type": "Schema_divergence",
                    "gravité": "critical",
                    "description": f"Schema '{schema_name}' divergent entre SOT et implémentation ENV2",
                    "localisation": "DuckDB schema / PRD-MOC",
                    "recommandation": "Régulariser le schema DuckDB avec la définition du PRD-MOC",
                })
    
    # --- Vérification des paths ---
    for path_name, path_def in sot_paths.items():
        if path_name in impl_paths:
            if impl_paths[path_name] != path_def:
                ecarts.append({
                    "type": "Path_erroné",
                    "gravité": "warning",
                    "description": f"Path '{path_name}' divergent : SOT={path_def}, ENV2={impl_paths[path_name]}",
                    "localisation": "Chemins codés en dur dans le code ENV2",
                    "recommandation": "Remplacer par les paths du SOT ou configurer via variables d'environnement",
                })
    
    # 4. Calcul score de conformité
    score = 100
    for écart in ecarts:
        if écart["gravité"] == "critical":
            score -= 10
        elif écart["gravité"] == "warning":
            score -= 5
    
    score = max(score, 0)
    
    # 5. Construction du rapport
    rapport = {
        "audit_id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "mode": mode,
        "ecarts_identifies": ecarts,
        "conformite_global": {
            "score_conformite": score,
            "frottement_engendré": "0.0" if score >= 80 else "> 0.0",
            "entropie_engendrée": "0.0" if score >= 80 else "> 0.0",
            "statut": "compatible" if score >= 80 else ("dérive_détectée" if score >= 50 else "critical"),
        },
        "actions_recommandees": generer_actions(ecarts),
        "sceau_wal": "WAL-0x243-CROSS-REPO-AUDIT-PASS",
    }
    
    if generate_report:
        generer_fichier_rapport_markdown(rapport)
    
    return rapport
```

### Règles d'Orchestration

| Règle | Description |
|---|---|
| **Règle A1** | L'audit est obligatoire après toute modification touchant plus d'un repo (Pattern E). |
| **Règle A2** | Si `score_conformite < 80` → blocage du push vers ENV0. HITL requis pour forcer le passage. |
| **Règle A3** | Si `ID_faux` détecté → arrêt immédiat, ne pas attendre la fin de l'audit. |
| **Règle A4** | Le `sceau_wal` `WAL-0x243-CROSS-REPO-AUDIT-PASS` doit être présent dans tout fichier de rapport généré. |
| **Règle A5** | Les écarts `critical` doivent être résolus avant tout autre travail sur le repo concerné. |

### Intégration Cross-Repo

- **Environnement ENV0 (GitHub)** : S'exécute dans le CI pipeline avant tout merge. Bloque les merges avec score < 80.
- **Environnement ENV2** : S'exécute en tant que `kilo audit-cross-repo` avant tout déploiement ou commit impliquant plusieurs repos.
- **Environnement ENV3** : Utilise les résultats pour valider que les nouvelles spécifications PRD-MOC sont cohérentes avec l'implémentation locale.
- **Point d'entrée CLI** : `kilo audit-cross-repo --mode full_audit` ou `kilo audit-cross-repo --mode id_vs_code`.
- **Dépendance** : S'appuie sur `gerivdb/GOVERNANCE-HUB/known_repositories.yaml`, `L4-TOOLS/SKILLS/keep-entity-normalizer.py`, `L4-TOOLS/SKILLS/plix-frame-validator.py`.

### Preuve d'Exécution (DEC-002)

```powershell
# Audit cross-repo complet
kilo audit-cross-repo --mode full_audit

# Résultat attendu (extrait) :
# [CROSS-REPO AUDIT] Début audit complet ENV3 vs ENV2
# [CROSS-REPO AUDIT] 3 écarts critiques identifiés :
#   - ID_faux : ID NotebookLM 16be1ada... vs attendu f4b58197...
#   - Schema_divergence : Schéma keep_entities manquant colonne hash_sha256
#   - Path_erroné : Path Windows codé en dur vs path attendu Linux
# [CROSS-REPO AUDIT] Score de conformité : 70/100 (détecte)
# [CROSS-REPO AUDIT] Actions recommandées : Corriger les 3 écarts critiques
# [CROSS-REPO AUDIT] Sceau WAL : WAL-0x243-CROSS-REPO-AUDIT-PASS
# [CROSS-REPO AUDIT] Audit terminé. Push vers ENV0 BLOQUÉ jusqu'à résolution.

# Audit ciblé sur les IDs seulement
kilo audit-cross-repo --mode id_vs_code

# Résultat attendu :
# [CROSS-REPO AUDIT] Vérification des IDs seuls
# [CROSS-REPO AUDIT] 1 ID faux détecté : NotebookLM
# [CROSS-REPO AUDIT] Score de conformité : 90/100
# [CROSS-REPO AUDIT] Sceau WAL : WAL-0x243-CROSS-REPO-AUDIT-PASS
```

### Relations avec les Other Skills

- **Compétition avec** `keep-entity-normalizer` : Le normalisateur crée les entités cohérentes ; l'auditeur vérifie qu'elles restent cohérentes après coup. Ils travaillent en paire : création → validation.
- **Compétition avec** `plix-frame-validator` : Le validateur vérifie les frames avant ingestion ; l'auditeur vérifie l'architecture globale après coup. Ils se complètent sur la prévention des erreurs.
- **Compétition avec** `validation-checklist` : La checklist vérifie le contenu d'une entité ou frame ; l'auditeur vérifie l'architecture qui les contient. Niveau d'abstraction différent.
- **Compétition avec** `act-validate-intent` : L'validateur d'intent vérifie une intention unique ; l'auditeur vérifie la cohérence globale cross-repo.

### Anti-patterns Bloquants

- ❌ Exécuter l'audit sans mode `full_audit` ou `id_vs_code` spécifié → audit incomplet.
- ❌ Ignorer les écarts `critical` → risque de boucle de synchronisation Keep↔DuckDB↔NotebookLM.
- ❌ Pusher vers ENV0 avec `score_conformite < 80` → violation de la règle A2, entraînement de dettes architecturale.
- ❌ Générer le rapport sans le sceau WAL `WAL-0x243-CROSS-REPO-AUDIT-PASS` → rapport non valide, traçabilité compromise.

### References ADR

- **ADR** : Cross-Repo-Architect-Auditor
- **IntentHash** : `0xCROSS_REPO_AUDITOR_20261106`
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Statut** : draft
- **Maj requise si** : statut passe à deprecated ou superseded

### Exemple d'Utilisation Rapide

```powershell
# Audit complet - identification depuis le répertoire courant
kilo audit-cross-repo

# Audit ciblé sur les IDs seulement
kilo audit-cross-repo --mode id_vs_code

# Via Python
from cross_repo_auditor import audit_cross_repo
rapport = audit_cross_repo(mode="full_audit")
print(f"Score : {rapport['conformite_global']['score_conformite']}%")
print(f"Statut : {rapport['conformite_global']['statut']}")
for écart in rapport["ecarts_identifies"]:
    print(f" - [{écart['gravité']}] {écart['type']} : {écart['description'][:60]}...")
```

### Patterns d'Integration dans le Pipeline WiCi

Le skill `cross-repo-architecture-auditor` s'insère dans le pipeline WiCi comme étape de **gatekeeper** :

```
Pipeline WiCi :
1. Concept → PRD-MOC (ENV3)
2. Implémentation (ENV2) → 3 skills : normalize, validate, audit
3. Audit cross-repo (obligatoire, blocage si score < 80)
4. Migration DuckDB + KeepEntity
5. Sync vers NotebookLM (Phase 3)
6. Push ENV0 (bloqué si audit non passé)
```

Cela garantit que aucune dérive architecturale ne traverse les mailles du filet, et que les 158 skills du registre évoluent dans un cadre de cohérence tracée par les sceaux WAL.

### Patterns d'Utilisation Rapide

```powershell
# Après avoir modifié des fichiers impliquant ENV2 et ENV3
kilo audit-cross-repo

# Si l'audit bloque (score < 80)
# → Résoudre les écarts critiques affichés
# → Relancer audit
# → Une fois score >= 80
git add .
git commit -m "fix: resolve cross-repo audit critical gaps"
git push origin main
```