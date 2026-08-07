"""Skill — yaml-safe-injector

Injecte des champs dans un YAML complexe sans corrompre la structure.
Préserve quoted strings multiline, ancres YAML, commentaires, ordre des clés.
"""

from __future__ import annotations

import difflib
import io
import shutil
from pathlib import Path
from typing import Any

from ruamel.yaml import YAML


class YAMLInjectionError(Exception):
    """Erreur lors de l'injection YAML."""


def inject_yaml(
    target_path: Path,
    updates: dict[str, Any],
    *,
    dry_run: bool = False,
    create_backup: bool = True,
) -> tuple[Path, str]:
    """Injecte des champs dans un fichier YAML en préservant sa structure.

    Args:
        target_path: Chemin du fichier YAML cible.
        updates: Dictionnaire des champs à injecter/mettre à jour.
        dry_run: Si True, ne écrit pas le fichier, retourne juste le diff.
        create_backup: Si True, crée un backup .bak avant écriture.

    Returns:
        Tuple (chemin_final, diff_unifique).

    Raises:
        YAMLInjectionError: Si le parsing ou la validation échoue.
    """
    if not target_path.exists():
        raise YAMLInjectionError(f"Fichier introuvable: {target_path}")

    original_text = target_path.read_text(encoding="utf-8")

    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 4096

    try:
        data = yaml.load(original_text)
    except Exception as exc:
        raise YAMLInjectionError(f"Parse YAML échoué: {exc}") from exc

    if data is None:
        data = {}

    if not isinstance(data, dict):
        raise YAMLInjectionError("La racine du YAML n'est pas un mapping.")

    _apply_updates(data, updates)

    output_buffer = io.StringIO()
    yaml.dump(data, output_buffer)
    new_text = output_buffer.getvalue()

    # Normaliser les line endings pour le diff
    original_lines = original_text.splitlines()
    new_lines = new_text.splitlines()
    diff = "\n".join(
        difflib.unified_diff(
            original_lines,
            new_lines,
            fromfile=str(target_path),
            tofile=str(target_path),
            lineterm="",
        )
    )

    if dry_run:
        return target_path, diff

    if create_backup:
        backup_path = target_path.with_suffix(target_path.suffix + ".bak")
        shutil.copy2(target_path, backup_path)

    target_path.write_text(new_text, encoding="utf-8")

    # Validation post-écriture
    try:
        yaml.load(new_text)
    except Exception as exc:
        # Rollback automatique
        if create_backup and backup_path.exists():
            shutil.copy2(backup_path, target_path)
        raise YAMLInjectionError(f"Validation post-écriture échouée, rollback effectué: {exc}") from exc
    finally:
        # Supprimer le backup après succès ou rollback
        if create_backup and backup_path.exists():
            backup_path.unlink()

    return target_path, diff


def _apply_updates(data: dict[str, Any], updates: dict[str, Any]) -> None:
    """Applique les mises à jour de manière récursive."""
    for key, value in updates.items():
        if isinstance(value, dict) and isinstance(data.get(key), dict):
            _apply_updates(data[key], value)
        else:
            data[key] = value


def rollback(target_path: Path) -> None:
    """Restaure le fichier depuis le backup .bak."""
    backup_path = target_path.with_suffix(target_path.suffix + ".bak")
    if not backup_path.exists():
        raise YAMLInjectionError(f"Backup introuvable: {backup_path}")
    shutil.copy2(backup_path, target_path)
    backup_path.unlink()
