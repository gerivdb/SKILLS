#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ccp_cli.py — CLI d'orchestration d'installation autonome d'extensions Chromium.

Assemble les 3 primitives du cockpit :
  1. predict_extension_id.py   -> ID deterministe (Cas A, sans cle)
  2. get_active_profile.py     -> Profil Chromium actif via chrome://version
  3. auto_load_unpacked.ps1    -> Hook Windows IFileDialog (remplissage sans clic humain)

Commandes :
  ccp_cli.py predict-id --path <dossier>
  ccp_cli.py active-profile
  ccp_cli.py extensions install --path <dossier> [--timeout 30]

L'installation orchestre :
  - Arme le hook PS1 en arriere-plan (AVANT le clic CDP)
  - Ouvre chrome://extensions via CDP, active le Mode Developpeur
  - Clic sur le bouton "Charger l'extension non empaquetée" (#loadUnpacked)
  - Le hook PS1 remplit le dialogue IFileDialog et valide
  - Verifie la presence de l'ID predit via `status`

Code de retour : 0 = installation verifiee, 1 = echec.
"""

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sync_playwright = None

# Importer les utilitaires CDP du cockpit (sous-dossier scripts/)
SCRIPT_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = SCRIPT_DIR / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from chromium_cdp_cockpit import (  # noqa: E402
    CDP_URL,
    ensure_cdp_port,
    _connect_cdp,
    _close_cdp,
)

PREDICT_SCRIPT = SCRIPTS_DIR / "predict_extension_id.py"
PROFILE_SCRIPT = SCRIPTS_DIR / "get_active_profile.py"
HOOK_SCRIPT = SCRIPTS_DIR / "auto_load_unpacked.ps1"

# ——————————————————————————————————————————————————————————————————————
# Appel des scripts autonomes (subprocess, pas d'import pour eviter les effets de bord)
# ——————————————————————————————————————————————————————————————————————

def run_predict_id(ext_path: str) -> str | None:
    """Retourne l'ID Chromium predict pour le dossier d'extension."""
    try:
        res = subprocess.run(
            [sys.executable, str(PREDICT_SCRIPT), ext_path],
            capture_output=True, text=True, timeout=15,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
        if res.returncode == 0:
            return res.stdout.strip()
        print(f"[WARN] predict_extension_id a echoue (rc={res.returncode}): {res.stderr.strip()}")
    except Exception as exc:
        print(f"[WARN] Impossible d'executer predict_extension_id.py : {exc}")
    return None


def run_active_profile() -> dict:
    """Retourne les infos du profil actif (dict) ou {} en echec."""
    try:
        res = subprocess.run(
            [sys.executable, str(PROFILE_SCRIPT), "--json"],
            capture_output=True, text=True, timeout=20,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
        if res.returncode == 0:
            return json.loads(res.stdout)
        print(f"[WARN] get_active_profile a echoue (rc={res.returncode}): {res.stderr.strip()}")
    except Exception as exc:
        print(f"[WARN] Impossible d'executer get_active_profile.py : {exc}")
    return {}


# ——————————————————————————————————————————————————————————————————————
# Primitives CDP pour l'installation (chrome://extensions)
# ——————————————————————————————————————————————————————————————————————

def _find_in_shadow(page, selectors):
    """Explore les shadow roots pour trouver un element correspondant a un des selecteurs CSS.
    Retourne le premier element handle trouve ou None."""
    js = """
    (selectors) => {
        function walk(root, depth) {
            if (depth > 8) return null;
            for (const sel of selectors) {
                const el = root.querySelector(sel);
                if (el) return el;
            }
            // Descendre dans les shadow roots
            const all = root.querySelectorAll('*');
            for (const node of all) {
                if (node.shadowRoot) {
                    const found = walk(node.shadowRoot, depth + 1);
                    if (found) return found;
                }
            }
            return null;
        }
        return walk(document, 0);
    }
    """
    return page.evaluate_handle(js, selectors)


def _click_by_text_or_id(page, candidates):
    """Tente de cliquer un element par id ou par texte (dans shadow DOM).
    candidates: liste de dict {id:.., text:..}"""
    js = """
    (candidates) => {
        function findAndClick(root, depth) {
            if (depth > 8) return false;
            // Par id
            for (const c of candidates) {
                if (c.id) {
                    const el = root.querySelector('#' + c.id);
                    if (el) { el.click(); return true; }
                }
            }
            // Par texte de bouton / cr-button / cr-toggle-button
            const buttons = root.querySelectorAll('cr-button, cr-toggle-button, button, a');
            for (const btn of buttons) {
                const txt = (btn.textContent || '').trim().toLowerCase();
                for (const c of candidates) {
                    if (c.text && txt.includes(c.text.toLowerCase())) {
                        btn.click();
                        return true;
                    }
                }
            }
            // Shadow descent
            const all = root.querySelectorAll('*');
            for (const node of all) {
                if (node.shadowRoot) {
                    if (findAndClick(node.shadowRoot, depth + 1)) return true;
                }
            }
            return false;
        }
        return findAndClick(document, 0);
    }
    """
    return page.evaluate(js, candidates)


def cmd_install(ext_path: str, timeout_sec: int = 30):
    """Installation autonome : predict ID -> arm hook -> CDP load unpacked -> verify."""
    ext_path_obj = Path(ext_path)
    if not ext_path_obj.exists():
        print(json.dumps({"ok": False, "error": f"Dossier introuvable : {ext_path}"}, ensure_ascii=False))
        return 1

    # 1. Predict ID
    pred_id = run_predict_id(ext_path)
    print(f"[INSTALL] ID Chromium predict : {pred_id or 'indisponible'}")

    # 2. Profil actif (information)
    profile = run_active_profile()
    if profile.get("ok"):
        print(f"[INSTALL] Profil actif : {profile.get('profile_name')} — {profile.get('profile_path')}")
    else:
        print(f"[INSTALL] Profil actif : non determine ({profile.get('error')})")

    # 3. Verifier CDP
    if not ensure_cdp_port():
        print(json.dumps({"ok": False, "error": "Port CDP 9222 non joignable"}, ensure_ascii=False))
        return 1

    # 4. Armer le hook PS1 en arriere-plan (AVANT le clic CDP)
    ps_cmd = [
        "pwsh", "-NoProfile", "-ExecutionPolicy", "Bypass",
        "-WindowStyle", "Hidden",
        "-File", str(HOOK_SCRIPT),
        "-ExtensionPath", str(ext_path_obj.resolve()),
        "-TimeoutSec", str(timeout_sec),
    ]
    try:
        ps_proc = subprocess.Popen(ps_cmd, creationflags=subprocess.CREATE_NO_WINDOW)
    except Exception as exc:
        print(f"[ERREUR] Impossible de lancer le hook PS1 : {exc}")
        return 1
    print(f"[INSTALL] Hook PS1 arme (PID {ps_proc.pid}), attente dialogue…")

    # 5. CDP : ouvrir chrome://extensions, activer Mode Developpeur, clic #loadUnpacked
    if sync_playwright is None:
        print(json.dumps({"ok": False, "error": "playwright non installe"}, ensure_ascii=False))
        ps_proc.terminate()
        return 1

    p, browser, context = _connect_cdp()
    install_ok = False
    try:
        page = context.new_page()
        page.goto("chrome://extensions", wait_until="networkidle")
        page.wait_for_timeout(1500)

        # Activer le Mode Developpeur (toggle en haut a droite)
        dev_clicked = _click_by_text_or_id(page, [
            {"id": "developer-mode-toggle"},
            {"text": "mode developpeur"},
            {"text": "developer mode"},
            {"text": "mode d\u00e9veloppeur"},
        ])
        print(f"[INSTALL] Mode developpeur : {'active' if dev_clicked else 'toggle non trouve (peut-etre deja actif)'}")
        page.wait_for_timeout(1000)

        # Clic sur "Charger l'extension non empaquetée" (#loadUnpacked / texte)
        load_clicked = _click_by_text_or_id(page, [
            {"id": "load-unpacked"},
            {"id": "loadUnpacked"},
            {"text": "charger l'extension non empaquetee"},
            {"text": "charger lunextension non empaquetee"},
            {"text": "load unpacked"},
        ])
        print(f"[INSTALL] Clic #loadUnpacked : {'OK' if load_clicked else 'ECHEC'}")

        if not load_clicked:
            # Diagnostic : lister ce qui est trouve dans la toolbar
            diag = page.evaluate("""() => {
                const txt = document.body ? document.body.textContent : '';
                return { hasUnpacked: /(non empaquetee|unpacked)/i.test(txt), hasDev: /(developpeur|developer)/i.test(txt) };
            }""")
            print(f"[INSTALL] Diagnostic page : {diag}")

        page.wait_for_timeout(2000)
        page.close()

        # 6. Attendre que le hook PS1 ait rempli le dialogue (il tourne deja)
        ps_rc = ps_proc.wait(timeout=timeout_sec + 5)
        print(f"[INSTALL] Hook PS1 termine (rc={ps_rc})")
        install_ok = (ps_rc == 0)

    finally:
        _close_cdp(p, browser)
        if ps_proc.poll() is None:
            ps_proc.terminate()

    # 7. Verification : l'extension est-elle presente dans le runtime ?
    #    On cherche par nom "GEM-X" (l'algo d'ID deterministe est une aide,
    #    pas une preuve : l'ID reel peut differer selon la version de Chromium).
    ext_name = ext_path_obj.name
    install_ok = False
    found_ext = None
    if install_ok or True:  # verifier quoi qu'il arrive (le hook peut avoir reussi sans rc=0 fiable)
        print(f"[INSTALL] Verification de la presence de '{ext_name}' dans chrome://extensions…")
        deadline = time.time() + 30
        while time.time() < deadline:
            p2, browser2, context2 = _connect_cdp()
            try:
                page2 = context2.new_page()
                page2.goto("chrome://extensions", wait_until="networkidle")
                res = page2.evaluate("""(name) => {
                    const mgr = document.querySelector('extensions-manager');
                    const list = mgr?.shadowRoot?.querySelector('extensions-item-list');
                    const items = list?.shadowRoot?.querySelectorAll('extensions-item') || [];
                    const nLower = name.toLowerCase();
                    for (const it of items) {
                        const n = it.shadowRoot?.querySelector('#name')?.textContent?.trim().toLowerCase();
                        const enabled = it.shadowRoot?.querySelector('#enable-toggle')?.getAttribute('aria-pressed') === 'true';
                        const errors = !!it.shadowRoot?.querySelector('#errors-button');
                        if (n === nLower || n.includes(nLower)) {
                            return { id: it.id, name: n, enabled, hasErrors: errors };
                        }
                    }
                    return null;
                }""", ext_name)
                page2.close()
                if res:
                    found_ext = res
                    install_ok = True
                    print(f"[INSTALL] Extension trouvee : id={res['id']} enabled={res['enabled']} errors={res['hasErrors']}")
                    break
            finally:
                _close_cdp(p2, browser2)
            time.sleep(4)

    if found_ext:
        print(json.dumps({"ok": True, "extension": found_ext, "installed": True}, ensure_ascii=False))
        return 0
    print(json.dumps({"ok": install_ok, "extension_id": pred_id, "installed": False}, ensure_ascii=False))
    return 0 if install_ok else 1


def cmd_install_load_extension(ext_path: str):
    """
    Installation autonome SANS dialogue Windows.
    
    Redemarrage de Chromium avec le flag --load-extension (la seule voie 100%
    autonome sans controle clavier/souris, le dialogue IFileDialog etant
    injoignable depuis CDP).
    
    Deroulement :
      1. Arret du processus Chrome parent (port 9222)
      2. Relancement avec --load-extension + --profile-directory=Profile 2
      3. Attente du retour du port CDP 9222
      4. Verification de la presence de l'extension par nom
    """
    ext_path_obj = Path(ext_path)
    if not ext_path_obj.exists():
        print(json.dumps({"ok": False, "error": f"Dossier introuvable : {ext_path}"}, ensure_ascii=False))
        return 1

    ext_name = ext_path_obj.name
    chrome_exe = r"C:\Users\GG\AppData\Local\Chromium\Application\chrome.exe"
    user_data_dir = r"C:\Users\GG\AppData\Local\Chromium\User Data"

    if not Path(chrome_exe).exists():
        print(json.dumps({"ok": False, "error": f"Chrome introuvable : {chrome_exe}"}, ensure_ascii=False))
        return 1

    # 1. Nettoyage : arret de tout Chrome + suppression des verrous de profil
    #    (fichiers LOCK laisses par un kill brutal qui bloquent le redemarrage).
    #    Attendre que le processus soit VRAIMENT mort avant de supprimer les
    #    verrous, sinon Windows garde un handle ouvert.
    print("[LOAD-EXT] Arret de tous les processus Chrome…")
    subprocess.run(
        ["taskkill", "/F", "/IM", "chrome.exe"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        creationflags=subprocess.CREATE_NO_WINDOW,
    )
    # Attendre jusqu'a 40s que tous les processus chrome.exe soient disparus
    deadline = time.time() + 40
    chrome_gone = False
    while time.time() < deadline:
        chk = subprocess.run(
            ["tasklist", "/FI", "IMAGENAME eq chrome.exe"],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
        out = chk.stdout or ""
        if "chrome.exe" not in out:
            chrome_gone = True
            break
        time.sleep(1)
    if not chrome_gone:
        print("[WARN] Des processus chrome sont encore en cours après 40s.")

    # Supprimer les fichiers LOCK de Chromium (verrou de profil) - tous, recursif
    ud = Path(user_data_dir)
    lock_count = 0
    for lock in list(ud.rglob("LOCK")) + list(ud.rglob("*.lock")):
        try:
            lock.unlink()
            lock_count += 1
            print(f"[LOAD-EXT] Verrou supprime : {lock}")
        except Exception:
            pass
    if lock_count > 0:
        print(f"[LOAD-EXT] {lock_count} verrou(x) supprime(s).")

    # Stabilisation : laisser l'OS liberer totalement les handles
    time.sleep(20)

    # 2. Relancer Chrome avec --load-extension (pas de dialogue Windows)
    #    Flags anti-dialogue : --no-first-run, --disable-restore-session-state
    cmd = [
        chrome_exe,
        f'--user-data-dir="{user_data_dir}"',
        '--profile-directory=Profile 2',
        '--remote-debugging-port=9222',
        f'--load-extension="{ext_path_obj.resolve()}"',
        '--remote-allow-origins',
        '--disable-features=AutoDeElevate',
        '--no-first-run',
        '--disable-restore-session-state',
    ]
    print(f"[LOAD-EXT] Lancement de Chromium avec --load-extension={ext_path_obj.resolve()}")
    try:
        chrome_proc = subprocess.Popen(cmd)
        print(f"[LOAD-EXT] PID Chrome lancé : {chrome_proc.pid}")
        # Laisser Chrome demarrer (initialisation du profil, recréation des BDD)
        time.sleep(10)
        # Test immediat du port
        try:
            urllib.request.urlopen("http://127.0.0.1:9222/json", timeout=2)
            print("[LOAD-EXT] Port 9222 deja repondant.")
        except Exception:
            print("[LOAD-EXT] Port 9222 pas encore repondant (attente prolongee…).")
    except Exception as exc:
        print(json.dumps({"ok": False, "error": f"Echec lancement Chrome : {exc}"}, ensure_ascii=False))
        return 1

    # 3. Attendre que le port CDP 9222 reponde (mon Chrome relance)
    deadline = time.time() + 120
    port_up = False
    while time.time() < deadline:
        try:
            urllib.request.urlopen("http://127.0.0.1:9222/json", timeout=2)
            port_up = True
            break
        except Exception:
            time.sleep(1)
    if not port_up:
        print(json.dumps({"ok": False, "error": "Port CDP 9222 non revenu apres redemarrage"}, ensure_ascii=False))
        return 1
    print("[LOAD-EXT] Port CDP 9222 disponible.")

    # 4. Verification de la presence de l'extension par nom
    print(f"[LOAD-EXT] Verification de la presence de '{ext_name}' dans chrome://extensions…")
    deadline = time.time() + 30
    found_ext = None
    while time.time() < deadline:
        p2, browser2, context2 = _connect_cdp()
        try:
            page2 = context2.new_page()
            page2.goto("chrome://extensions", wait_until="networkidle")
            res = page2.evaluate("""(name) => {
                const mgr = document.querySelector('extensions-manager');
                const list = mgr?.shadowRoot?.querySelector('extensions-item-list');
                const items = list?.shadowRoot?.querySelectorAll('extensions-item') || [];
                const nLower = name.toLowerCase();
                for (const it of items) {
                    const n = it.shadowRoot?.querySelector('#name')?.textContent?.trim().toLowerCase();
                    const enabled = it.shadowRoot?.querySelector('#enable-toggle')?.getAttribute('aria-pressed') === 'true';
                    const errors = !!it.shadowRoot?.querySelector('#errors-button');
                    if (n === nLower || n.includes(nLower)) {
                        return { id: it.id, name: n, enabled, hasErrors: errors };
                    }
                }
                return null;
            }""", ext_name)
            page2.close()
            if res:
                found_ext = res
                print(f"[LOAD-EXT] Extension trouvee : id={res['id']} enabled={res['enabled']} errors={res['hasErrors']}")
                break
        finally:
            _close_cdp(p2, browser2)
        time.sleep(3)

    if found_ext:
        print(json.dumps({"ok": True, "extension": found_ext, "installed": True, "method": "load-extension"}, ensure_ascii=False))
        return 0
    print(json.dumps({"ok": False, "installed": False, "method": "load-extension"}, ensure_ascii=False))
    return 1


CCP_META_DB = Path(__file__).resolve().parent / "chromium_meta.json"


def cmd_extensions_add(slug: str, manifest_path: str, git_repo: str, version: str):
    """
    Met a jour la base de donnees relationnelle locale (chromium_meta.json)
    avec les metadonnees d'une extension Chromium.
    """
    manifest_file = Path(manifest_path)
    if not manifest_file.exists():
        print(json.dumps({"ok": False, "error": f"Manifest introuvable : {manifest_path}"}, ensure_ascii=False))
        return 1

    try:
        manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(json.dumps({"ok": False, "error": f"Manifest invalide : {e}"}, ensure_ascii=False))
        return 1

    # ID predictif (Cas A)
    pred_id = run_predict_id(str(manifest_file.parent))

    # Charger ou creer la base meta
    if CCP_META_DB.exists():
        try:
            meta = json.loads(CCP_META_DB.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            meta = {"extensions": {}}
    else:
        meta = {"extensions": {}}

    entry = {
        "slug": slug,
        "name": manifest.get("name", manifest_file.parent.name),
        "version": version or manifest.get("version", "unknown"),
        "description": manifest.get("description", ""),
        "manifest_version": manifest.get("manifest_version"),
        "manifest_path": str(manifest_file.resolve()),
        "git_repo": git_repo,
        "extension_dir": str(manifest_file.parent.resolve()),
        "predicted_id": pred_id,
        "actual_id": None,
        "status": "registered",
        "activated": False,
    }

    meta["extensions"][slug] = entry

    CCP_META_DB.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps({"ok": True, "slug": slug, "entry": entry, "meta_db": str(CCP_META_DB)}, ensure_ascii=False, indent=2))
    return 0


# ——————————————————————————————————————————————————————————————————————
# Point d'entree
# ——————————————————————————————————————————————————————————————————————

def main():
    parser = argparse.ArgumentParser(description="CCP CLI — Installation autonome d'extensions Chromium")
    sub = parser.add_subparsers(dest="action", required=True)

    p_pred = sub.add_parser("predict-id", help="Calcule l'ID Chromium deterministe d'un dossier")
    p_pred.add_argument("--path", required=True, help="Chemin du dossier d'extension")

    sub.add_parser("active-profile", help="Affiche le profil Chromium actif via CDP")

    p_inst = sub.add_parser("extensions", help="Gestion des extensions")
    p_inst.add_argument("cmd", nargs="?", choices=["install", "load-extension", "add"], help="Methode d'installation")
    p_inst.add_argument("--path", required=False, help="Chemin du dossier d'extension")
    p_inst.add_argument("--slug", required=False, help="Slug de l'extension (pour 'add')")
    p_inst.add_argument("--manifest-path", required=False, help="Chemin vers manifest.json (pour 'add')")
    p_inst.add_argument("--git-repo", required=False, help="Depot git source (pour 'add')")
    p_inst.add_argument("--version", required=False, help="Version de l'extension (pour 'add')")
    p_inst.add_argument("--timeout", type=int, default=30, help="Timeout dialogue Windows (secondes)")

    args = parser.parse_args()

    if args.action == "predict-id":
        ext_id = run_predict_id(args.path)
        if ext_id:
            print(ext_id)
            return 0
        return 1

    if args.action == "active-profile":
        profile = run_active_profile()
        if profile.get("ok"):
            print(json.dumps(profile, ensure_ascii=False, indent=2))
            return 0
        print(json.dumps(profile, ensure_ascii=False))
        return 1

    if args.action == "extensions":
        if args.cmd == "load-extension":
            if not args.path:
                print("[ERREUR] --path requis pour 'extensions load-extension'", file=sys.stderr)
                return 2
            return cmd_install_load_extension(args.path)
        if args.cmd == "install":
            if not args.path:
                print("[ERREUR] --path requis pour 'extensions install'", file=sys.stderr)
                return 2
            return cmd_install(args.path, args.timeout)
        if args.cmd == "add":
            if not args.slug:
                print("[ERREUR] --slug requis pour 'extensions add'", file=sys.stderr)
                return 2
            if not args.manifest_path:
                print("[ERREUR] --manifest-path requis pour 'extensions add'", file=sys.stderr)
                return 2
            if not args.git_repo:
                print("[ERREUR] --git-repo requis pour 'extensions add'", file=sys.stderr)
                return 2
            if not args.version:
                print("[ERREUR] --version requis pour 'extensions add'", file=sys.stderr)
                return 2
            return cmd_extensions_add(args.slug, args.manifest_path, args.git_repo, args.version)
        print("[ERREUR] Sous-commande inconnue : extensions <install|load-extension|add>", file=sys.stderr)
        return 2

    return 1


if __name__ == "__main__":
    sys.exit(main())
