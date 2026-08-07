"""Local verse mapping for N243 anamorphic reuse.

This mapping supplements known_repositories.yaml until its verse_mapping
fields can be injected safely without YAML corruption.
"""

from __future__ import annotations

from pathlib import Path

VERSE_MAP: dict[str, str] = {
    "VERSES": "verse",
    "TINA": "verse",
    "TQL": "verse",
    "SPIDX": "verse",
    "KORX": "verse",
    "TALEX": "verse",
    "BATVERSE": "verse",
    "HOLMES": "verse",
    "auto-dev": "verse",
    "SABRE": "verse",
}


def verse_for(name: str) -> str:
    return VERSE_MAP.get(name, "none")
