#!/usr/bin/env python3
"""
dump_cdp_page.py — Extraction de page CDP sans Playwright.

Se connecte au serveur CDP natif sur 127.0.0.1:9222, liste les targets,
sélectionne celle dont l'URL correspond au filtre, et dump le texte brut
du corps de la page dans un fichier de sortie.

Zéro dépendance à Playwright. Utilise uniquement `websockets` (déjà installé)
et la bibliothèque standard Python.

Conforme à la règle Absolute Portability : toutes les ressources adjacentes
sont localisées via Path(__file__).parent.
"""

import argparse
import asyncio
import json
import sys
from pathlib import Path

import websockets

CDP_HOST = "127.0.0.1"
CDP_PORT = 9222
CDP_JSON_URL = f"http://{CDP_HOST}:{CDP_PORT}/json"


def list_targets() -> list[dict]:
    """Récupère la liste des targets CDP disponibles sur le port 9222."""
    import urllib.request

    with urllib.request.urlopen(CDP_JSON_URL, timeout=5) as resp:
        return json.loads(resp.read().decode("utf-8"))


def find_target(targets: list[dict], url_filter: str | None) -> dict | None:
    """Sélectionne la target correspondant au filtre d'URL."""
    for t in targets:
        if url_filter and url_filter in t.get("url", ""):
            return t
        if not url_filter and t.get("type") == "page":
            return t
    return None


async def dump_page(target: dict, output_path: Path | None) -> str:
    """Se connecte en WebSocket à la target et extrait document.body.innerText."""
    ws_url = target["webSocketDebuggerUrl"]
    async with websockets.connect(ws_url) as ws:
        await ws.send(
            json.dumps(
                {
                    "id": 1,
                    "method": "Runtime.evaluate",
                    "params": {"expression": "document.body.innerText"},
                }
            )
        )
        res = json.loads(await ws.recv())
        text = res.get("result", {}).get("result", {}).get("value", "")

    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(text, encoding="utf-8")

    return text


async def main(url_filter: str | None, output_path: Path | None) -> int:
    targets = list_targets()
    if not targets:
        print("[dump_cdp_page] Aucune target CDP trouvée sur 127.0.0.1:9222")
        return 1

    target = find_target(targets, url_filter)
    if target is None:
        print(
            f"[dump_cdp_page] Aucune target correspondant au filtre '{url_filter}'"
        )
        print("[dump_cdp_page] Targets disponibles :")
        for t in targets:
            print(f"  - {t.get('type')} | {t.get('url')} | {t.get('targetId')}")
        return 1

    text = await dump_page(target, output_path)
    if output_path is not None:
        print(
            f"[dump_cdp_page] Dump réussi : {len(text)} caractères dans {output_path}"
        )
    else:
        print(text)
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dump une page CDP via le port 9222")
    parser.add_argument(
        "--url",
        dest="url_filter",
        default=None,
        help="Filtre d'URL pour sélectionner la target (ex: qwen.ai)",
    )
    parser.add_argument(
        "--output",
        dest="output_path",
        type=Path,
        default=None,
        help="Chemin du fichier de sortie (défaut : affichage stdout)",
    )
    args = parser.parse_args()

    sys.exit(asyncio.run(main(args.url_filter, args.output_path)))
