"""
skill_ir/skill_ir.py — SkillIR(AnywhereIR) (S1→S3)

Coherence moteur pour 59 Skills CTULU.
5 opcodes :
  SKILL_LOAD        — parse frontmatter skill -> IRNode
  SKILL_LINK        — arc requires / supersedes / feeds
  SKILL_GATE        — version compatible / deps resolues / pas de cycle
  SKILL_PROPAGATOR  — skill change -> [A_REVALIDER] consommateurs
  SKILL_SCORE       — phi-coherence suite : ratio deps resolues

v1.0: IntentHash: 0xSKILL_IR_SKILL_IR_20260620
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

import yaml

# --- Shim de compatibilite keel_core ---
try:
    from keel_core import DAG, IRArc, IRNode, TritLevel
except ImportError:
    from enum import auto as _auto

    class TritLevel:
        T1 = _auto()
        T2 = _auto()
        T3 = _auto()

    @dataclass
    class IRNode:
        id: str
        node_type: str = "skill"
        status: str = "active"
        phi: float = 0.0
        trit: Any = None
        meta: dict = field(default_factory=dict)

        @property
        def is_valid(self):
            return bool(self.id) and self.status in ("active", "deprecated")

        @property
        def phi_contribution(self):
            return 1.0 if self.trit == TritLevel.T1 else 0.5 if self.trit == TritLevel.T2 else 0.0

    @dataclass
    class IRArc:
        source: str
        target: str
        arc_type: str = "requires"
        resolved: bool = True
        meta: dict = field(default_factory=dict)

    @dataclass
    class DAG:
        nodes: dict = field(default_factory=dict)
        arcs: list = field(default_factory=list)

        @property
        def node_count(self):
            return len(self.nodes)

        @property
        def arc_count(self):
            return len(self.arcs)

        def add_node(self, node):
            self.nodes[node.id] = node

        def add_arc(self, arc):
            self.arcs.append(arc)

        def get_node(self, nid):
            return self.nodes.get(nid)

        def get_dependencies(self, nid):
            return [a.target for a in self.arcs if a.source == nid]

        def get_dependents(self, nid):
            return [a.source for a in self.arcs if a.target == nid]

        def has_node(self, nid):
            return nid in self.nodes

        def has_arc(self, src, tgt):
            return any(a.source == src and a.target == tgt for a in self.arcs)


# --- Exceptions ---

class SkillValidationError(Exception):
    """Levee si un skill est invalide."""
    pass


# --- SkillIR ---

class SkillIR:
    """
    Coherence moteur pour 59 Skills CTULU.

    Methodes :
      - load(skill_path) -> IRNode
      - link(source, target, arc_type) -> IRArc
      - gate(node, dag) -> str (T1/T2/T3)
      - build_dag(skills) -> DAG
      - propagate(changed_id, dag) -> list[str]
      - score(dag) -> float
    """

    VALID_STATUSES = {"active", "deprecated"}
    VALID_ARC_TYPES = {"requires", "supersedes", "feeds", "extends"}

    @staticmethod
    def load(skill_path: str | Path) -> IRNode:
        """
        SKILL_LOAD — parse un skill depuis son repertoire.

        Lit le frontmatter YAML du SKILL.md (si present)
        ou extrait les metadonnees du nom du repertoire.

        Args:
            skill_path: chemin vers le repertoire du skill

        Returns:
            IRNode construit.

        Raises:
            SkillValidationError: si le repertoire n'existe pas.
        """
        path = Path(skill_path)
        if not path.exists():
            raise SkillValidationError(f"Skill introuvable: {path}")

        # Si on passe un fichier, prendre le parent
        if path.is_file():
            path = path.parent

        skill_name = path.name
        frontmatter: dict[str, Any] = {}
        body: str = ""

        # Chercher SKILL.md ou manifest.yaml
        skill_md = path / "SKILL.md"
        manifest_yaml = path / "manifest.yaml"

        if manifest_yaml.exists():
            content = manifest_yaml.read_text(encoding="utf-8")
            frontmatter = yaml.safe_load(content) or {}
        elif skill_md.exists():
            content = skill_md.read_text(encoding="utf-8")
            frontmatter, body = SkillIR._parse_frontmatter(content)

        # Extraire les champs
        skill_id = frontmatter.get("id", skill_name)
        version = frontmatter.get("version", "1.0.0")
        description = frontmatter.get("description", frontmatter.get("title", ""))
        deps = frontmatter.get("deps", [])
        triggers = frontmatter.get("triggers", [])
        strata = frontmatter.get("strata", "L3")
        intent_hash = frontmatter.get("intent_hash", "")

        if not intent_hash:
            intent_hash = f"0x{skill_name.upper()}_{datetime.now(timezone.utc).strftime('%Y%m%d')}"

        # Determiner le trit
        trit = TritLevel.T1
        if frontmatter.get("status") == "deprecated":
            trit = TritLevel.T2

        meta = {
            "version": version,
            "description": description,
            "strata": strata,
            "deps": deps,
            "triggers": triggers,
            "intent_hash": intent_hash,
            "skill_path": str(path),
        }

        return IRNode(
            id=skill_id,
            node_type="skill",
            status=frontmatter.get("status", "active"),
            phi=1.0,
            trit=trit,
            meta=meta,
        )

    @staticmethod
    def _parse_frontmatter(content: str) -> tuple[dict, str]:
        """Parse le frontmatter YAML d'un fichier Markdown."""
        if not content.startswith("---"):
            return {}, content
        end = content.find("---", 3)
        if end == -1:
            return {}, content
        fm_str = content[3:end].strip()
        body = content[end + 3:].strip()
        try:
            frontmatter = yaml.safe_load(fm_str) or {}
        except yaml.YAMLError:
            frontmatter = {}
        return frontmatter, body

    @staticmethod
    def link(
        source: IRNode,
        target: IRNode,
        arc_type: str = "requires",
    ) -> IRArc:
        """
        SKILL_LINK — cree un arc entre deux skills.

        Args:
            source: IRNode source
            target: IRNode cible
            arc_type: type d'arc (requires / supersedes / feeds / extends)

        Returns:
            IRArc cree.
        """
        if arc_type not in SkillIR.VALID_ARC_TYPES:
            arc_type = "requires"

        return IRArc(
            source=source.id,
            target=target.id,
            arc_type=arc_type,
            resolved=True,
        )

    @staticmethod
    def gate(node: IRNode, dag: Optional[DAG] = None) -> str:
        """
        SKILL_GATE — evalue la coherence d'un skill.

        PG1 : version compatible (format semver)
        PG2 : deps resolues dans le DAG
        PG3 : pas de cycle dans les dependances

        Returns:
            'T1' (coherent), 'T2' (warning), 'T3' (bloquant)
        """
        # PG1 : version
        version = node.meta.get("version", "0.0.0")
        if not re.match(r"^\d+\.\d+\.\d+$", str(version)):
            return "T2"

        # PG2 : deps resolues
        deps = node.meta.get("deps", [])
        if dag and deps:
            for dep in deps:
                dep_name = dep.split(":")[0].strip() if isinstance(dep, str) else str(dep)
                if not dag.has_node(dep_name):
                    return "T2"

        # PG3 : cycles
        if dag:
            visited: set[str] = set()
            stack: set[str] = set()

            def _dfs(nid: str) -> bool:
                if nid in stack:
                    return True
                if nid in visited:
                    return False
                visited.add(nid)
                stack.add(nid)
                for dep_id in dag.get_dependencies(nid):
                    if _dfs(dep_id):
                        return True
                stack.discard(nid)
                return False

            if _dfs(node.id):
                return "T3"

        return "T1"

    @staticmethod
    def build_dag(skills: list[IRNode]) -> DAG:
        """
        SKILL_DAG — construit le DAG des skills.

        Args:
            skills: liste d'IRNode skills

        Returns:
            DAG construit.
        """
        dag = DAG()

        for skill in skills:
            dag.add_node(skill)

        # Creer les arcs depuis les deps
        id_set = {s.id for s in skills}
        for skill in skills:
            deps = skill.meta.get("deps", [])
            for dep in deps:
                dep_name = dep.split(":")[0].strip() if isinstance(dep, str) else str(dep)
                if dep_name in id_set:
                    dag.add_arc(IRArc(
                        source=skill.id,
                        target=dep_name,
                        arc_type="requires",
                        resolved=True,
                    ))

        return dag

    @staticmethod
    def propagate(changed_id: str, dag: DAG) -> list[str]:
        """
        SKILL_PROPAGATOR — propage un changement vers les consommateurs.

        Args:
            changed_id: ID du skill qui a change
            dag: DAG des skills

        Returns:
            Liste des IDs impactes.
        """
        if changed_id not in dag.nodes:
            return []

        impacted: list[str] = []
        visited: set[str] = {changed_id}
        queue: list[str] = [changed_id]

        while queue:
            current = queue.pop(0)
            for dep_id in dag.get_dependents(current):
                if dep_id not in visited:
                    visited.add(dep_id)
                    impacted.append(dep_id)
                    queue.append(dep_id)

        return impacted

    @staticmethod
    def score(dag: DAG) -> float:
        """
        SKILL_SCORE — calcule le phi-coherence de la suite.

        Returns:
            float dans [0.0, 1.0]
        """
        if dag.node_count == 0:
            return 0.0

        total_deps = 0
        resolved_deps = 0

        for node in dag.nodes.values():
            deps = node.meta.get("deps", [])
            for dep in deps:
                dep_name = dep.split(":")[0].strip() if isinstance(dep, str) else str(dep)
                total_deps += 1
                if dag.has_node(dep_name):
                    resolved_deps += 1

        if total_deps == 0:
            return 1.0

        return round(resolved_deps / total_deps, 4)
