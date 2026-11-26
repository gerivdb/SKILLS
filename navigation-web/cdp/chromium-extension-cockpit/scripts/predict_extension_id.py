#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
predict_extension_id.py — Calculateur d'ID d'extension Chromium (Cas A et Cas B).

Reproduit l'algorithme interne Chromium (Extension::GenerateIdForPath) pour une
extension non empaquetée (unpacked) :

Cas A — Sans champ "key" dans manifest.json :
  1. Chemin absolu canonique du dossier (minuscules, slashes normalisés /)
  2. SHA-256 UTF-8 du chemin
  3. 16 premiers octets du digest
  4. Chaque octet -> 2 caracteres Base26 sur l'alphabet a-p (4 bits par caractere)
     => ID de exactement 32 caracteres [a-p]

Cas B — Avec champ "key" (clé publique RSA au format SubjectPublicKeyInfo DER,
encodée en Base64 dans manifest.json) :
  1. Décoder la clé publique Base64 (DER / SPKI)
  2. SHA-256 des octets DER
  3. 16 premiers octets du digest
  4. Chaque octet -> 2 caracteres Base26 sur l'alphabet a-p (4 bits par caractere)
     => ID de exactement 32 caracteres [a-p]

Usage :
    python predict_extension_id.py <chemin_dossier_extension>        [Cas A]
    python predict_extension_id.py --key <base64_public_key>          [Cas B]
    python predict_extension_id.py --manifest <chemin/manifest.json>  [Cas A ou B auto]

Exemples :
    python predict_extension_id.py "D:\DO\WEB\TOOLS\L4-TOOLS\GEM-X"
    python predict_extension_id.py --manifest "C:\Temp\OpenCode_Fork\dist\manifest.json"

Code de retour : 0 = OK, affiche l'ID prédit sur stdout.
"""

import base64
import hashlib
import json
import sys
from pathlib import Path

ALPHABET = "abcdefghijklmnop"  # 0->a ... 15->p (4 bits par caractere)


def _digest_to_id(digest: bytes) -> str:
    """Traduit les 16 premiers octets d'un digest SHA-256 en ID Base26 (32 chars)."""
    out = []
    for byte in digest[:16]:
        out.append(ALPHABET[(byte >> 4) & 0xF])
        out.append(ALPHABET[byte & 0xF])
    return "".join(out)


def canonicalize_path(path: str) -> str:
    """Chemin absolu canonique : resolve, minuscules, forward slashes."""
    resolved = Path(path).resolve()
    return resolved.as_posix().lower()


def path_to_extension_id(path: str) -> str:
    """Calcule l'ID Chromium deterministic pour un dossier d'extension (Cas A)."""
    canon = canonicalize_path(path)
    digest = hashlib.sha256(canon.encode("utf-8")).digest()
    return _digest_to_id(digest)


def public_key_to_extension_id(b64_public_key: str) -> str:
    """Calcule l'ID Chromium deterministic à partir d'une clé publique RSA
    encodée en Base64 (format SubjectPublicKeyInfo DER) — Cas B."""
    der = base64.b64decode(b64_public_key)
    digest = hashlib.sha256(der).digest()
    return _digest_to_id(digest)


def manifest_to_extension_id(manifest_path: str) -> tuple[str, str]:
    """Détecte Cas A ou Cas B selon la présence de "key" dans le manifest.
    Retourne (id_predictif, mode_utilise)."""
    manifest_file = Path(manifest_path)
    if not manifest_file.exists():
        raise FileNotFoundError(f"manifest.json introuvable : {manifest_path}")

    manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    key = manifest.get("key")
    if key:
        # Cas B : clé publique présente
        ext_id = public_key_to_extension_id(key)
        return ext_id, "B (clé publique)"
    else:
        # Cas A : pas de clé, utilisation du chemin du dossier
        ext_id = path_to_extension_id(str(manifest_file.parent))
        return ext_id, "A (chemin)"


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)

    arg = sys.argv[1]

    if arg == "--manifest" and len(sys.argv) >= 3:
        ext_id, mode = manifest_to_extension_id(sys.argv[2])
        print(f"[MODE {mode}] ID prédit : {ext_id}")
        print(ext_id)
        sys.exit(0)

    if arg == "--key" and len(sys.argv) >= 3:
        ext_id = public_key_to_extension_id(sys.argv[2])
        print(f"[MODE B (clé publique)] ID prédit : {ext_id}")
        print(ext_id)
        sys.exit(0)

    # Cas par défaut : chemin de dossier (Cas A)
    ext_path = arg
    if not Path(ext_path).exists():
        print(f"[ERREUR] Dossier introuvable : {ext_path}", file=sys.stderr)
        sys.exit(1)

    ext_id = path_to_extension_id(ext_path)
    print(f"[MODE A (chemin)] ID prédit : {ext_id}")
    print(ext_id)


if __name__ == "__main__":
    main()
