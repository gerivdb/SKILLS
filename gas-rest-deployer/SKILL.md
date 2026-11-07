---
type: SKILL
version: 1.0.0
intent_hash: 0xSKILL_GAS_REST_DEPLOYER_20261105
---

# Skill : gas-rest-deployer

## Rôle
Déployer des fichiers `.gs` et le manifeste `appsscript.json` vers un projet Google Apps Script distant via l'API REST (`PUT /projects/{scriptId}/content`), puis créer une version et un déploiement Web App, sans dépendre de `clasp`.

## Triggers
- "déployer GAS"
- "push script Google Apps Script"
- "API REST projects/content"
- "créer version GAS"
- "déploiement Web App GAS"

## Entrée
- `scriptId` : ID du projet GAS
- `accessToken` : token OAuth2 (via refresh_token ou clasprc)
- `files` : tableau `{ name, type, source }` (type `SERVER_JS` ou `JSON`)
- `description` : description de version

## Sortie
- `versionNumber`
- `deploymentId`
- `webAppUrl`

## Structure
```
scripts/gas-rest-deployer/
├── deploy.ps1          # Orchestration PowerShell (PUT content → versions → deployments)
├── deploy.ps1.md       # Documentation d'usage
└── SKILL.md            # Métadonnées du skill (ce fichier)
```

## Exemple
```powershell
.\scripts\gas-rest-deployer\deploy.ps1 -ScriptId "1fRGLY4S..." -Files @("AntiSlop-Auditor.gs", "sync-veille-to-google-services.gs", "appsscript.json") -Description "Pont RAGX via tunnel Cloudflare"
```

## Contraintes
- Le `PUT /content` remplace l'intégralité du projet — tous les fichiers doivent être envoyés en une seule requête
- Ne jamais utiliser `gh repo create` (interdit par BDCP)
- Utiliser `git remote set-url` + `git push` (pas `gh`)

## Référence ADR
- **ADR** : ADR-094-git-remote-safety-protocol
- **IntentHash** : 0xGIT_REMOTE_SAFETY_20260619
