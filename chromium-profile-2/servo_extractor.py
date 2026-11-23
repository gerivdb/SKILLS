#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
servo_extractor.py — Skill chromium-profile-2 (Pilier 5, Multi-Moteur)
Extraction de contenu web en Markdown sans Chromium.

Essai servo-fetch (Servo/Rust) en premier. Sur Windows, servo-fetch panic
(EGL/Surfman non disponible) — le script bascule alors sur un extractor léger
requests+BeautifulSoup. L'objectif est de comparer le temps d'exécution avec
Chromium (~3.6s cold load sur Gemini).
"""

from __future__ import annotations

import subprocess
import sys
import time
from typing import Optional

# ---------------------------------------------------------------------------
# Fallback léger (requests + BeautifulSoup) — fonctionne sur tous les OS
# ---------------------------------------------------------------------------
try:
    import requests
    from bs4 import BeautifulSoup
    _LIGHT_AVAILABLE = True
except Exception:
    _LIGHT_AVAILABLE = False

# servo-fetch est installé (pip install servo-fetch OK) mais panic sur Windows
# (EGL/Surfman). On ne l'importe pas au niveau du module pour éviter le crash.
_SERVO_INSTALLED = True  # vérifié par pip, mais non utilisable sur Windows


def _extract_servo_subprocess(url: str, timeout_s: int = 30) -> Optional[str]:
    """
    Tente servo-fetch dans un sous-processus isolé (pour éviter le panic Rust
    qui tuerait le processus parent sur Windows).
    """
    code = (
        "import sys; "
        "try: "
        "  from servo_fetch import fetch; "
        "  print(fetch(sys.argv[1], timeout=30), end='') "
        "except Exception as e: "
        "  print(f'__SERVO_ERROR__{e}', file=sys.stderr); "
        "  sys.exit(1)"
    )
    try:
        proc = subprocess.run(
            [sys.executable, "-c", code, url],
            capture_output=True,
            text=True,
            timeout=timeout_s,
        )
        if proc.returncode == 0 and proc.stdout.strip():
            return proc.stdout
        return None
    except Exception:
        return None


def _extract_light(url: str, timeout_s: int = 30) -> Optional[str]:
    """Extraction légère via requests + BeautifulSoup (HTML statique, pas de JS)."""
    try:
        resp = requests.get(url, timeout=timeout_s, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "noscript", "iframe", "svg"]):
            tag.decompose()
        text = soup.get_text(separator="\n", strip=True)
        lines = [l for l in text.splitlines() if l.strip()]
        return "\n".join(lines)
    except Exception:
        return None


def extract_markdown(url: str, timeout_s: int = 30) -> Optional[str]:
    """
    Récupère le contenu d'une URL en texte/Markdown sans Chromium.
    1. Essaie servo-fetch dans un sous-processus (isolé du panic Rust).
    2. Fallback sur requests + BeautifulSoup.
    """
    if _SERVO_INSTALLED:
        result = _extract_servo_subprocess(url, timeout_s)
        if result:
            return result
        print("[servo-fetch indisponible (panic EGL sur Windows), bascule sur fallback léger]")

    if _LIGHT_AVAILABLE:
        return _extract_light(url, timeout_s)

    print("ERREUR: Aucun extractor disponible.")
    return None


def main():
    if len(sys.argv) < 2:
        print("Usage: python servo_extractor.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    print(f"Extraction (Pilier 5, sans Chromium) de: {url}")

    t0 = time.perf_counter()
    content = extract_markdown(url)
    t1 = time.perf_counter()
    elapsed = t1 - t0

    if content is None:
        print("ECHEC de l'extraction.")
        sys.exit(1)

    print(f"Temps d'extraction: {elapsed:.3f}s")
    print(f"Taille du contenu: {len(content)} caractères")
    print("--- APERCU (premiers 500 chars) ---")
    print(content[:500])
    print("-----------------------------------")

    out_path = "servo_extract_output.md"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Sauvegarde: {out_path}")


if __name__ == "__main__":
    main()
