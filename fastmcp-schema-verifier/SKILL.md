---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_FMSV_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/fastmcp-schema-verifier/SKILL.md
---

# Skill - fastmcp-schema-verifier

## Objectif

Verifier la conformite des schemas d'outils FastMCP (inputSchema, types Pydantic) avant exposition sur le Gateway unifie. Garantit que tout outil declare respecte la spec JSON-RPC 2.0 et peut etre serialise sans erreur.

## Declencheur

- Declaration d'un nouvel outil FastMCP sur le gateway.
- Modification d'un schema inputSchema existant.
- Erreur de validation JSON-RPC 2.0 sur tools/list suite a un schema non conforme.
- Tentative d'exposition d'un outil avec des types Pydantic invalides.

## Entrees

- Definition de l'outil FastMCP (nom, description, inputSchema).
- Schema inputSchema au format JSON Schema.
- Types Pydantic associes aux parametres d'entree.

## Sorties

- Rapport de conformite du schema (valide / invalide).
- Liste des erreurs de validation detectees (types manquants, champs requis absents, etc.).
- Autorisation ou rejet de l'exposition de l'outil sur le gateway.
- Code retour 0 si valide, code retour 1 si invalide.

## Regles Operationnelles

### 1. Verification de la presence de inputSchema
Tout outil declare doit posseder un champ inputSchema valide (objet JSON Schema). Absence de ce champ = rejet immediat.

### 2. Verification des types Pydantic
Les types declares dans inputSchema doivent correspondre a des types Pydantic supportes (string, integer, number, boolean, array, object). Types inconnus = rejet.

### 3. Verification des champs requis
Les champs marques comme requis dans inputSchema doivent etre presents dans la definition de l'outil. Champ requis manquant = rejet.

### 4. Test de serialisation JSON-RPC 2.0
Le schema doit permettre une serialisation correcte des reponses tools/list au format JSON-RPC 2.0 (protocolVersion, capabilities, tools avec name, description, inputSchema).

### 5. Rejet en cas d'erreur
Tout schema ne passant pas les verifications ci-dessus est refuse et l'outil n'est pas expose sur le gateway. Un message d'erreur precise identifie le champ ou le type en cause.
