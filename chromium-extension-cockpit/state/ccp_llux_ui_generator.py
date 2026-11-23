#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ccp_llux_ui_generator.py — Pont entre BIRDY/LLUX et le Cockpit UI du CCP.

Génère des composants UI MV3 (Web Components, popups, side panels) à partir des
concepts ontologiques de LLUX (via BIRDY/concept_design.py et ROOTX).

Intègre la couche sémantique de conception (LLUX) dans le dashboard VS Code du
Chromium Control Plane, permettant de prototyper des interfaces d'extensions
sans dépendre d'un outil cloud propriétaire (Google Stitch).

Usage :
    python ccp_llux_ui_generator.py design-concept --name "Mon Bouton" --type button
    python ccp_llux_ui_generator.py generate-panel --ext-id 1 --name "Side Panel"
"""

import argparse
import json
import sqlite3
import sys
import uuid
from pathlib import Path
from typing import Any

# Ajouter le chemin vers BIRDY pour importer concept_design
BIRDY_SRC = Path(__file__).resolve().parents[4] / "L2-PLATFORM" / "BIRDY" / "src"
if str(BIRDY_SRC) not in sys.path:
    sys.path.insert(0, str(BIRDY_SRC))

try:
    from concept_design import ConceptDesign, ConceptDesignConfig
except ImportError:
    ConceptDesign = None
    ConceptDesignConfig = None

try:
    from rootx_client import RootxClient, RootxClientConfig
except ImportError:
    RootxClient = None
    RootxClientConfig = None

DB_PATH = Path(__file__).resolve().parent / "chromium_meta.db"

# Templates de composants UI MV3 (Web Components, compatibles CSP strict)
UI_COMPONENT_TEMPLATES = {
    "button": """<button class="gerivdb-btn gerivdb-btn--{variant}" id="{id}" {aria} onclick="{handler}">{label}</button>
<style>
  .gerivdb-btn {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 8px 16px;
    border-radius: 6px;
    font-weight: 600;
    font-size: 0.875rem;
    border: none;
    cursor: pointer;
    transition: all 0.15s;
  }}
  .gerivdb-btn--primary {{ background: #3b82f6; color: #fff; }}
  .gerivdb-btn--primary:hover {{ background: #2563eb; }}
  .gerivdb-btn--danger {{ background: #ef4444; color: #fff; }}
  .gerivdb-btn--danger:hover {{ background: #dc2626; }}
  .gerivdb-btn:focus-visible {{ outline: 2px solid #3b82f6; outline-offset: 2px; }}
</style>""",
    "card": """<div class="gerivdb-card" id="{id}" {aria}>
  <div class="gerivdb-card__header">{title}</div>
  <div class="gerivdb-card__body">{content}</div>
</div>
<style>
  .gerivdb-card {{
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 16px;
    color: #f8fafc;
  }}
  .gerivdb-card__header {{
    font-weight: 700;
    font-size: 1rem;
    margin-bottom: 12px;
    color: #3b82f6;
  }}
  .gerivdb-card__body {{ color: #cbd5e1; }}
</style>""",
    "sidepanel": """<div class="gerivdb-sidepanel" id="{id}" {aria}>
  <div class="gerivdb-sidepanel__header">
    <span class="gerivdb-sidepanel__title">{title}</span>
    <button class="gerivdb-sidepanel__close" onclick="{close_handler}">&times;</button>
  </div>
  <div class="gerivdb-sidepanel__body">{content}</div>
</div>
<style>
  .gerivdb-sidepanel {{
    position: fixed;
    top: 0; right: 0;
    width: 320px; height: 100vh;
    background: #0f172a;
    border-left: 1px solid #334155;
    color: #f8fafc;
    display: flex; flex-direction: column;
    z-index: 9999;
  }}
  .gerivdb-sidepanel__header {{
    padding: 12px 16px;
    display: flex; align-items: center; justify-content: space-between;
    border-bottom: 1px solid #334155;
  }}
  .gerivdb-sidepanel__title {{ font-weight: 600; color: #3b82f6; }}
  .gerivdb-sidepanel__close {{ background: none; border: none; color: #94a3b8; font-size: 1.5rem; cursor: pointer; }}
  .gerivdb-sidepanel__body {{ padding: 16px; overflow-y: auto; color: #cbd5e1; }}
</style>""",
}


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.row_factory = sqlite3.Row
    return conn


def resolve_ext_name(conn: sqlite3.Connection, ext_id: int) -> str:
    row = conn.execute("SELECT slug FROM extensions WHERE id = ?", (ext_id,)).fetchone()
    return row["slug"] if row else f"ext-{ext_id}"


def design_concept_ui(
    name: str,
    component_type: str,
    ext_slug: str | None = None,
    rootx_endpoint: str = "http://localhost:8030",
) -> dict[str, Any]:
    """
    Concepte un composant UI via LLUX/ROOTX puis génère le code HTML/CSS/JS MV3.
    Retourne un dict avec les métadonnées, le code généré et le concept_id LLUX.
    """
    concept_id = f"ui_{uuid.uuid4().hex[:8]}"
    result: dict[str, Any] = {
        "concept_id": concept_id,
        "name": name,
        "component_type": component_type,
        "ext_slug": ext_slug,
        "llux_designed": False,
        "code": "",
        "errors": [],
    }

    # 1. Conception ontologique via LLUX/ROOTX (si disponible)
    if ConceptDesign is not None:
        cd = ConceptDesign(ConceptDesignConfig(rootx_endpoint=rootx_endpoint))
        health = cd.health()
        if health.get("status") == "ok":
            design_result = cd.design_concept(
                {
                    "action": "design_ui_component",
                    "name": name,
                    "component_type": component_type,
                    "ext_slug": ext_slug,
                    "llux_source": "BIRDY/concept_design.py",
                },
            )
            result["llux_designed"] = design_result.get("designed", False)
            result["llux_concept_id"] = design_result.get("concept_id", "")
            if design_result.get("errors"):
                result["errors"].extend(design_result["errors"])
        else:
            result["errors"].append(f"LLUX/ROOTX indisponible : {health.get('rootx_error', 'inconnu')}")
    else:
        result["errors"].append("Module concept_design de BIRDY introuvable")

    # 2. Génération du code UI MV3
    template = UI_COMPONENT_TEMPLATES.get(component_type, UI_COMPONENT_TEMPLATES["card"])
    aria = f'aria-label="{name}"' if name else ""
    handler = f"on{name.replace(' ', '')}Click()" if name else "console.log('Component clicked')"
    label = name
    variant = "primary"
    title = name
    content = f"<p>Contenu généré pour {name}</p>"
    close_handler = "this.parentElement.remove()"

    if component_type == "button":
        code = template.format(id=concept_id, aria=aria, handler=handler, variant=variant, label=label)
    elif component_type == "card":
        code = template.format(id=concept_id, aria=aria, title=title, content=content)
    elif component_type == "sidepanel":
        code = template.format(id=concept_id, aria=aria, title=title, content=content, close_handler=close_handler)
    else:
        code = template.format(id=concept_id, aria=aria, title=title, content=content)

    result["code"] = code
    result["file_name"] = f"{concept_id}.html"
    return result


def save_concept_to_db(conn: sqlite3.Connection, ext_id: int | None, design: dict[str, Any]) -> int:
    """Enregistre le concept UI dans la base (dans une table dédiée ou telemetry_events)."""
    # On stocke dans telemetry_events comme événement de conception UI
    conn.execute(
        """INSERT INTO telemetry_events
           (extension_id, source, level, message, stack_trace)
           VALUES (?, ?, ?, ?, ?)""",
        (
            ext_id,
            "llux-ui-generator",
            "info",
            f"UI concept designed: {design['name']} ({design['component_type']})",
            json.dumps({"concept_id": design["concept_id"], "component_type": design["component_type"], "file_name": design.get("file_name", "")}, ensure_ascii=False),
        ),
    )
    conn.commit()
    row = conn.execute("SELECT last_insert_rowid() AS id").fetchone()
    return row["id"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Générateur UI LLUX pour le CCP")
    sub = parser.add_subparsers(dest="command", required=True)

    p_design = sub.add_parser("design-concept", help="Concepte un composant UI via LLUX")
    p_design.add_argument("--name", required=True, help="Nom du composant")
    p_design.add_argument("--type", required=True, choices=["button", "card", "sidepanel"], help="Type de composant")
    p_design.add_argument("--ext-id", type=int, default=None, help="ID de l'extension cible")
    p_design.add_argument("--rootx-endpoint", default="http://localhost:8030", help="Endpoint ROOTX")
    p_design.add_argument("--output", default=None, help="Fichier de sortie HTML (optionnel)")
    p_design.set_defaults(func=cmd_design_concept)

    p_list = sub.add_parser("list-components", help="Liste les concepts UI générés (depuis la télémétrie)")
    p_list.add_argument("--limit", type=int, default=20)
    p_list.set_defaults(func=cmd_list_components)

    args = parser.parse_args()
    args.func(args)


def cmd_design_concept(args: argparse.Namespace) -> None:
    design = design_concept_ui(
        name=args.name,
        component_type=args.type,
        ext_slug=None,
        rootx_endpoint=args.rootx_endpoint,
    )

    # Si un ext-id est donné, lier le concept à l'extension
    ext_id = args.ext_id
    if ext_id:
        conn = get_db()
        try:
            design["ext_slug"] = resolve_ext_name(conn, ext_id)
            save_concept_to_db(conn, ext_id, design)
        finally:
            conn.close()

    print(json.dumps(design, ensure_ascii=False, indent=2))

    # Écriture optionnelle dans un fichier
    if args.output:
        Path(args.output).write_text(design["code"], encoding="utf-8")
        print(f"\n[INFO] Code écrit dans : {args.output}")


def cmd_list_components(args: argparse.Namespace) -> None:
    conn = get_db()
    try:
        rows = conn.execute(
            """SELECT t.id, t.timestamp, e.slug AS extension_slug, t.message, t.stack_trace
               FROM telemetry_events t
               LEFT JOIN extensions e ON e.id = t.extension_id
               WHERE t.source = 'llux-ui-generator'
               ORDER BY t.id DESC
               LIMIT ?""",
            (args.limit,),
        ).fetchall()
        if not rows:
            print("(aucun concept UI généré)")
            return
        print(f"{'ID':<4} {'Heure':<20} {'Extension':<20} {'Concept'}")
        print("-" * 80)
        for r in rows:
            msg = r["message"] or ""
            print(f"{r['id']:<4} {r['timestamp']:<20} {(r['extension_slug'] or '-'):<20} {msg[:60]}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
