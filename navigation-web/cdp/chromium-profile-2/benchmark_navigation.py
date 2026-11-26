#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
benchmark_navigation.py — Skill chromium-profile-2 (Shard B, v4)
Benchmark de navigation event-driven :
  • Session pooling (WebSocket persistant) — Pilier 1
  • Event-driven navigation : attend Page.loadEventFired (événement CDP natif) au lieu de sleep/polling
  • Extraction de densité DOM (Pilier 3)
"""

import sys
import time
import json
from pathlib import Path

# Importer ChromiumCDPClient (dans le même dossier que ce script)
sys.path.insert(0, str(Path(__file__).resolve().parent))

from chromium_cdp_client import ChromiumCDPClient

# Importer MA3 SlidingWindow (REF-182)
MA3_PATH = Path(__file__).resolve().parent.parent / "ma3_algorithms"
if str(MA3_PATH) not in sys.path:
    sys.path.insert(0, str(MA3_PATH))
from sliding_window import SlidingWindow  # noqa: E402

# --- Extraction texte DOM complet via SlidingWindow (Pilier 3, MA3 REF-182) ---
# Remplace DENSITY_JS qui retournait 0 char sur le Shadow DOM de Gemini.
# Le filtrage des menus/pubs se fait cote Python via les chunks densement remplis.


def _dom_size(result):
    if result is None:
        return 0
    if isinstance(result, dict):
        value = result.get("result", {}).get("value", "")
        if isinstance(value, str):
            return len(value)
        return len(str(value))
    return len(str(result))


def main():
    client = ChromiumCDPClient()

    status = client.start_browser()
    print(f"Browser: {status['status']} sur port {status['port']}")

    # Onglet vierge
    tab = client.open_tab("about:blank")
    target_id = tab.get("targetId")
    print(f"Onglet ouvert: {target_id}")

    # --- Navigation event-driven : attend Page.loadEventFired ---
    t_nav_start = time.perf_counter()
    nav_result = client.navigate("https://gemini.google.com/app")
    t_nav_end = time.perf_counter()
    nav_time = t_nav_end - t_nav_start

    loaded = nav_result.get("loaded", False)
    load_event = nav_result.get("load_event")
    print(f"Page chargée (loadEventFired): {loaded} — temps de navigation: {nav_time:.3f}s")
    if load_event:
        params = load_event.get("params", {})
        print(f"  loadEventFired timestamp: {params.get('timestamp', 'N/A')}")

    # --- Attente de la réponse complète via le pont DOM (Sensor/Reader) ---
    t_extract_start = time.perf_counter()
    dense_text = client.wait_for_response_complete(timeout=30.0)
    t_extract_end = time.perf_counter()
    extract_time = t_extract_end - t_extract_start

    # Filtrage par SlidingWindow sur le texte reçu (Pilier 3)
    sliding_chunks = SlidingWindow.dom_density(dense_text, window_size=4096, min_chars=256)
    dense_chars = sum(len(c) for _, _, c in sliding_chunks)
    chunk_count = len(sliding_chunks)

    print("=== RÉSULTAT BENCHMARK NAVIGATION v4 (MA3 Sensor/Reader) ===")
    print(f"URL: https://gemini.google.com")
    print(f"Temps de navigation (navigate→loadEventFired): {nav_time:.3f}s")
    print(f"Temps d'attente réponse (Sensor/Reader): {extract_time:.3f}s")
    print(f"Contenu sémantique extrait: {dense_chars} caractères ({chunk_count} chunks)")
    print(f"Aperçu: {dense_text[:200]}...")
    print("============================================================")

    client.disconnect()

    return {
        "url": "https://gemini.google.com",
        "navigation_time_s": round(nav_time, 3),
        "dom_extraction_time_s": round(extract_time, 3),
        "semantic_content_chars": dense_chars,
        "semantic_preview": dense_text[:200],
        "loaded": loaded,
        "chunk_count": chunk_count,
    }


if __name__ == "__main__":
    result = main()
    print(f"Benchmark JSON: {json.dumps(result, ensure_ascii=False)}")
