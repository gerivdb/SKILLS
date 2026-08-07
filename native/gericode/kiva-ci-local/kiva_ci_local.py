"""Skill — kiva-ci-local

Template et validation de .kiva/ci.yaml pour pipelines CI locales KIVA-CLI.
"""

from __future__ import annotations

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def generate_ci_yaml(target_dir: Path, *, stages: list[str] | None = None) -> Path:
    """Génère un fichier .kiva/ci.yaml.

    Args:
        target_dir: Répertoire du repo.
        stages: Liste des stages (défaut: lint, test, typecheck, validate).

    Returns:
        Chemin du fichier créé.
    """
    if stages is None:
        stages = ["lint", "test", "typecheck", "validate"]

    ci_path = target_dir / ".kiva" / "ci.yaml"
    ci_path.parent.mkdir(parents=True, exist_ok=True)

    content = "\n".join(
        [
            "name: n243-local-ci",
            'version: "1.0.0"',
            "status: active",
            "",
            "stages:",
        ]
        + [f"  - {stage}: kiva run {stage}" for stage in stages]
        + [
            "",
            "hooks:",
            "  pre_commit:",
            "    - kiva run lint",
            "  post_merge:",
            "    - kiva run test",
            "",
            "settings:",
            "  parallel: true",
            "  max_retries: 2",
            "  retry_delay: 5s",
            "  artifacts_dir: .kiva/artifacts",
            "  logs_dir: .kiva/logs",
            "",
        ]
    )

    ci_path.write_text(content, encoding="utf-8")
    logger.info("CI générée: %s", ci_path)
    return ci_path
