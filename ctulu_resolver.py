#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CTULUResolver v2 — Module déployé dans gerivdb/SKILLS

Ce fichier est un wrapper autour du resolver CTULU principal.
Il est copié depuis CTULU/integrations/ctulu-resolver/deliverables/SKILLS_ctulu_resolver.py

Usage depuis skill_loader.py:
    from ctulu_resolver import get_resolver, resolve_tool, list_ctulu_tools
    
    resolver = get_resolver()
    if resolver:
        tools = resolver.list_tools(layer="phase7")
        
IntentHash: 0xCTULU_RESOLVER_V2_SKILLS_20260614
"""

from pathlib import Path
import sys
import logging

log = logging.getLogger(__name__)

# Chemin vers CTULU (adapter si nécessaire)
CTULU_BASE = Path("D:/DO/WEB/TOOLS/L4-TOOLS/CTULU")
CTULU_RESOLVER_PATH = CTULU_BASE / "integrations" / "ctulu-resolver"

# Ajoute CTULU au path
if CTULU_RESOLVER_PATH.exists():
    sys.path.insert(0, str(CTULU_RESOLVER_PATH))

try:
    from ctulu_resolver import CTULUResolver, ToolEntry
    _RESOLVER_AVAILABLE = True
except ImportError as e:
    log.warning("CTULUResolver non disponible: %s", e)
    CTULUResolver = None
    ToolEntry = None
    _RESOLVER_AVAILABLE = False


def get_resolver() -> "CTULUResolver | None":
    """Retourne une instance du resolver si CTULU est accessible."""
    if not _RESOLVER_AVAILABLE or CTULUResolver is None:
        return None
    try:
        return CTULUResolver(ctulu_base=CTULU_BASE)
    except Exception as e:
        log.error("Erreur initialisation CTULUResolver: %s", e)
        return None


def resolve_tool(tool_id: str) -> dict | None:
    """Résout un outil CTULU par ID. Utilisable par skill_loader.py."""
    resolver = get_resolver()
    if resolver is None:
        return None
    entry = resolver.resolve(tool_id)
    if entry:
        return entry.to_dict()
    return None


def resolve_deps(tool_id: str, transitive: bool = True) -> list:
    """Résout les dépendances d'un outil CTULU."""
    resolver = get_resolver()
    if resolver is None:
        return []
    return resolver.resolve_deps(tool_id, transitive=transitive)


def list_ctulu_tools(layer: str = None) -> list:
    """Liste les outils CTULU, avec filtre optionnel par layer."""
    resolver = get_resolver()
    if resolver is None:
        return []
    tools = resolver.list_tools(layer=layer)
    return [t.to_dict() for t in tools]


def validate_tool(tool_id: str) -> dict:
    """Valide la conformité d'un outil CTULU."""
    resolver = get_resolver()
    if resolver is None:
        return {"tool_id": tool_id, "valid": False, "errors": ["Resolver non disponible"]}
    return resolver.validate(tool_id)
