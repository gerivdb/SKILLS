#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ccp_ui_server.py — Serveur HTTP de bord de contrôle pour le Chromium Control Plane.

Expose une API REST sur les données de chromium_meta.db et sert le dashboard
HTML/JS du cockpit VS Code.

Usage :
    python ccp_ui_server.py [--port 8796] [--db-path chemin/db]

Endpoints :
    GET /api/health        -> statut du serveur
    GET /api/extensions    -> liste des extensions (slug, version, statut, erreurs non résolues)
    GET /api/daemon-bridges -> liste des ponts de daemons locaux
    GET /api/telemetry     -> événements non résolus (limit paramètre optionnel)
    GET /                  -> sert le dashboard HTML
"""

import argparse
import json
import sqlite3
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

DEFAULT_DB = Path(__file__).resolve().parent / "chromium_meta.db"
DEFAULT_PORT = 8796


def get_db(db_path: Path = DEFAULT_DB) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.row_factory = sqlite3.Row
    return conn


class CCPHandler(BaseHTTPRequestHandler):
    """Handler HTTP pour le dashboard du CCP."""

    db_path: Path = DEFAULT_DB

    def _send_json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, status: int, html: str) -> None:
        body = html.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        path = self.path.split("?")[0]

        if path == "/api/health":
            try:
                conn = get_db(self.db_path)
                conn.execute("SELECT 1").fetchone()
                conn.close()
                self._send_json(200, {"status": "ok", "db": str(self.db_path)})
            except Exception as exc:
                self._send_json(500, {"status": "error", "error": str(exc)})
            return

        if path == "/api/extensions":
            try:
                conn = get_db(self.db_path)
                rows = conn.execute(
                    """SELECT e.id, e.slug, e.version, e.status, e.auto_reload,
                              e.git_repo, e.git_commit,
                              COUNT(t.id) AS error_count,
                              SUM(CASE WHEN t.level='error' AND t.resolved=0 THEN 1 ELSE 0 END) AS unresolved_errors
                       FROM extensions e
                       LEFT JOIN telemetry_events t ON t.extension_id = e.id
                       GROUP BY e.id
                       ORDER BY e.slug"""
                ).fetchall()
                extensions = []
                for r in rows:
                    extensions.append({
                        "id": r["id"],
                        "slug": r["slug"],
                        "version": r["version"] or "?",
                        "status": r["status"] or "disabled",
                        "auto_reload": bool(r["auto_reload"]),
                        "git_repo": r["git_repo"],
                        "git_commit": r["git_commit"],
                        "error_count": r["error_count"] or 0,
                        "unresolved_errors": r["unresolved_errors"] or 0,
                        "healthy": (r["status"] == "active") and (r["unresolved_errors"] or 0) == 0,
                    })
                conn.close()
                self._send_json(200, {"ok": True, "extensions": extensions})
            except Exception as exc:
                self._send_json(500, {"ok": False, "error": str(exc)})
            return

        if path == "/api/daemon-bridges":
            try:
                conn = get_db(self.db_path)
                rows = conn.execute(
                    """SELECT d.id, e.slug AS extension_slug, d.port, d.protocol,
                              d.expected_status, d.fail_policy, d.description
                       FROM daemon_bridges d
                       LEFT JOIN extensions e ON e.id = d.extension_id
                       ORDER BY d.port"""
                ).fetchall()
                bridges = []
                for r in rows:
                    bridges.append({
                        "id": r["id"],
                        "extension_slug": r["extension_slug"],
                        "port": r["port"],
                        "protocol": r["protocol"],
                        "expected_status": r["expected_status"],
                        "fail_policy": r["fail_policy"],
                        "description": r["description"],
                    })
                conn.close()
                self._send_json(200, {"ok": True, "bridges": bridges})
            except Exception as exc:
                self._send_json(500, {"ok": False, "error": str(exc)})
            return

        if path == "/api/telemetry":
            try:
                limit = int(self.headers.get("Range", "50").split("-")[-1] or 50)
            except ValueError:
                limit = 50
            try:
                conn = get_db(self.db_path)
                rows = conn.execute(
                    """SELECT t.id, t.timestamp, e.slug AS extension_slug, t.source,
                              t.level, t.message, t.resolved
                       FROM telemetry_events t
                       LEFT JOIN extensions e ON e.id = t.extension_id
                       WHERE t.resolved = 0 AND t.level IN ('error', 'warning')
                       ORDER BY t.id DESC
                       LIMIT ?""",
                    (limit,),
                ).fetchall()
                events = []
                for r in rows:
                    events.append({
                        "id": r["id"],
                        "timestamp": r["timestamp"],
                        "extension_slug": r["extension_slug"],
                        "source": r["source"],
                        "level": r["level"],
                        "message": r["message"],
                        "resolved": bool(r["resolved"]),
                    })
                conn.close()
                self._send_json(200, {"ok": True, "events": events})
            except Exception as exc:
                self._send_json(500, {"ok": False, "error": str(exc)})
            return

        if path == "/api/llux/ui-concepts":
            self._handle_llux_ui_concepts_list()
            return

        if path == "/" or path == "/dashboard":
            self._serve_dashboard()
            return

        self._send_json(404, {"ok": False, "error": "not_found"})

    def do_POST(self) -> None:
        path = self.path.split("?")[0]
        from urllib.parse import parse_qs, urlparse
        parsed = urlparse(self.path)
        qs = parse_qs(parsed.query)
        slug = qs.get("slug", [None])[0]

        if path == "/api/reload":
            self._handle_reload(slug)
            return
        if path == "/api/clear-errors":
            self._handle_clear_errors(slug)
            return
        if path == "/api/llux/ui-concepts":
            self._handle_llux_ui_concepts()
            return

        self._send_json(404, {"ok": False, "error": "not_found"})

    def _handle_reload(self, slug: str) -> None:
        if not slug:
            self._send_json(400, {"ok": False, "error": "missing slug"})
            return
        try:
            import subprocess
            cockpit = Path(__file__).resolve().parent / "chromium_cdp_cockpit.py"
            res = subprocess.run(
                [sys.executable, str(cockpit), "reload", "--id", slug],
                capture_output=True, text=True, timeout=30,
            )
            if res.returncode == 0:
                self._send_json(200, {"ok": True, "message": f"Extension {slug} rechargée"})
            else:
                self._send_json(200, {"ok": False, "error": res.stderr or res.stdout})
        except Exception as exc:
            self._send_json(500, {"ok": False, "error": str(exc)})

    def _handle_clear_errors(self, slug: str) -> None:
        if not slug:
            self._send_json(400, {"ok": False, "error": "missing slug"})
            return
        try:
            import subprocess
            cockpit = Path(__file__).resolve().parent / "chromium_cdp_cockpit.py"
            res = subprocess.run(
                [sys.executable, str(cockpit), "clear-errors", "--id", slug],
                capture_output=True, text=True, timeout=30,
            )
            if res.returncode == 0:
                self._send_json(200, {"ok": True, "message": f"Erreurs purgées pour {slug}"})
            else:
                self._send_json(200, {"ok": False, "error": res.stderr or res.stdout})
        except Exception as exc:
            self._send_json(500, {"ok": False, "error": str(exc)})

    def _handle_llux_ui_concepts_list(self) -> None:
        """Gère les requêtes GET vers /api/llux/ui-concepts (liste des concepts UI)."""
        try:
            conn = get_db(self.db_path)
            rows = conn.execute(
                """SELECT t.id, t.timestamp, e.slug AS extension_slug, t.message,
                          t.stack_trace
                   FROM telemetry_events t
                   LEFT JOIN extensions e ON e.id = t.extension_id
                   WHERE t.source = 'llux-ui-generator'
                   ORDER BY t.id DESC
                   LIMIT 50"""
            ).fetchall()
            concepts = []
            for r in rows:
                concepts.append({
                    "id": r["id"],
                    "timestamp": r["timestamp"],
                    "extension_slug": r["extension_slug"],
                    "message": r["message"],
                    "stack_trace": r["stack_trace"],
                })
            conn.close()
            self._send_json(200, {"ok": True, "concepts": concepts})
        except Exception as exc:
            self._send_json(500, {"ok": False, "error": str(exc)})

    def _handle_llux_ui_concepts(self) -> None:
        """Gère les requêtes POST vers /api/llux/ui-concepts (création de concept UI)."""
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length) if content_length else b"{}"
            payload = json.loads(body.decode("utf-8")) if body else {}
        except Exception:
            payload = {}

        name = payload.get("name", "Nouveau Composant")
        component_type = payload.get("type", "card")
        ext_id = payload.get("ext_id")

        try:
            sys.path.insert(0, str(Path(__file__).resolve().parent))
            from ccp_llux_ui_generator import design_concept_ui, get_db, save_concept_to_db, resolve_ext_name

            design = design_concept_ui(
                name=name,
                component_type=component_type,
                ext_slug=None,
                rootx_endpoint="http://localhost:8030",
            )

            # Lier à l'extension si un ID est fourni
            if ext_id:
                conn = get_db()
                try:
                    design["ext_slug"] = resolve_ext_name(conn, ext_id)
                    save_concept_to_db(conn, ext_id, design)
                finally:
                    conn.close()

            self._send_json(200, {"ok": True, "concept": design})
        except Exception as exc:
            self._send_json(500, {"ok": False, "error": str(exc)})

    def _serve_dashboard(self) -> None:
        ui_dir = Path(__file__).resolve().parent / "ui"
        dashboard = ui_dir / "ccp_dashboard.html"
        if not dashboard.exists():
            self._send_json(404, {"ok": False, "error": "dashboard_not_found"})
            return
        html = dashboard.read_text(encoding="utf-8")
        self._send_html(200, html)

    def log_message(self, format: str, *args) -> None:  # noqa: A002
        # Silencieux par défaut pour ne pas polluer le terminal
        pass


def main() -> None:
    parser = argparse.ArgumentParser(description="Serveur HTTP du CCP UI Dashboard")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="Port d'écoute HTTP")
    parser.add_argument("--db-path", type=str, default=str(DEFAULT_DB), help="Chemin vers chromium_meta.db")
    args = parser.parse_args()

    CCPHandler.db_path = Path(args.db_path)
    if not CCPHandler.db_path.exists():
        print(f"[ERREUR] Base CCP introuvable : {CCPHandler.db_path}")
        print("Exécutez d'abord : python state/init_db.py --reset")
        sys.exit(1)

    server = HTTPServer(("127.0.0.1", args.port), CCPHandler)
    print(f"[SUCCÈS] CCP UI Dashboard sur http://127.0.0.1:{args.port}/")
    print(f"[INFO]   Base de données : {CCPHandler.db_path}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[INFO] Arrêt du serveur CCP UI.")
        server.server_close()


if __name__ == "__main__":
    main()
