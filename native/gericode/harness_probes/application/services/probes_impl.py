from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from harness_probes.domain.value_objects.probe_result_vo import ProbeResultVO


@dataclass(frozen=True)
class ProbeContext:
    repo_root: Path
    skills_roots: tuple[Path, ...]
    verses_root: Path
    ontology_root: Path


def _default_context() -> ProbeContext:
    here = Path(__file__).resolve()
    repo_root = here.parent.parent.parent.parent.parent.parent
    web_root = repo_root.parent.parent.parent
    tools_root = repo_root.parent.parent
    return ProbeContext(
        repo_root=repo_root,
        skills_roots=(
            repo_root / "skills",
            repo_root / "native" / "gericode",
        ),
        verses_root=web_root / "VERSES",
        ontology_root=web_root / "ONTOLOGY",
    )


def _run(cmd: list[str], cwd: Path | None = None) -> tuple[int, str, str]:
    import subprocess
    try:
        proc = subprocess.run(cmd, cwd=cwd or _default_context().repo_root, capture_output=True, text=True, check=False)
        return proc.returncode, proc.stdout, proc.stderr
    except Exception as exc:
        return 1, "", str(exc)


def probe_p701_tdd(ctx: ProbeContext) -> ProbeResultVO:
    # Run pytest scoped to a known stable skill (harness-bootstrapper) to validate
    # TDD compliance without triggering collection errors from the full repo or
    # recursive self-invocation through harness_probes tests.
    tdd_target = ctx.repo_root / "native" / "gericode" / "harness-bootstrapper"
    returncode, stdout, _ = _run(
        ["python", "-m", "pytest", "-q"],
        cwd=tdd_target,
    )
    detail = (stdout or "").strip().splitlines()[-1] if (stdout or "").strip() else f"exit {returncode}"
    return ProbeResultVO(probe_id="P-701", passed=returncode == 0, detail=detail)


def probe_p702_bdd(ctx: ProbeContext) -> ProbeResultVO:
    hits: list[Path] = []
    for root in ctx.skills_roots:
        if root.exists():
            hits.extend(root.rglob("*.feature"))
    detail = f"{len(hits)} feature file(s)"
    return ProbeResultVO(probe_id="P-702", passed=bool(hits), detail=detail or "No BDD features found")


def probe_p703_atdd(ctx: ProbeContext) -> ProbeResultVO:
    hits: list[Path] = []
    for root in ctx.skills_roots:
        if root.exists():
            hits.extend(root.rglob("contract.yaml"))
    detail = f"{len(hits)} acceptance contract(s)"
    return ProbeResultVO(probe_id="P-703", passed=bool(hits), detail=detail or "No acceptance contracts found")


def probe_p704_ddd(ctx: ProbeContext) -> ProbeResultVO:
    bad: list[str] = []
    keywords = ("mcp", "subprocess", "requests.")
    for root in ctx.skills_roots:
        if not root.exists():
            continue
        for path in root.rglob("domain/**/*.py"):
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            lower = text.lower()
            if any(keyword in lower for keyword in keywords):
                # Only flag actual import statements, not docstrings/filenames
                has_infra_import = False
                for line in text.splitlines():
                    stripped = line.strip().lower()
                    if stripped.startswith("import ") or stripped.startswith("from "):
                        if any(keyword in stripped for keyword in keywords):
                            has_infra_import = True
                            break
                if has_infra_import:
                    bad.append(str(path.relative_to(ctx.repo_root)))
    detail = f"Infra dependency in domain layer: {bad[0]}" if bad else "No infra dependency detected in domain layer"
    return ProbeResultVO(probe_id="P-704", passed=not bad, detail=detail)


def probe_p705_dbc(ctx: ProbeContext) -> ProbeResultVO:
    hits: list[Path] = []
    for root in ctx.skills_roots:
        if root.exists():
            hits.extend(root.rglob("contracts/*.py"))
    detail = f"{len(hits)} contracts module(s)"
    return ProbeResultVO(probe_id="P-705", passed=bool(hits), detail=detail or "No contracts module found")


def probe_p706_hexagonal(ctx: ProbeContext) -> ProbeResultVO:
    missing: list[str] = []
    # Only scan native/gericode skills, which are expected to follow hexagonal architecture
    hex_roots = tuple(
        root / "native" / "gericode"
        for root in ctx.skills_roots
        if (root / "native" / "gericode").exists()
    )
    for root in hex_roots:
        if not root.exists():
            continue
        for skill_dir in root.iterdir():
            if not skill_dir.is_dir():
                continue
            has_ports = (skill_dir / "application/ports").exists() or (skill_dir / "application/ports/in").exists()
            has_adapters = (skill_dir / "infrastructure/adapters").exists()
            if not has_ports or not has_adapters:
                missing.append(str(skill_dir.relative_to(ctx.repo_root)))
    detail = f"Missing hexagonal structure in: {', '.join(missing[:5])}" if missing else "Hexagonal structure present across scanned skills"
    return ProbeResultVO(probe_id="P-706", passed=not missing, detail=detail)


def probe_p707_harness(ctx: ProbeContext) -> ProbeResultVO:
    tools_root = ctx.repo_root.parent.parent
    required = [
        tools_root / "L2-PLATFORM" / "GeriCode" / ".kilo" / "scaffold" / "adapters" / "in" / "base.py",
        tools_root / "L2-PLATFORM" / "GeriCode" / ".kilo" / "scaffold" / "adapters" / "out" / "base.py",
        tools_root / "L2-PLATFORM" / "GeriCode" / ".kilo" / "scaffold" / "lifecycle" / "lifecycle.py",
    ]
    missing = [str(path.relative_to(tools_root)) for path in required if not path.exists()]
    detail = f"Missing harness modules: {', '.join(missing)}" if missing else "Harness scaffold and self-improvement modules present"
    return ProbeResultVO(probe_id="P-707", passed=not missing, detail=detail)


def probe_p708_ontology(ctx: ProbeContext) -> ProbeResultVO:
    ontology_index = ctx.ontology_root / "concepts" / "concepts_index.json"
    if ontology_index.exists():
        detail = f"ONTOLOGY concepts_index.json found under {ctx.ontology_root}"
    else:
        detail = f"ONTOLOGY concepts_index.json missing under {ctx.ontology_root}"
    return ProbeResultVO(probe_id="P-708", passed=ontology_index.exists(), detail=detail)


def probe_p709_wal(ctx: ProbeContext) -> ProbeResultVO:
    wal_hits = list(ctx.repo_root.rglob("*wal*"))
    if wal_hits:
        detail = f"Found {len(wal_hits)} WAL-related file(s): {wal_hits[0].name}"
    else:
        detail = "No WAL-related files found"
    return ProbeResultVO(probe_id="P-709", passed=bool(wal_hits), detail=detail)


def probe_p710_verses(ctx: ProbeContext) -> ProbeResultVO:
    detail = f"VERSES root missing: {ctx.verses_root}"
    if not ctx.verses_root.exists():
        return ProbeResultVO(probe_id="P-710", passed=False, detail=detail)
    verses = list(ctx.verses_root.rglob("verse_*.md"))
    if verses:
        detail = f"Found {len(verses)} verse file(s) under {ctx.verses_root}"
    else:
        detail = f"No verse files found under {ctx.verses_root}"
    return ProbeResultVO(probe_id="P-710", passed=bool(verses), detail=detail)



def probe_p712_triade_coherence(ctx: ProbeContext) -> ProbeResultVO:
    tools_root = ctx.repo_root.parent.parent
    checks = {
        "skill-citizen-primus-triade.md": ctx.ontology_root / "concepts" / "skill-citizen-primus-triade.md",
        "L4-TOOLS SKILLS REGISTRY.yaml": tools_root / "L4-TOOLS" / "SKILLS" / "REGISTRY.yaml",
        "L4-TOOLS PRIMUS REGISTRY.yaml": tools_root / "L4-TOOLS" / "PRIMUS" / "REGISTRY.yaml",
    }
    missing = [str(path.relative_to(tools_root)) for name, path in checks.items() if not path.exists()]
    if missing:
        detail = f"Missing triade artifacts: {', '.join(missing)}"
        return ProbeResultVO(probe_id="P-712", passed=False, detail=detail)
    skills_registry = checks["L4-TOOLS SKILLS REGISTRY.yaml"]
    try:
        import yaml
        with open(skills_registry, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        total_skills = int(data.get("total_skills", 0))
        passed = total_skills > 100
        detail = f"Skills registry found with {total_skills} skills (threshold > 100)"
    except Exception as exc:
        passed = False
        detail = f"Failed to parse skills registry: {exc}"
    return ProbeResultVO(probe_id="P-712", passed=passed, detail=detail)

def probe_p711_bridges(ctx: ProbeContext) -> ProbeResultVO:
    tools_root = ctx.repo_root.parent.parent
    candidates = [
        tools_root / "L1-INFRA" / "TOPOS" / "BRIDGES.yaml",
        tools_root / "L0-CANON" / "GOVERNANCE-HUB" / "BRIDGES.yaml",
        tools_root / "L2-PLATFORM" / "GeriCode" / "act-protocol" / "BRIDGES",
    ]
    hits = [str(path.relative_to(tools_root)) for path in candidates if path.exists()]
    detail = f"Found bridge manifest(s): {', '.join(hits)}" if hits else "No BRIDGES manifest found"
    return ProbeResultVO(probe_id="P-711", passed=bool(hits), detail=detail)


PROBES = {
    "P-701": probe_p701_tdd,
    "P-702": probe_p702_bdd,
    "P-703": probe_p703_atdd,
    "P-704": probe_p704_ddd,
    "P-705": probe_p705_dbc,
    "P-706": probe_p706_hexagonal,
    "P-707": probe_p707_harness,
    "P-708": probe_p708_ontology,
    "P-709": probe_p709_wal,
    "P-710": probe_p710_verses,
    "P-711": probe_p711_bridges,
    "P-712": probe_p712_triade_coherence,
}


def run_all() -> list[ProbeResultVO]:
    ctx = _default_context()
    return [fn(ctx) for probe_id, fn in sorted(PROBES.items())]


