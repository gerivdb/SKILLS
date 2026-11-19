---
type: skill
version: "1.0.0"
status: active
intent_hash: 0xSKILL_M3_STUB_DETECTOR_20261119
---

# skill.m3.stub-detector — Détection de stubs menteurs

## Objectif

Scanner un dépôt cible pour détecter les **stubs menteurs** (`return {"status": "ok"}` en dur, `NotImplementedError` avec docstring `[TODO]`) et générer un rapport structuré prêt à être consommé par le `citizen.stub-eradicator`.

Ce skill est le premier maillon de la chaîne autopoïétique : il ne corrige rien, il détecte uniquement.

## Déclencheur

Toute demande d'audit d'un dépôt pour détecter des stubs menteurs, ou toute exécution planifiée (cron nightly) du `citizen.stub-eradicator`.

## Règles obligatoires

### 1. Entrée unique
Le skill reçoit un chemin de dépôt cible en argument. Aucun autre paramètre n'est requis.

### 2. Détection par pattern texte (stdlib uniquement)
Scanner récursivement tous les fichiers `.py` du dépôt cible. Détecter :
- `return {"status": "ok"` (stub menteur retournant un statut ok en dur)
- `raise NotImplementedError` combiné avec une docstring contenant `[TODO]`
- Tout bloc `return` contenant uniquement des valeurs en dur sans appel réseau réel

### 3. Zéro dépendance externe
Utiliser exclusivement la bibliothèque standard Python (`os`, `re`, `sys`, `json`). Aucune installation pip requise.

### 4. Rapport structuré JSON
Générer un rapport JSON avec les champs suivants :
- `depot` : chemin du dépôt scanné
- `date_scan` : horodatage UTC ISO-8601
- `total_fichiers_py` : nombre de fichiers .py analysés
- `stubs_detectes` : liste des fichiers contenant des stubs, avec pour chacun :
  - `chemin` : chemin relatif du fichier
  - `ligne` : numéro de ligne du stub
  - `pattern` : pattern détecté (`status_ok`, `not_implemented_todo`)
  - `contenu_ligne` : texte de la ligne incriminée
- `synthese` : nombre total de stubs détectés

### 5. Aucune modification
Le skill est en lecture seule. Il ne modifie aucun fichier du dépôt cible.

## Contrat de sortie

```json
{
  "depot": "D:/DO/WEB/TOOLS/L4-TOOLS/EXEMPLE",
  "date_scan": "2026-11-19T06:XX:XXZ",
  "total_fichiers_py": 42,
  "stubs_detectes": [
    {
      "chemin": "src/mon_module.py",
      "ligne": 18,
      "pattern": "status_ok",
      "contenu_ligne": "        return {\"status\": \"ok\"}"
    }
  ],
  "synthese": {
    "total_stubs": 1
  }
}
```

## Antipatterns bloqués

- Ne jamais supprimer ou modifier un fichier lors de la détection (réservé à l'éradicateur).
- Ne jamais utiliser de dépendance externe (pip, npm, etc.).
- Ne jamais ignorer un fichier `.py` sans raison documentée.

## Fichier de référence

- `D:\DO\WEB\TOOLS\L3-CITIZENS\CITIZENS\citizen.stub-eradicator` : consommateur du rapport généré par ce skill.

## Référence ADR

- **ADR** : ADR-2026-11-19-001-autopoietic-stub-eradication
- **IntentHash** : 0xAUTOPOIETIC_STUB_ERADICATION_20261119
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed
