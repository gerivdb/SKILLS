#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌐 VERSE CONTEXT
Contrat d'injection de contexte Verse dans les Skills et Workflows.

Permet à WorkflowVerse d'initialiser l'execution_context
du WorkflowExecutor avec la mémoire et les paramètres d'une Verse active.

Consommateurs :
  - WorkflowVerse/workflow_executor.py  (injection au démarrage)
  - DynamicSkillLoader.load()           (contexte par skill)
  - CTULU tools                         (paramètres domaine)
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime


@dataclass
class VERSEContext:
    """
    Contexte d'exécution fourni par une Verse active.

    Injecté dans WorkflowExecutor.execution_context avant
    le premier step d'un pipeline.

    Champs obligatoires
    -------------------
    verse_id    : identifiant unique de la Verse (ex: "WorkflowVerse", "bon_sens_python_verse")
    verse_name  : nom lisible

    Champs optionnels
    -----------------
    domain      : domaine métier (ex: "devtools", "ontology", "physics")
    memory      : mémoire active — clés/valeurs arbitraires du domaine
    params      : paramètres d'exécution du pipeline
    skills      : liste de skill_ids requis par cette Verse
    tools       : liste de tool_ids CTULU requis
    primitives  : liste de primitive_ids PRIMUS requis
    created_at  : timestamp de création du contexte
    """

    # Obligatoires
    verse_id: str
    verse_name: str

    # Optionnels
    domain: Optional[str] = None
    memory: Dict[str, Any] = field(default_factory=dict)
    params: Dict[str, Any] = field(default_factory=dict)
    skills: List[str] = field(default_factory=list)
    tools: List[str] = field(default_factory=list)
    primitives: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """
        Sérialise le contexte pour injection dans WorkflowExecutor.execution_context.

        Le dict résultant est mergé dans execution_context avant l'exécution
        du premier step.
        """
        return {
            "__verse_id": self.verse_id,
            "__verse_name": self.verse_name,
            "__verse_domain": self.domain,
            "__verse_created_at": self.created_at.isoformat(),
            "__verse_skills": self.skills,
            "__verse_tools": self.tools,
            "__verse_primitives": self.primitives,
            **self.memory,   # mémoire domaine directement accessible par les steps
            **self.params,   # paramètres directement accessibles par les steps
        }

    @classmethod
    def from_verse_detector(cls, detected: Dict[str, Any]) -> "VERSEContext":
        """
        Construit un VERSEContext depuis le résultat de verse_detector.py.

        Compatible avec le format retourné par VerseDetector.detect().
        """
        return cls(
            verse_id=detected.get("id", "unknown"),
            verse_name=detected.get("name", "Unknown Verse"),
            domain=detected.get("domain"),
            memory=detected.get("memory", {}),
            params=detected.get("params", {}),
            skills=detected.get("skills", []),
            tools=detected.get("tools", []),
            primitives=detected.get("primitives", []),
        )

    def with_memory(self, key: str, value: Any) -> "VERSEContext":
        """Fluent builder — ajoute une entrée mémoire."""
        self.memory[key] = value
        return self

    def with_param(self, key: str, value: Any) -> "VERSEContext":
        """Fluent builder — ajoute un paramètre d'exécution."""
        self.params[key] = value
        return self

    def requires_skill(self, skill_id: str) -> "VERSEContext":
        """Fluent builder — déclare un skill requis."""
        if skill_id not in self.skills:
            self.skills.append(skill_id)
        return self

    def requires_tool(self, tool_id: str) -> "VERSEContext":
        """Fluent builder — déclare un tool CTULU requis."""
        if tool_id not in self.tools:
            self.tools.append(tool_id)
        return self

    def requires_primitive(self, primitive_id: str) -> "VERSEContext":
        """Fluent builder — déclare une primitive PRIMUS requise."""
        if primitive_id not in self.primitives:
            self.primitives.append(primitive_id)
        return self

    def __repr__(self) -> str:
        return (
            f"VERSEContext(verse_id={self.verse_id!r}, domain={self.domain!r}, "
            f"skills={self.skills}, tools={self.tools}, "
            f"memory_keys={list(self.memory.keys())})"
        )
