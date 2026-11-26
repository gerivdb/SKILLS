#!/usr/bin/env python3
"""Script: verify_ntp_html.py
Rôle : Vérifier la structure HTML des pages NTP (ntp.html, index.html, sidecar/index.html).
"""
import sys
from pathlib import Path


def check_html(path: str) -> bool:
    p = Path(path)
    if not p.exists():
        print(f"ERREUR: Fichier introuvable: {path}")
        return False
    content = p.read_text(encoding="utf-8")
    checks = [
        ("doctype", "<!doctype html>" in content.lower()),
        ("meta charset", 'charset="utf-8"' in content),
        ("preconnect", "preconnect" in content),
        ("theme-color", "theme-color" in content),
        ("version meta", 'name="version"' in content),
        ("build meta", 'name="web-resources-build"' in content),
    ]
    all_ok = True
    for name, ok in checks:
        status = "OK" if ok else "MANQUANT"
        print(f"  {path}: {name} — {status}")
        if not ok:
            all_ok = False
    return all_ok


def main():
    files = [
        "spa/ntp.html",
        "spa/index.html",
        "sidecar/index.html",
    ]
    base = Path(__file__).parent.parent
    all_ok = True
    for f in files:
        if not check_html(str(base / f)):
            all_ok = False
    if all_ok:
        print("ntp_valide=true")
        print("Toutes les pages NTP sont valides (doctype, charset, preconnect, theme-color, meta versioning)")
        sys.exit(0)
    else:
        print("ntp_valide=false")
        print("Certaines pages NTP presentent des anomalies")
        sys.exit(1)


if __name__ == "__main__":
    main()