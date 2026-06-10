#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 CTULU RESOLVER
Résolution externe de tools CTULU depuis SKILLS.

Permet à skill_registry.py et skill_loader.py d'interroger
gerivdb/CTULU/REGISTRY.yaml par tool_id et version,
plutôt que de résoudre uniquement en local.

Consommateurs :
  - skill_registry.py  → SkillRegistry.resolve_tool()
  - skill_loader.py    → DynamicSkillLoader.load_with_tools()
  - VERSEContext        → ctx.tools[] sont résolus ici avant exécution
"""

import json
import urllib.request
import urllib.error
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# URL brute du REGISTRY.yaml CTULU (pas d'auth requise pour repo public)
_CTULU_REGISTRY_URL = (
    "https://raw.githubusercontent.com/gerivdb/CTULU/main/REGISTRY.yaml"
)

# Fallback local si CTULU est un submodule ou cloné en local
_CTULU_LOCAL_PATHS = [
    "../CTULU/REGISTRY.yaml",
    "../../CTULU/REGISTRY.yaml",
    "/workspaces/CTULU/REGISTRY.yaml",
]


@dataclass
class ToolEntry:
    """
    Entrée d'un tool CTULU résolu.
    Miroir déclaratif du format REGISTRY.yaml CTULU.
    """
    id: str
    status: str                          # SPIKE | DRAFT | STABLE | DEPRECATED
    type: str                            # frontend | backend | adapter | primitive
    path: str
    description: str
    consumers: List[str] = field(default_factory=list)
    primitives: List[str] = field(default_factory=list)  # PRIMUS deps
    version: Optional[str] = None
    input: Optional[str] = None
    output: Optional[str] = None
    prd: Optional[str] = None
    adr: Optional[str] = None

    @property
    def is_available(self) -> bool:
        """True si le tool est utilisable (pas DEPRECATED)."""
        return self.status != "DEPRECATED"

    @property
    def ctulu_url(self) -> str:
        """URL GitHub du tool dans CTULU."""
        return f"https://github.com/gerivdb/CTULU/tree/main/{self.path}"


class CTULUResolver:
    """
    Résolveur de tools CTULU.

    Stratégie de résolution (dans l'ordre) :
    1. Cache mémoire (chargé une fois par instance)
    2. Fichier local (CTULU cloné en local ou submodule)
    3. Fetch HTTP depuis github.com/gerivdb/CTULU

    Usage :
        resolver = CTULUResolver()
        tool = resolver.resolve("dag-navigator")
        if tool and tool.is_available:
            print(tool.ctulu_url)

        # Depuis un VERSEContext
        tools = resolver.resolve_many(ctx.tools)
    """

    def __init__(self, registry_url: str = _CTULU_REGISTRY_URL):
        self._registry_url = registry_url
        self._cache: Dict[str, ToolEntry] = {}
        self._loaded = False

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def resolve(self, tool_id: str) -> Optional[ToolEntry]:
        """Résout un tool_id → ToolEntry. Retourne None si introuvable."""
        self._ensure_loaded()
        return self._cache.get(tool_id)

    def resolve_many(self, tool_ids: List[str]) -> Dict[str, Optional[ToolEntry]]:
        """Résout une liste de tool_ids en une passe. Retourne un dict id→ToolEntry|None."""
        self._ensure_loaded()
        return {tid: self._cache.get(tid) for tid in tool_ids}

    def find_by_consumer(self, consumer: str) -> List[ToolEntry]:
        """Retourne tous les tools CTULU consommés par un repo donné."""
        self._ensure_loaded()
        return [
            t for t in self._cache.values()
            if consumer in t.consumers
        ]

    def find_by_type(self, tool_type: str) -> List[ToolEntry]:
        """Retourne tous les tools d'un type donné (frontend | backend | adapter)."""
        self._ensure_loaded()
        return [t for t in self._cache.values() if t.type == tool_type]

    def all_tools(self) -> List[ToolEntry]:
        """Retourne tous les tools du registry CTULU."""
        self._ensure_loaded()
        return list(self._cache.values())

    def reload(self) -> int:
        """Force un rechargement du registry. Retourne le nombre de tools chargés."""
        self._loaded = False
        self._cache.clear()
        self._ensure_loaded()
        return len(self._cache)

    # ------------------------------------------------------------------
    # Internal loading
    # ------------------------------------------------------------------

    def _ensure_loaded(self):
        if not self._loaded:
            self._load_registry()
            self._loaded = True

    def _load_registry(self):
        """Charge CTULU/REGISTRY.yaml depuis local ou HTTP."""
        raw = self._fetch_local() or self._fetch_remote()
        if raw:
            self._parse_registry(raw)

    def _fetch_local(self) -> Optional[str]:
        """Tente de lire REGISTRY.yaml depuis les chemins locaux connus."""
        import os
        for path in _CTULU_LOCAL_PATHS:
            if os.path.exists(path):
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        return f.read()
                except Exception:
                    continue
        return None

    def _fetch_remote(self) -> Optional[str]:
        """Fetch HTTP du REGISTRY.yaml depuis GitHub (public, no auth)."""
        try:
            with urllib.request.urlopen(self._registry_url, timeout=5) as resp:
                return resp.read().decode('utf-8')
        except Exception:
            return None

    def _parse_registry(self, raw: str):
        """Parse le YAML du registry et alimente le cache."""
        try:
            import yaml
            data = yaml.safe_load(raw)
            for tool_data in data.get('tools', []):
                entry = ToolEntry(
                    id=tool_data.get('id', ''),
                    status=tool_data.get('status', 'DRAFT'),
                    type=tool_data.get('type', 'unknown'),
                    path=tool_data.get('path', ''),
                    description=tool_data.get('description', ''),
                    consumers=tool_data.get('consumers', []),
                    primitives=tool_data.get('primitives', []),
                    version=tool_data.get('version'),
                    input=tool_data.get('input'),
                    output=tool_data.get('output'),
                    prd=tool_data.get('prd'),
                    adr=tool_data.get('adr'),
                )
                self._cache[entry.id] = entry
        except Exception:
            pass  # Registry indisponible : fail silencieux, ne bloque pas SKILLS


# Instance globale — import et utilise directement
CTULU_RESOLVER = CTULUResolver()
