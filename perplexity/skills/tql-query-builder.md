---
name: tql-query-builder
description: "Construit des requetes TQL AST valides pour NEXUS (FIND/FILTER/SORT/GROUP), les envoie via nexus_client.py, interprete les resultats. Inclut des templates de requetes frequentes."
version: "1.0.0"
triggers:
  - "requete TQL"
  - "TQL query"
  - "interroger NEXUS"
  - "TQL FIND"
  - "TQL FILTER"
layer: "L0_CANON"
nexusTags: ["CONFORME_NEXUS", "TQL", "QUERY_BUILDER"]
status: "active"
changelog:
  - {v: "1.0.0", date: "2026-06-11", notes: "Creation — complement de keel-vdb-tql (couvre NEXUS, pas KEEL)"}
slotWeight: 1
trit_primitive: TritThinkConfig
---

# TQL-QUERY-BUILDER — Construction de requetes TQL pour NEXUS

## Domaine et perimetre

Ce skill construit des requetes TQL AST valides pour interroger NEXUS via le endpoint `tql/api/query_endpoint.py`. Complement de `keel-vdb-tql` qui couvre KEEL, pas NEXUS directement.

## Syntaxe TQL supportee

### FIND
```json
{
  "operation": "FIND",
  "collection": "<path>",
  "fields": ["*"] ou ["field1", "field2"],
  "limit": 100
}
```

### FILTER
```json
{
  "operation": "FILTER",
  "collection": "<path>",
  "condition": {
    "field": "<field>",
    "op": "eq|ne|gt|lt|contains",
    "value": "<value>"
  }
}
```

### SORT
```json
{
  "operation": "SORT",
  "collection": "<path>",
  "sort_by": {
    "field": "<field>",
    "direction": "asc|desc"
  }
}
```

### GROUP
```json
{
  "operation": "GROUP",
  "collection": "<path>",
  "group_by": "<field>"
}
```

## Templates de requetes frequentes

### Bridges par statut
```json
{
  "operation": "FILTER",
  "collection": "BRIDGES",
  "condition": {"field": "status", "op": "eq", "value": "active"}
}
```

### Repos par strate
```json
{
  "operation": "FILTER",
  "collection": "known_repositories",
  "condition": {"field": "layer", "op": "eq", "value": "L0_CANON"}
}
```

### EPICs par phi_cps
```json
{
  "operation": "SORT",
  "collection": "EPICS",
  "sort_by": {"field": "phi_cps", "direction": "desc"}
}
```

## Methodologie

1. Identifier le besoin (FIND/FILTER/SORT/GROUP)
2. Construire l'AST JSON
3. Envoyer via `nexus_client.py`
4. Interpreter le resultat

## Integration

- **Declencheur** : Requete Perplexity sur les donnees NEXUS
- **Dependances** : nexus_client.py (BRAIN), endpoint TQL (NEXUS)
- **Complement de** : keel-vdb-tql
