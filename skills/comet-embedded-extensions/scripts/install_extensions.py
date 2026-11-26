#!/usr/bin/env python3
"""Script: install_extensions.py
Rôle : Installer les 3 extensions CRX embarquées de Comet dans Chromium Profil 2 via CDP.
Contrainte : Attach-only CDP sur port 9222. Jamais de lancement Playwright/Pyppeteer destructeur.
"""
import json
import sys
import urllib.request
import urllib.error
import base64
import os
from pathlib import Path

CDP_URL = "http://localhost:9222"


def cdp_post(endpoint: str, data: dict | None = None, timeout: int = 10):
    """Envoyer une requête POST CDP et retourner la réponse JSON."""
    url = f"{CDP_URL}{endpoint}"
    body = json.dumps(data or {}).encode("utf-8") if data else b""
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"ERREUR_CDP {e.code} sur {url}: {body}")
        return None
    except urllib.error.URLError as e:
        print(f"ERREUR_CONNEXION_CDP {url}: {e}")
        return None


def cdp_get(endpoint: str, timeout: int = 10):
    """Envoyer une requête GET CDP et retourner la réponse JSON."""
    url = f"{CDP_URL}{endpoint}"
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"ERREUR_CDP_GET {url}: {e}")
        return None


def install_extension(crx_path: str, extension_id: str):
    """Installer une extension CRX via CDP Extension.install."""
    crx_file = Path(crx_path)
    if not crx_file.exists():
        print(f"ERREUR: Fichier CRX introuvable: {crx_path}")
        return False

    # Lire et encoder le CRX en base64
    crx_bytes = crx_file.read_bytes()
    crx_b64 = base64.b64encode(crx_bytes).decode("ascii")

    result = cdp_post("/json/Extension.install", {
        "extension": crx_b64,
    })
    if result is None:
        print(f"ERREUR: Impossible d'installer {extension_id} (pas de réponse CDP)")
        return False

    if result.get("success"):
        print(f"OK: Extension {extension_id} installée avec succès")
        return True
    else:
        print(f"ERREUR: Echec installation {extension_id}: {result}")
        return False


def read_external_extensions(registry_path: str):
    """Lire le registre external_extensions.json et retourner la liste des extensions."""
    registry = Path(registry_path)
    if not registry.exists():
        print(f"ERREUR: Registre introuvable: {registry_path}")
        return []

    with open(registry, "r", encoding="utf-8") as f:
        data = json.load(f)

    extensions = []
    for ext_id, ext_info in data.items():
        extensions.append({
            "id": ext_id,
            "version": ext_info.get("external_version", "unknown"),
            "crx_file": ext_info.get("external_crx", ""),
        })
    return extensions


def main():
    # Chemin du registre (relatif au dossier du skill ou chemin absolu)
    registry_path = os.environ.get(
        "COMET_EXTERNAL_EXTENSIONS_REGISTRY",
        str(Path(__file__).parent.parent / "references" / "comet-external-extensions.json"),
    )
    crx_dir = os.environ.get(
        "COMET_CRX_DIR",
        str(Path(__file__).parent.parent / "references" / "crx"),
    )

    print(f"[install_extensions] Registre: {registry_path}")
    print(f"[install_extensions] Répertoire CRX: {crx_dir}")

    extensions = read_external_extensions(registry_path)
    if not extensions:
        print("[install_extensions] Aucune extension trouvée dans le registre")
        sys.exit(1)

    print(f"[install_extensions] {len(extensions)} extension(s) à installer")

    for ext in extensions:
        crx_path = Path(crx_dir) / ext["crx_file"]
        print(f"[install_extensions] Installation de {ext['id']} (v{ext['version']}) depuis {crx_path}")
        success = install_extension(str(crx_path), ext["id"])
        if not success:
            print(f"[install_extensions] Echec pour {ext['id']}")
            sys.exit(1)

    print("[install_extensions] Toutes les extensions ont été installées")
    print("extensions_activees=true")


if __name__ == "__main__":
    main()