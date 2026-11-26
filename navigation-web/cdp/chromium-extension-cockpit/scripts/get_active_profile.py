#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
get_active_profile.py — Inspecteur du profil Chromium actuellement en cours.

Interroge chrome://version via le port CDP 9222 pour extraire avec certitude
le nom et le chemin absolu du profil actif (ex:
  Profile Name: Profil 2
  Profile Path: C:\Users\GG\AppData\Local\Chromium\User Data\Profile 2).

Requiert : playwright (pip install playwright) et le port CDP 9222 ouvert.

Usage :
    python get_active_profile.py
    python get_active_profile.py --json

Code de retour : 0 = OK, affiche le profil sur stdout.
"""

import argparse
import json
import sys
import urllib.request

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sync_playwright = None

CDP_URL = "http://127.0.0.1:9222"


def cdp_check_port() -> bool:
    try:
        req = urllib.request.Request(f"{CDP_URL}/json")
        with urllib.request.urlopen(req, timeout=5) as resp:
            json.loads(resp.read().decode())
        return True
    except Exception:
        return False


def get_active_profile() -> dict:
    if sync_playwright is None:
        return {"ok": False, "error": "playwright non installe (pip install playwright)"}
    if not cdp_check_port():
        return {"ok": False, "error": "Port CDP 9222 non joignable"}

    p = sync_playwright().start()
    try:
        browser = p.chromium.connect_over_cdp(CDP_URL)
        context = browser.contexts[0]
        page = context.new_page()
        try:
            page.goto("chrome://version", wait_until="networkidle")
            page.wait_for_timeout(1500)
            profile = page.evaluate("""() => {
                const get = (id) => {
                    const el = document.getElementById(id);
                    return el ? el.textContent.trim() : null;
                };
                return {
                    profile_name: get("profile_name"),
                    profile_path: get("profile_path"),
                    command_line: get("command_line"),
                    user_data_dir: get("user_data_dir"),
                };
            }""")
        finally:
            page.close()
            browser.close()
            p.stop()
    except Exception as exc:
        try:
            p.stop()
        except Exception:
            pass
        return {"ok": False, "error": str(exc)}

    return {"ok": True, **profile}


def main():
    parser = argparse.ArgumentParser(description="Inspecteur du profil Chromium actif via CDP")
    parser.add_argument("--json", action="store_true", help="Sortie JSON brute")
    args = parser.parse_args()

    result = get_active_profile()
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if not result.get("ok"):
            print(f"[ERREUR] {result.get('error')}", file=sys.stderr)
            sys.exit(1)
        print(f"Profile Name : {result.get('profile_name')}")
        print(f"Profile Path : {result.get('profile_path')}")
        if result.get("user_data_dir"):
            print(f"User Data Dir: {result.get('user_data_dir')}")
        if result.get("command_line"):
            print(f"Command Line : {result.get('command_line')}")


if __name__ == "__main__":
    main()
