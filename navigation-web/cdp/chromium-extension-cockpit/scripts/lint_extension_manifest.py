#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lint_extension_manifest.py — Porte de contrôle statique (pre-commit gate)
pour les manifests d'extensions Chromium MV3.

Vérifications :
1. 100% des fichiers déclarés (service_worker, content_scripts,
   web_accessible_resources, side_panel, action.default_popup,
   options_ui.page, declarative_net_request.rule_resources[].path)
   existent physiquement sur le disque.
2. Aucun ID Chrome Web Store amont codé en dur dans
   net_request.json (initiatorDomains) → éradication du bug 403.
3. Aucune directive dépréciée (focus-without-user-activation) dans
   les fichiers HTML de l'extension.

Usage :
    python lint_extension_manifest.py <chemin/manifest.json>
    # ou depuis la racine du dépôt d'extension :
    python lint_extension_manifest.py

Code de retour : 0 = conforme, 1 = rejet (commit bloqué).
"""

import json
import re
import sys
from pathlib import Path

ERRORS = []


def error(msg):
    ERRORS.append(msg)
    print(f"[LINT-ERROR] {msg}")


def lint_manifest(manifest_path: Path):
    """Vérifie l'existence physique de tous les fichiers déclarés dans le manifest."""
    if not manifest_path.exists():
        error(f"manifest.json introuvable : {manifest_path}")
        return

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        error(f"manifest.json invalide (JSON) : {e}")
        return

    root = manifest_path.parent

    def check_file(rel_path: str, ctx: str):
        if not rel_path:
            return
        full = root / rel_path
        if not full.exists():
            error(f"{ctx} : fichier manquant '{rel_path}'")

    # background.service_worker
    bg = manifest.get("background", {})
    if isinstance(bg, dict):
        sw = bg.get("service_worker")
        if sw:
            check_file(sw, "background.service_worker")

    # side_panel.default_path
    sp = manifest.get("side_panel", {})
    if isinstance(sp, dict):
        pp = sp.get("default_path")
        if pp:
            check_file(pp, "side_panel.default_path")

    # action.default_popup
    action = manifest.get("action", {})
    if isinstance(action, dict):
        dp = action.get("default_popup")
        if dp:
            check_file(dp, "action.default_popup")

    # options_ui.page
    opts = manifest.get("options_ui", {})
    if isinstance(opts, dict):
        op = opts.get("page")
        if op:
            check_file(op, "options_ui.page")

    # content_scripts[].js[] et [].css[]
    cs_list = manifest.get("content_scripts", [])
    if isinstance(cs_list, list):
        for i, cs in enumerate(cs_list):
            if not isinstance(cs, dict):
                continue
            for js in cs.get("js", []):
                check_file(js, f"content_scripts[{i}].js")
            for css in cs.get("css", []):
                check_file(css, f"content_scripts[{i}].css")

    # web_accessible_resources[].resources[]
    war_list = manifest.get("web_accessible_resources", [])
    if isinstance(war_list, list):
        for i, war in enumerate(war_list):
            if not isinstance(war, dict):
                continue
            for res in war.get("resources", []):
                check_file(res, f"web_accessible_resources[{i}].resources")

    # declarative_net_request.rule_resources[].path
    dnr = manifest.get("declarative_net_request", {})
    if isinstance(dnr, dict):
        rr_list = dnr.get("rule_resources", [])
        if isinstance(rr_list, list):
            for i, rr in enumerate(rr_list):
                if not isinstance(rr, dict):
                    continue
                rp = rr.get("path")
                if rp:
                    check_file(rp, f"declarative_net_request.rule_resources[{i}].path")


def lint_dnr_rules(root: Path):
    """Vérifie qu'aucun ID CWS amont n'est en dur dans net_request.json (initiatorDomains)."""
    dnr_path = root / "net_request.json"
    if not dnr_path.exists():
        return

    try:
        dnr = json.loads(dnr_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        error(f"net_request.json invalide (JSON) : {e}")
        return

    if not isinstance(dnr, list):
        return

    # Pattern ID CWS : 32 caractères alphanumériques (chrome-extension ID)
    cws_id_re = re.compile(r"^[a-z]{32}$")

    for i, rule in enumerate(dnr):
        if not isinstance(rule, dict):
            continue
        condition = rule.get("condition", {})
        if not isinstance(condition, dict):
            continue
        initiator_domains = condition.get("initiatorDomains", [])
        if not isinstance(initiator_domains, list):
            continue
        for domain in initiator_domains:
            if not isinstance(domain, str):
                continue
            # Un ID CWS est une chaîne de 32 caractères minuscules alphanumériques
            if cws_id_re.match(domain):
                error(
                    f"net_request.json règle[{i}] : initiatorDomains contient "
                    f"un ID Chrome Web Store amont '{domain}' (doit être supprimé)"
                )


def lint_deprecated_directives(root: Path):
    """Vérifie l'absence de focus-without-user-activation dans les fichiers HTML."""
    html_files = list(root.rglob("*.html"))
    for html_file in html_files:
        try:
            content = html_file.read_text(encoding="utf-8")
        except Exception as e:
            error(f"Impossible de lire {html_file} : {e}")
            continue
        if re.search(
            r'allow\s*=\s*["\'][^"\']*focus-without-user-activation',
            content,
            re.IGNORECASE,
        ):
            rel = html_file.relative_to(root)
            error(
                f"Directive dépréciée 'focus-without-user-activation' "
                f"active dans l'attribut allow de {rel}"
            )


def main():
    # Déterminer le chemin du manifest
    if len(sys.argv) > 1:
        manifest_path = Path(sys.argv[1]).resolve()
    else:
        manifest_path = Path("manifest.json").resolve()

    if not manifest_path.is_file():
        print(f"[LINT-ERROR] Fichier non trouvé : {manifest_path}", file=sys.stderr)
        sys.exit(1)

    root = manifest_path.parent

    lint_manifest(manifest_path)
    lint_dnr_rules(root)
    lint_deprecated_directives(root)

    if ERRORS:
        print(f"\n[LINT-FAIL] {len(ERRORS)} erreur(s) détectée(s). Commit bloqué.", file=sys.stderr)
        sys.exit(1)

    print("[LINT-OK] Manifest MV3 conforme — aucun fichier fantôme, aucun ID CWS amont, aucune directive dépréciée.")
    sys.exit(0)


if __name__ == "__main__":
    main()
