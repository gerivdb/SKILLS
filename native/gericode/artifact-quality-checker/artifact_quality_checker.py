"""Checks artifact quality for governance documents."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Sequence


@dataclass
class ProbeResult:
    id: str
    status: str


@dataclass
class CheckReport:
    score: float
    result: str
    artifact_type: str
    probes: List[ProbeResult]


class ArtifactQualityChecker:
    REQUIRED_SECTIONS: Sequence[str] = (
        "Contexte",
        "Décision",
        "Conséquences",
        "Alternatives",
        "Statut",
    )

    def __init__(self, output_dir: Path) -> None:
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def load_artifact(self, path: Path) -> dict:
        content = path.read_text(encoding="utf-8")
        return {"path": str(path), "content": content}

    def check(self, artifact: dict) -> CheckReport:
        content = artifact.get("content", "")
        artifact_type = "ADR"
        probes: List[ProbeResult] = []

        frontmatter_ok = content.startswith("---")
        probes.append(ProbeResult(id="P-106", status="PASS" if frontmatter_ok else "FAIL"))

        missing_sections = [
            section for section in self.REQUIRED_SECTIONS if f"## {section}" not in content
        ]
        probes.append(ProbeResult(id="P-107", status="PASS" if not missing_sections else "FAIL"))

        score = sum(1 for probe in probes if probe.status == "PASS") / len(probes)
        result = "PASS" if score == 1.0 else "FAIL"

        return CheckReport(score=score, result=result, artifact_type=artifact_type, probes=probes)

    def generate_report(self, report: CheckReport) -> Path:
        report_path = self.output_dir / "artifact-quality-report.yaml"
        lines = [
            f"score: {report.score}",
            f"result: {report.result}",
            f"artifact_type: {report.artifact_type}",
            "probes:",
        ]
        for probe in report.probes:
            lines.append(f"  - id: {probe.id}")
            lines.append(f"    status: {probe.status}")
        report_path.write_text("\n".join(lines), encoding="utf-8")
        return report_path
