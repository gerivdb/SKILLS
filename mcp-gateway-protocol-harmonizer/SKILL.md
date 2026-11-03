---
type: SKILL
version: "1.0.0"
status: active
date: "2026-11-03"
intent_hash: 0xSKILL_MGPH_20261103
layer: L4-TOOLS
author: gerivdb
source_repo: gerivdb/SKILLS
source_path: skills/mcp-gateway-protocol-harmonizer/SKILL.md
---

# Skill - mcp-gateway-protocol-harmonizer

## Objectif

Harmoniser et garantir l'interopérabilité entre les clients MCP (qui utilisent le protocole JSON-RPC 2.0 sur HTTP avec les méthodes `initialize`, `tools/list`, `tools/call`) et le routeur de passerelle multi-transports du GATEWAY-MANAGER (gérant les backends sous-jacents en `stdio`, `http` ou `mcp` direct).

## Déclencheurs

- Réponses HTTP 400 (*Bad Request*) ou HTTP 501 (*Not Implemented*) lors de l'appel d'un client MCP sur `POST /mcp/{backend_id}`.
- Déclaration d'un nouveau backend MCP dans `config/mcp-servers.yaml` (ex: `jupyter-ai`).
- Script de test client (ex: `test_jupyter_mcp.py`, KiloCode, Claude Code) échouant à lister les outils d'un backend enregistré.

## Entrées

- Configuration du backend (`config/mcp-servers.yaml` ou registre dynamique).
- Routeur FastAPI du serveur (`src/gateway_manager/server.py`).
- Routeur de transport stdio (`src/gateway_manager/stdio_client.py`).

## Sorties

- Routage JSON-RPC 2.0 transparent pour tout backend quel que soit son type (`stdio`, `http`, `mcp`).
- Réponses conformes aux spécifications MCP 2024-11-05 (`protocolVersion`, `tools`, `content`).

## Règles Opérationnelles

### 1. Universalité de l'endpoint `/mcp/{backend_id}`
L'endpoint de passerelle `POST /mcp/{backend_id}` ne doit jamais rejeter arbitrairement une requête sous prétexte que le backend est de type `stdio` ou `http`. Il doit agir comme un pont de traduction :
- Si la méthode JSON-RPC est `initialize` : répondre avec les capacités serveur standard (`protocolVersion: 2024-11-05`, `capabilities: {tools: {}}`).
- Si la méthode JSON-RPC est `tools/list` : retourner la liste des outils déclarés du backend, formatés selon le schéma MCP (`name`, `description`, `inputSchema`).
- Si la méthode JSON-RPC est `tools/call` : extraire `params.name` et `params.arguments` et relayer l'appel au gestionnaire de transport adéquat (`stdio_router` ou client HTTP).

### 2. Validation par sonde synthétique
Toujours vérifier un endpoint proxy avec un payload JSON-RPC minimal avant de déclarer l'intégration fonctionnelle :
```python
payload = {"jsonrpc": "2.0", "method": "tools/list", "params": {}, "id": 1}
```

### 3. Gestion gracieuse des backends non encore démarrés
Si le processus sous-jacent (ex: proxy stdio Jupyter ou serveur upstream) n'est pas actif, le gateway doit retourner une liste d'outils configurés sans crasher et signaler l'état dans les logs.

