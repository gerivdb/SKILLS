# Skill : gas-rest-deployer

## Objectif
Déployer une application Web Google Apps Script via l'API REST v1 (`projects.deployments.create`) avec le payload exact et la casse correcte, afin d'éviter les erreurs de validation Google (400 Bad Request) liées à des noms de champs incorrects.

## Contexte
Le déploiement GAS a échoué chez Shard D car le payload JSON utilisait des noms de champs incorrects (ex: `type` au lieu de `deploymentConfig`, `accessLevel: "ANYONE"` au lieu de `ANYONE_ANONYMOUS`). L'API Apps Script v1 exige des noms et des valeurs d'énumération précis.

## Payload exact pour `POST /v1/projects/{scriptId}/deployments`

### Requête

```http
POST https://script.googleapis.com/v1/projects/{scriptId}/deployments
Authorization: Bearer <access_token>
Content-Type: application/json
```

```json
{
  "deploymentConfig": {
    "versionNumber": 2,
    "manifestFileName": "appsscript",
    "description": "Starfleet Bridge v1 - Web App Public",
    "webappConfig": {
      "accessLevel": "ANYONE_ANONYMOUS",
      "executeAs": "USER_DEPLOYING"
    }
  }
}
```

### Champs obligatoires

| Champ | Type | Valeur | Description |
|-------|------|--------|-------------|
| `deploymentConfig.versionNumber` | integer | ≥ 1 | Numéro de version du manifeste à déployer |
| `deploymentConfig.manifestFileName` | string | `"appsscript"` | Nom du fichier de manifeste (sans extension) |
| `deploymentConfig.description` | string | libre | Description du déploiement |
| `deploymentConfig.webappConfig.accessLevel` | string | `"ANYONE_ANONYMOUS"` | Accès public (requis pour Web App accessible sans auth) |
| `deploymentConfig.webappConfig.executeAs` | string | `"USER_DEPLOYING"` | Exécuter sous l'identité du déployeur |

### Valeurs d'énumération critiques (casse exacte)

| Champ | Valeur correcte | Valeur incorrecte (à éviter) |
|-------|----------------|-------------------------------|
| `accessLevel` | `ANYONE_ANONYMOUS` | `ANYONE`, `public`, `ME`, `DOMAIN` |
| `executeAs` | `USER_DEPLOYING` | `USER_DEPLOYING` (case-sensitive) |
| `manifestFileName` | `appsscript` | `appsscript.json`, `manifest` |

### Réponse attendue (200 OK)

```json
{
  "deploymentId": "AKfycbXXXXXXXXXXXXXXXXXXXXXXXX",
  "deploymentConfig": {
    "versionNumber": 2,
    "manifestFileName": "appsscript",
    "description": "Starfleet Bridge v1 - Web App Public",
    "webappConfig": {
      "accessLevel": "ANYONE_ANONYMOUS",
      "executeAs": "USER_DEPLOYING"
    }
  }
}
```

L'URL de l'application Web est :
```
https://script.google.com/macros/s/<deploymentId>/exec
```

## Procédure de déploiement

### Étape 1 — Obtenir un access_token valide

```powershell
# Via le fichier .clasprc.json (clasp)
$config = Get-Content ~/.clasprc.json -Raw | ConvertFrom-Json
$token = $config.tokens.default.access_token
```

Ou via OAuth 2.0 directement :
```powershell
# Refresh token si nécessaire
$refresh_token = $config.tokens.default.refresh_token
$client_id = "<votre-client-id>"
$client_secret = "<votre-client-secret>"

$response = Invoke-RestMethod -Uri "https://oauth2.googleapis.com/token" -Method Post -Body @{
    grant_type = "refresh_token"
    client_id = $client_id
    client_secret = $client_secret
    refresh_token = $refresh_token
} -ContentType "application/x-www-form-urlencoded"

$token = $response.access_token
```

### Étape 2 — Créer le déploiement

```powershell
$scriptId = "1mJB9exCXXXSv1brFLV4T77-bUgx5R3yEncmmkcCpEaSeJ14wHyw9KihM"
$token = "<ACCESS_TOKEN>"

$body = @{
    deploymentConfig = @{
        versionNumber = 2
        manifestFileName = "appsscript"
        description = "Starfleet Bridge v1 - Web App Public"
        webappConfig = @{
            accessLevel = "ANYONE_ANONYMOUS"
            executeAs = "USER_DEPLOYING"
        }
    }
} | ConvertTo-Json -Depth 3

$response = Invoke-RestMethod -Uri "https://script.googleapis.com/v1/projects/$scriptId/deployments" `
    -Method Post `
    -Headers @{ Authorization = "Bearer $token" } `
    -ContentType "application/json" `
    -Body $body

$response.deploymentId
```

### Étape 3 — Tester l'URL déployée

```powershell
$execUrl = "https://script.google.com/macros/s/$($response.deploymentId)/exec"

$payload = @{
    target_execution_env = "ENV3_STARFLEET"
    intent_hash = "0xTEST_PRD_BLUEPRINT_20261111"
    source_document = "test_prd_moc.md"
    blueprint_version = "1.0"
    compiler_version = "0.1.0"
} | ConvertTo-Json

$resp = Invoke-RestMethod -Uri $execUrl -Method Post -ContentType "application/json" -Body $payload
$resp.status  # Doit retourner "success"
$resp.seal    # Doit retourner "WAL-0x282-POLE-1-BRIDGE-INGESTION"
```

## Erreurs courantes

| Erreur | Cause | Correction |
|--------|-------|------------|
| `400 Bad Request: Invalid JSON payload` | `webappConfig` au lieu de `webappConfig` ou champ manquant | Vérifier les noms de champs exactement |
| `400 Bad Request: Invalid value for accessLevel` | `ANYONE` au lieu de `ANYONE_ANONYMOUS` | Utiliser `ANYONE_ANONYMOUS` |
| `400 Bad Request: Invalid value for executeAs` | Valeur incorrecte | Utiliser `USER_DEPLOYING` |
| `403 Forbidden` | Token expiré ou scopes manquants | Rafraîchir le token, vérifier les scopes `https://www.googleapis.com/auth/script.deployments` |

## Invariants de stase

- $\mathcal{F} = 0.0$ : aucune dérive fonctionnelle ; le payload suit exactement la spécification API Google Apps Script v1
- $\mathcal{H} = 0.0$ : aucune hallucination de spécification ; les noms de champs et valeurs d'énumération sont copiés depuis la documentation officielle

## Référence ADR
- **ADR** : ADR-2026-06-07-001-ADR-GOVERNANCE-GATE (règle BDCP)
- **Interdiction** : utilisation de `--no-verify` ou de payloads incorrects qui nécessiteraient des tentatives répétées
