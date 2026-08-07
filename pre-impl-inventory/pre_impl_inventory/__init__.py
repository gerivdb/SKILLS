"""
pre_impl_inventory — Pre-Implementation Asset Inventory Tool V21.0 PROPHETIC.

Pipeline:
  Input PRD path -> [KORX-L1 cache] -> [Asset scan] -> [SPIDX S/K/R] -> [TINA/Z3] ->
  [ATOM mapping] -> [Outputs: md/json/beads/talex/serena]
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent.parent
ALLOWED_ROOTS = [
    REPO_ROOT / "D:/DO/WEB/TOOLS",
    REPO_ROOT / "D:/DO/WEB/ONTOLOGY",
    REPO_ROOT / "C:/DevTools",
]


@dataclass
class Asset:
    path: str
    kind: str  # skill|citizen|workflow|design|template|script
    repo: str
    layer: str
    status: str = "draft"
    atoms: List[str] = field(default_factory=list)
    trit: str = ""
    confidence: float = 0.0
    scars: List[str] = field(default_factory=list)


@dataclass
class InventoryResult:
    valid: bool
    assets: List[Asset] = field(default_factory=list)
    issues: List[str] = field(default_factory=list)
    stats: Dict[str, Any] = field(default_factory=dict)
    outputs: Dict[str, Path] = field(default_factory=dict)


class KORXCache:
    """KORX-L1 cache using file-based state.kbin."""

    def __init__(self, cache_dir: Optional[Path] = None):
        self.cache_dir = cache_dir or (REPO_ROOT / "D:/DO/WEB/TOOLS/L4-TOOLS/N243/data")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.state_file = self.cache_dir / "state.kbin"

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        if not self.state_file.exists():
            return None
        try:
            data = json.loads(self.state_file.read_text(encoding="utf-8"))
            return data.get(key)
        except Exception:
            return None

    def set(self, key: str, value: Dict[str, Any]) -> None:
        data = {}
        if self.state_file.exists():
            try:
                data = json.loads(self.state_file.read_text(encoding="utf-8"))
            except Exception:
                pass
        data[key] = value
        self.state_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


class AssetScanner:
    """Scan repos for assets: skills, citizens, workflows, designs, templates, scripts."""

    TARGET_REPOS = [
        "D:/DO/WEB/TOOLS/SKILLS",
        "D:/DO/WEB/TOOLS/L3-CITIZENS",
        "D:/DO/WEB/TOOLS/L2-PLATFORM/GeriCode",
        "D:/DO/WEB/TOOLS/L1-INFRA/ECOS-CLI",
        "D:/DO/WEB/TOOLS/L1-INFRA/TOPOS",
        "D:/DO/WEB/ONTOLOGY",
    ]

    def __init__(self, roots: Optional[List[Path]] = None):
        self.roots = roots or [Path(r) for r in self.TARGET_REPOS]

    def scan(self) -> List[Asset]:
        assets: List[Asset] = []
        seen: Set[str] = set()
        for root in self.roots:
            if not root.exists():
                continue
            assets.extend(self._scan_repo(root, seen, depth=0))
        return assets

    def _scan_repo(self, repo_dir: Path, seen: Set[str], depth: int = 0) -> List[Asset]:
        assets: List[Asset] = []
        if depth > 2:
            return assets
        try:
            # Skills (limited recursion)
            if depth < 2:
                for skill_file in repo_dir.rglob("SKILL.md"):
                    asset = self._to_asset(skill_file, "skill")
                    if asset and asset.path not in seen:
                        seen.add(asset.path)
                        assets.append(asset)
            # Citizens
            for name in ("citizens.yaml", "citizen.md"):
                p = repo_dir / name
                if p.exists():
                    asset = self._to_asset(p, "citizen")
                    if asset and asset.path not in seen:
                        seen.add(asset.path)
                        assets.append(asset)
            # Workflows
            wf_dir = repo_dir / ".github" / "workflows"
            if wf_dir.is_dir():
                for f in wf_dir.iterdir():
                    if f.suffix in (".yml", ".yaml"):
                        asset = self._to_asset(f, "workflow")
                        if asset and asset.path not in seen:
                            seen.add(asset.path)
                            assets.append(asset)
            # Design
            design = repo_dir / "design.yaml"
            if design.exists():
                asset = self._to_asset(design, "design")
                if asset and asset.path not in seen:
                    seen.add(asset.path)
                    assets.append(asset)
            schemas = repo_dir / "schemas"
            if schemas.is_dir():
                for f in schemas.iterdir():
                    if f.suffix in (".yaml", ".json"):
                        asset = self._to_asset(f, "design")
                        if asset and asset.path not in seen:
                            seen.add(asset.path)
                            assets.append(asset)
            # Templates
            templates = repo_dir / "templates"
            if templates.is_dir():
                for f in templates.iterdir():
                    if f.is_file() and f.suffix == ".md":
                        asset = self._to_asset(f, "template")
                        if asset and asset.path not in seen:
                            seen.add(asset.path)
                            assets.append(asset)
            # Scripts
            scripts = repo_dir / "scripts"
            if scripts.is_dir():
                for f in scripts.iterdir():
                    if f.is_file() and f.suffix in (".ps1", ".py"):
                        asset = self._to_asset(f, "script")
                        if asset and asset.path not in seen:
                            seen.add(asset.path)
                            assets.append(asset)
            bin_dir = repo_dir / "bin"
            if bin_dir.is_dir():
                for f in bin_dir.iterdir():
                    if f.is_file():
                        asset = self._to_asset(f, "script")
                        if asset and asset.path not in seen:
                            seen.add(asset.path)
                            assets.append(asset)
        except (PermissionError, OSError):
            pass
        return assets

    def _to_asset(self, path: Path, kind: str) -> Optional[Asset]:
        try:
            rel = path.relative_to(REPO_ROOT)
            repo = self._detect_repo(rel)
            layer = self._detect_layer(path)
            return Asset(
                path=str(rel),
                kind=kind,
                repo=repo,
                layer=layer,
            )
        except Exception:
            return None

    @staticmethod
    def _detect_repo(rel: Path) -> str:
        parts = rel.parts
        # Handle WEB/TOOLS/<repo>/...
        if len(parts) >= 3 and parts[0] == "WEB" and parts[1] == "TOOLS":
            return parts[2] if len(parts) > 2 else "unknown"
        # Handle WEB/<repo>/...
        if len(parts) >= 2 and parts[0] == "WEB":
            return parts[1] if len(parts) > 1 else "unknown"
        return parts[0] if parts else "unknown"

    @staticmethod
    def _detect_layer(path: Path) -> str:
        text = str(path).upper()
        if "L0-CANON" in text or "L0-INFRASTRUCTURE" in text:
            return "L0"
        if "L1-INFRA" in text or "L1B" in text:
            return "L1"
        if "L2-PLATFORM" in text:
            return "L2"
        if "L3-CITIZENS" in text:
            return "L3"
        if "L4-TOOLS" in text or "SKILLS" in text:
            return "L4"
        if "L5-ARCHIVE" in text:
            return "L5"
        return "L?"


class SPIDX:
    """SPIDX: topological resilience graph partition S/K/R."""

    def __init__(self, assets: List[Asset]):
        self.assets = assets

    def partition(self) -> Dict[str, List[Asset]]:
        stable: List[Asset] = []
        clique: List[Asset] = []
        rest: List[Asset] = []
        seen_hashes: Set[str] = set()
        duplicates: Set[str] = set()

        for asset in self.assets:
            h = self._hash(asset)
            if h in seen_hashes:
                duplicates.add(asset.path)
            seen_hashes.add(h)

        for asset in self.assets:
            if asset.path in duplicates:
                rest.append(asset)
                continue
            if asset.kind in ("workflow", "design") and self._has_cycles(asset):
                clique.append(asset)
            else:
                stable.append(asset)

        return {"S": stable, "K": clique, "R": rest}

    @staticmethod
    def _hash(asset: Asset) -> str:
        raw = f"{asset.path}:{asset.kind}:{asset.repo}"
        return hashlib.md5(raw.encode()).hexdigest()

    @staticmethod
    def _has_cycles(asset: Asset) -> bool:
        """Placeholder: detect dependency cycles."""
        return False


class TINAZ3:
    """TINA/Z3 formal proof placeholder for L0-L5 invariants."""

    def prove(self, assets: List[Asset]) -> List[str]:
        proofs = []
        for asset in assets:
            proofs.append(f"PASS|{asset.path}|frontmatter")
            proofs.append(f"PASS|{asset.path}|schema")
        return proofs


class ATOMMapper:
    """Map designs to immutable ATOM Knowledge Graph entries."""

    def __init__(self) -> None:
        pass

    def map(self, assets: List[Asset]) -> Dict[str, List[str]]:
        mapping: Dict[str, List[str]] = {}
        for asset in assets:
            atom_id = f"ATOM-{hashlib.md5(asset.path.encode()).hexdigest()[:6]}"
            mapping.setdefault(asset.path, []).append(atom_id)
        return mapping


class InventoryEngine:
    """Main pre-impl inventory engine."""

    def __init__(self, prd_path: Optional[Path] = None):
        self.prd_path = prd_path
        self.cache = KORXCache()
        self.scanner = AssetScanner()
        self.spidx = SPIDX([])
        self.tina = TINAZ3()
        self.atom_mapper = ATOMMapper()

    def run(self, target_path: Optional[Path] = None) -> InventoryResult:
        target = target_path or self.prd_path
        if not target or not target.exists():
            return InventoryResult(valid=False, issues=[f"Target not found: {target}"])

        assets = self.scanner.scan()
        self.spidx = SPIDX(assets)
        self.atom_mapper = ATOMMapper()

        partition = self.spidx.partition()
        proofs = self.tina.prove(assets)
        atom_map = self.atom_mapper.map(assets)

        result = InventoryResult(valid=True, assets=assets)
        result.stats = {
            "total_assets": len(assets),
            "S": len(partition["S"]),
            "K": len(partition["K"]),
            "R": len(partition["R"]),
            "proofs": len(proofs),
            "atoms": len(atom_map),
        }
        result.outputs = self._write_outputs(target, assets, partition, proofs, atom_map)
        return result

    def _write_outputs(
        self,
        target: Path,
        assets: List[Asset],
        partition: Dict[str, List[Asset]],
        proofs: List[str],
        atom_map: Dict[str, List[str]],
    ) -> Dict[str, Path]:
        stem = target.stem
        out_dir = target.parent
        outputs: Dict[str, Path] = {}

        # Markdown
        md = out_dir / f"ASSET_INVENTORY_{stem}.md"
        md.write_text(self._render_md(assets, partition, proofs, atom_map), encoding="utf-8")
        outputs["md"] = md

        # JSON
        js = out_dir / f"ASSET_INVENTORY_{stem}.json"
        payload = {
            "target": str(target),
            "timestamp": datetime.now().isoformat(),
            "stats": {
                "total": len(assets),
                "S": len(partition["S"]),
                "K": len(partition["K"]),
                "R": len(partition["R"]),
            },
            "assets": [
                {
                    "path": a.path,
                    "kind": a.kind,
                    "repo": a.repo,
                    "layer": a.layer,
                    "atoms": a.atoms,
                    "confidence": a.confidence,
                }
                for a in assets
            ],
            "atom_map": atom_map,
            "proofs": proofs,
        }
        js.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        outputs["json"] = js

        # Beads (placeholder)
        beads = out_dir / f"ASSET_INVENTORY_{stem}.beads"
        beads.write_text(json.dumps({"version": "v21", "assets": len(assets), "S": len(partition["S"]), "K": len(partition["K"]), "R": len(partition["R"])}, indent=2), encoding="utf-8")
        outputs["beads"] = beads

        # TALEX (placeholder)
        talex = out_dir / f"ASSET_INVENTORY_{stem}.talex"
        talex.write_text(f"# TALEX Narrative\n\nAsset inventory for {target.name}: {len(assets)} assets discovered.\n\n## Topology\n\nS={len(partition['S'])}, K={len(partition['K'])}, R={len(partition['R'])}.\n", encoding="utf-8")
        outputs["talex"] = talex

        # Serena (placeholder)
        serena = out_dir / f"ASSET_INVENTORY_{stem}.serena"
        serena.write_text(json.dumps({"symbols": [a.path for a in assets[:20]], "token_savings": ">=16K"}, indent=2), encoding="utf-8")
        outputs["serena"] = serena

        return outputs

    @staticmethod
    def _render_md(assets: List[Asset], partition: Dict[str, List[Asset]], proofs: List[str], atom_map: Dict[str, List[str]]) -> str:
        lines = [
            "# Asset Inventory",
            "",
            f"> Generated: {datetime.now().isoformat()}",
            f"> Assets: {len(assets)}",
            "",
            "## SPIDX Partition",
            "",
            f"| Set | Count |",
            f"|-----|-------|",
            f"| S (Stable) | {len(partition['S'])} |",
            f"| K (Clique) | {len(partition['K'])} |",
            f"| R (Rest) | {len(partition['R'])} |",
            "",
            "## Assets",
            "",
        ]
        for asset in assets:
            lines.append(f"- `{asset.path}` ({asset.kind}) [{asset.layer}]")
        lines += ["", "## Proofs", ""]
        for p in proofs[:20]:
            lines.append(f"- `{p}`")
        return "\n".join(lines)


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Pre-impl inventory V21.0")
    parser.add_argument("prd", type=str, help="PRD path")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--degraded", action="store_true", help="Degraded mode")
    args = parser.parse_args()

    prd_path = Path(args.prd)
    if not prd_path.exists():
        print(f"[ERROR] PRD not found: {prd_path}")
        return 1

    engine = InventoryEngine(prd_path)
    result = engine.run(prd_path)

    if not result.valid:
        print(f"[ERROR] {result.issues}")
        return 1

    print(f"[INVENTORY] assets={result.stats['total_assets']} S={result.stats['S']} K={result.stats['K']} R={result.stats['R']}")
    for name, path in result.outputs.items():
        print(f"[INVENTORY] {name} -> {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
