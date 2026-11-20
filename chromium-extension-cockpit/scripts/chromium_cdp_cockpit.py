#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
chromium_cdp_cockpit.py — Registre Opératoire Chromium / CDP Cockpit
Primitives de pilotage et de preuve pour extensions Chromium (ENV3 / Sidekeep-X / DEEP-X / GEM-X / QWX).

Actions supportées :
  - status    : Liste les extensions installées, leurs versions et état d'erreurs
  - reload    : Rechargement à chaud d'une extension via son ID
  - clear-errors : Purge le journal d'erreurs d'une extension (Clear All)
  - frames    : Inspection de la hiérarchie iframes d'une extension (panel)
  - version   : Preuve Disque vs Live (manifest version vs runtime version)
  - audit     : Audit de santé global des extensions (matrice de santé)

Requiert : playwright (pip install playwright).
Si le port CDP 9222 est fermé, le script lance automatiquement une
micro-sandbox Chromium (launch_micro_sandbox.ps1) puis exécute l'action demandée.
"""

import argparse
import json
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sync_playwright = None

CDP_URL = "http://127.0.0.1:9222"

# ——————————————————————————————————————————————
# Utilitaires CDP HTTP (sans Playwright, pour le JSON brut)
# ——————————————————————————————————————————————

def cdp_list_targets():
    """Retourne la liste brute des cibles CDP actives (port 9222)."""
    req = urllib.request.Request(f"{CDP_URL}/json")
    with urllib.request.urlopen(req, timeout=5) as resp:
        return json.loads(resp.read().decode())

def cdp_check_port():
    """Vérifie que le port CDP 9222 répond. Retourne True/False."""
    try:
        cdp_list_targets()
        return True
    except Exception:
        return False

# Extension par défaut utilisée pour le auto-spawn de la micro-sandbox
# quand le port CDP est fermé. Doit disposer d'un manifest.json valide.
DEFAULT_SANDBOX_EXT = r"D:\DO\WEB\TOOLS\L0-CANON\ENV3-repo\sidekeep-x"
LAUNCHER_SCRIPT = r"D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\chromium-extension-cockpit\scripts\launch_micro_sandbox.ps1"


def ensure_cdp_port(timeout_s: float = 8.0) -> bool:
    """Garantit que le port CDP 9222 est joignable.

    Si le port ne répond pas, le script lance automatiquement en arrière-plan
    une micro-sandbox Chromium via ``launch_micro_sandbox.ps1`` (port 9222,
    profil éphémère), puis poll le socket jusqu'au timeout.

    Retourne True si le port est disponible, False sinon.
    """
    if cdp_check_port():
        return True

    print("[INFO] Port CDP 9222 fermé — auto-spawn de la micro-sandbox éphémère…")
    try:
        subprocess.Popen(
            [
                "pwsh",
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                LAUNCHER_SCRIPT,
                "-ExtensionPath",
                DEFAULT_SANDBOX_EXT,
                "-Port",
                "9222",
            ],
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
    except Exception as exc:
        print(f"[ERREUR] Échec du lancement de la sandbox : {exc}")
        return False

    deadline = time.time() + timeout_s
    while time.time() < deadline:
        time.sleep(0.5)
        if cdp_check_port():
            print("[SUCCÈS] Port CDP 9222 disponible après auto-spawn.")
            return True

    print(f"[ERREUR] Port CDP 9222 toujours indisponible après {timeout_s} s.")
    return False

# ——————————————————————————————————————————————
# Primitives Playwright (Shadow DOM, iframes, erreurs)
# ——————————————————————————————————————————————

def _connect_cdp():
    if sync_playwright is None:
        raise RuntimeError("playwright n'est pas installé. Exécutez : pip install playwright")
    p = sync_playwright().start()
    browser = p.chromium.connect_over_cdp(CDP_URL)
    context = browser.contexts[0]
    return p, browser, context

def _close_cdp(p, browser):
    browser.close()
    p.stop()

def cmd_status():
    """Affiche le statut des extensions (id, nom, version, erreurs, activé)."""
    if not ensure_cdp_port():
        print(json.dumps({"ok": False, "error": "Port CDP 9222 non joignable"}, ensure_ascii=False))
        return

    p, browser, context = _connect_cdp()
    try:
        page = context.new_page()
        page.goto("chrome://extensions", wait_until="networkidle")
        exts = page.evaluate("""() => {
            const mgr = document.querySelector('extensions-manager');
            const list = mgr?.shadowRoot?.querySelector('extensions-item-list');
            const items = list?.shadowRoot?.querySelectorAll('extensions-item') || [];
            return Array.from(items).map(it => {
                const shadow = it.shadowRoot;
                const nameEl = shadow?.querySelector('#name');
                const versionEl = shadow?.querySelector('#version');
                const errorsBtn = shadow?.querySelector('#errors-button');
                const toggle = shadow?.querySelector('#enable-toggle');
                return {
                    id: it.id,
                    name: nameEl?.textContent?.trim() || '',
                    version: versionEl?.textContent?.trim() || '',
                    hasErrors: !!errorsBtn,
                    enabled: toggle?.getAttribute('aria-pressed') === 'true'
                };
            });
        }""")
        page.close()
    finally:
        _close_cdp(p, browser)

    print(json.dumps({"ok": True, "extensions": exts}, indent=2, ensure_ascii=False))

def cmd_reload(ext_id):
    """Rechargement à chaud d'une extension via son ID Chromium.
    
    Si l'extension est désactivée, l'active d'abord (auto-réveil) avant
    de déclencher le rechargement.
    """
    if not ensure_cdp_port():
        print(json.dumps({"ok": False, "error": "Port CDP 9222 non joignable"}, ensure_ascii=False))
        return

    p, browser, context = _connect_cdp()
    try:
        page = context.new_page()
        page.goto("chrome://extensions", wait_until="networkidle")
        res = page.evaluate(f"""(id) => {{
            const mgr = document.querySelector('extensions-manager');
            const list = mgr?.shadowRoot?.querySelector('extensions-item-list');
            const item = list?.shadowRoot?.querySelector(`extensions-item[id="${id}"]`);
            if (!item) return {{ ok: false, error: "Extension introuvable" }};
            const shadow = item.shadowRoot;
            let btn = shadow?.querySelector('#dev-reload-button');
            if (!btn) {{
                // Extension désactivée : activer d'abord (auto-réveil)
                const toggle = shadow?.querySelector('#enable-toggle');
                if (!toggle) return {{ ok: false, error: "Extension désactivée et toggle d'activation introuvable" }};
                toggle.click();
                return {{ ok: false, error: "Extension désactivée — activation demandée. Relancez la commande reload." }};
            }}
            btn.click();
            const nameEl = shadow?.querySelector('#name');
            return {{ ok: true, id: id, name: nameEl?.textContent?.trim() || '' }};
        }}""", ext_id)
        page.close()
    finally:
        _close_cdp(p, browser)

    print(json.dumps(res, indent=2, ensure_ascii=False))

def cmd_clear_errors(ext_id):
    """Purge le journal d'erreurs d'une extension (bouton Clear All)."""
    if not ensure_cdp_port():
        print(json.dumps({"ok": False, "error": "Port CDP 9222 non joignable"}, ensure_ascii=False))
        return

    p, browser, context = _connect_cdp()
    try:
        page = context.new_page()
        page.goto(f"chrome://extensions/?errors={ext_id}", wait_until="networkidle")
        res = page.evaluate("""() => {
            const mgr = document.querySelector('extensions-manager');
            const view = mgr?.shadowRoot?.querySelector('extensions-error-page');
            if (!view) return { cleared: false, reason: "Page d'erreurs introuvable" };
            const buttons = view.shadowRoot?.querySelectorAll('cr-button') || [];
            for (const btn of buttons) {
                const label = (btn.textContent || '').toLowerCase();
                if (label.includes('effacer') || label.includes('clear') || label.includes('tout effacer') || label.includes('clear all')) {
                    btn.click();
                    return { cleared: true };
                }
            }
            return { cleared: false, reason: "Aucun bouton de purge trouvé" };
        }""")
        page.close()
    finally:
        _close_cdp(p, browser)

    print(json.dumps(res, indent=2, ensure_ascii=False))

def cmd_frames(ext_id):
    """Inspecte la hiérarchie iframes d'une extension (side panel / popup)."""
    if not ensure_cdp_port():
        print(json.dumps({"ok": False, "error": "Port CDP 9222 non joignable"}, ensure_ascii=False))
        return

    p, browser, context = _connect_cdp()
    try:
        page = context.new_page()
        page.goto(f"chrome-extension://{ext_id}/panel/index.html", wait_until="domcontentloaded")
        page.wait_for_timeout(2500)
        frames_list = []
        for f in page.frames:
            frames_list.append({
                "url": f.url,
                "name": f.name,
                "parent": f.parent_frame.url if f.parent_frame else None
            })
        page.close()
    except Exception as e:
        # Tentative fallback sur popup
        try:
            page = context.new_page()
            page.goto(f"chrome-extension://{ext_id}/popup.html", wait_until="domcontentloaded")
            page.wait_for_timeout(2500)
            frames_list = []
            for f in page.frames:
                frames_list.append({
                    "url": f.url,
                    "name": f.name,
                    "parent": f.parent_frame.url if f.parent_frame else None
                })
            page.close()
        except Exception as e2:
            p, browser, context = None, None, None
            print(json.dumps({"ok": False, "error": str(e2)}, ensure_ascii=False))
            return
    finally:
        if p:
            browser.close()
            p.stop()

    print(json.dumps({"ok": True, "extension_id": ext_id, "frames": frames_list}, indent=2, ensure_ascii=False))

def cmd_version(manifest_path):
    """Preuve Disque vs Live : compare version disque et version live via CDP."""
    manifest = Path(manifest_path)
    if not manifest.exists():
        print(json.dumps({"ok": False, "error": f"Fichier introuvable : {manifest_path}"}, ensure_ascii=False))
        return

    manifest_data = json.loads(manifest.read_text(encoding="utf-8"))
    disk_version = manifest_data.get("version", "unknown")
    manifest_name = manifest_data.get("name", manifest.parent.name).lower()

    if not ensure_cdp_port():
        print(json.dumps({
            "ok": False,
            "error": "Port CDP 9222 non joignable",
            "disk_version": disk_version
        }, ensure_ascii=False))
        return

    p, browser, context = _connect_cdp()
    try:
        page = context.new_page()
        page.goto("chrome://extensions", wait_until="networkidle")
        live_version = page.evaluate(f"""(name) => {{
            const mgr = document.querySelector('extensions-manager');
            const list = mgr?.shadowRoot?.querySelector('extensions-item-list');
            const items = list?.shadowRoot?.querySelectorAll('extensions-item') || [];
            const nLower = name.toLowerCase();
            for (const it of items) {{
                const n = it.shadowRoot?.querySelector('#name')?.textContent?.trim().toLowerCase();
                if (n === nLower || n.includes(nLower)) {{
                    return it.shadowRoot?.querySelector('#version')?.textContent?.trim() || 'unknown';
                }}
            }}
            return 'not_found';
        }}""", manifest_name)
        page.close()
    finally:
        _close_cdp(p, browser)

    match = (str(live_version) == str(disk_version))
    print(json.dumps({
        "ok": True,
        "manifest_path": str(manifest),
        "disk_version": disk_version,
        "live_version": live_version,
        "match": match
    }, indent=2, ensure_ascii=False))

def cmd_audit():
    """Audit de santé global des extensions via CDP (matrice de santé)."""
    if not ensure_cdp_port():
        print(json.dumps({"ok": False, "error": "Port CDP 9222 non joignable"}, ensure_ascii=False))
        return

    p, browser, context = _connect_cdp()
    try:
        page = context.new_page()
        page.goto("chrome://extensions", wait_until="networkidle")
        exts = page.evaluate("""() => {
            const mgr = document.querySelector('extensions-manager');
            const list = mgr?.shadowRoot?.querySelector('extensions-item-list');
            const items = list?.shadowRoot?.querySelectorAll('extensions-item') || [];
            return Array.from(items).map(it => {
                const shadow = it.shadowRoot;
                const nameEl = shadow?.querySelector('#name');
                const versionEl = shadow?.querySelector('#version');
                const errorsBtn = shadow?.querySelector('#errors-button');
                const toggle = shadow?.querySelector('#enable-toggle');
                return {
                    id: it.id,
                    name: nameEl?.textContent?.trim() || 'Inconnu',
                    version: versionEl?.textContent?.trim() || '?',
                    hasErrors: !!errorsBtn,
                    enabled: toggle?.getAttribute('aria-pressed') === 'true'
                };
            });
        }""")
        page.close()
    finally:
        _close_cdp(p, browser)

    # Tableau de santé
    print("+----------------------------+---------+---------+------------------+----------------------+")
    print("| Extension                  | Version | Runtime | Backend Requis   | Statut Santé         |")
    print("+----------------------------+---------+---------+------------------+----------------------+")
    for e in exts:
        name = e['name'][:26].ljust(26)
        version = e['version'][:7].ljust(7)
        runtime = "Actif" if e['enabled'] else "Inactif"
        runtime = runtime[:9].ljust(9)
        backend = "-"
        if e['hasErrors']:
            health = "❌ ERREURS".ljust(20)
        elif not e['enabled']:
            health = "⚠️ DÉSACTIVÉE".ljust(20)
        else:
            health = "✅ 0 erreur".ljust(20)
        print(f"| {name} | {version} | {runtime} | {backend.ljust(16)} | {health} |")
    print("+----------------------------+---------+---------+------------------+----------------------+")
    print(f"\nTotal : {len(exts)} extension(s) détectée(s).")
    healthy = sum(1 for e in exts if e['enabled'] and not e['hasErrors'])
    print(f"Santé : {healthy}/{len(exts)} opérationnelle(s).")


# ——————————————————————————————————————————————
# Point d'entrée
# ——————————————————————————————————————————————

def main():
    parser = argparse.ArgumentParser(description="Chromium CDP Cockpit — Pilotage et preuve d'extensions Chromium")
    sub = parser.add_subparsers(dest="action", required=True)

    sub.add_parser("status", help="Liste les extensions installées et leur état")
    p_reload = sub.add_parser("reload", help="Rechargement à chaud d'une extension")
    p_reload.add_argument("--id", required=True, help="ID Chromium de l'extension")
    p_clear = sub.add_parser("clear-errors", help="Purge le journal d'erreurs d'une extension")
    p_clear.add_argument("--id", required=True, help="ID Chromium de l'extension")
    p_frames = sub.add_parser("frames", help="Inspecte les iframes d'une extension (panel/popup)")
    p_frames.add_argument("--id", required=True, help="ID Chromium de l'extension")
    p_version = sub.add_parser("version", help="Preuve Disque vs Live (manifest version)")
    p_version.add_argument("--manifest", required=True, help="Chemin vers manifest.json sur disque")
    p_audit = sub.add_parser("audit", help="Audit de santé global des extensions (matrice)")

    args = parser.parse_args()

    if args.action == "status":
        cmd_status()
    elif args.action == "reload":
        cmd_reload(args.id)
    elif args.action == "clear-errors":
        cmd_clear_errors(args.id)
    elif args.action == "frames":
        cmd_frames(args.id)
    elif args.action == "version":
        cmd_version(args.manifest)
    elif args.action == "audit":
        cmd_audit()

if __name__ == "__main__":
    main()
