---
type: SKILL
version: "1.0.0"
intent_hash: 0xCLASPR_FULL_WORKFLOW_20261102
name: claspr-full-workflow
role: meta
wal_id: WAL-0x243
depends_on: claspr-clapet-guard, claspr-auth-guard, claspr-atomic-deploy, claspr-safe-deploy, claspr-git-sync
friction: 0.0
entropy: 0.0
---

# Skill - claspr-full-workflow

## Role

Meta-skill orchestrant la chaine complete de deploiement CLASPR : clapet -> auth -> deploy -> sync -> push -> nettoyage. Invoque les 5 skills precedents en sequence.

## Declencheur

Une demande de deploiement complet des modules GAS vers le projet Google Apps Script distant.

## Protocole obligatoire

### Sequence d'execution

| Ordre | Skill | Action |
|-------|-------|--------|
| 1 | claspr-clapet-guard | Verifier clapet fermee |
| 2 | claspr-auth-guard | Verifier .clasprc.json valide |
| 3 | claspr-atomic-deploy | Deployer les fichiers .gs (max 3) |
| 4 | claspr-safe-deploy | Verifier remote, branche, historique |
| 5 | claspr-git-sync | Synchroniser local/distant |
| 6 | Nettoyage | Supprimer fichiers temporaires, caches obsoletes |

## Gestion d'erreur

Si un skill renvoie un code de sortie non-nul, le workflow s'arrete immediatement et un sceau WAL d'erreur est emis. Aucun pas suivant n'est execute.

## Interdictions absolues

- L'agent ne peut JAMAIS ouvrir le clapet BDCP sans instruction explicite (ouvre le clapet, passe en FREE, desactive BDCP)
- L'agent ne peut JAMAIS executer clasp login (flux OAuth interactif)
- L'agent ne peut JAMAIS utiliser --force sur un push

## Sceau WAL

WAL-0x243-CLASPR-FULL-WORKFLOW (RC = 0, F = 0.0, H = 0.0)

## Voûte de Référence SSoT

[GOUV](https://gemini.google.com/notebook/83e23803-655d-4f3b-9e40-db7e45f8cad4)