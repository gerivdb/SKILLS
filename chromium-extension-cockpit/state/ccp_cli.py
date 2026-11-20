#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ccp_cli.py — Interface CLI du Chromium Control Plane (CCP).

Permet de gérer la base relationnelle unifiée chromium_meta.db :
- extensions   : CRUD des extensions (slug, version, statut, commit git...)
- daemon-bridges : CRUD des dépendances vers des daemons locaux
- telemetry    : lecture des événements CDP (erreurs, avertissements)
- snapshots    : gestion des instantanés d'état chrome.storage.local

Usage :
    python ccp_cli.py extensions add --slug sidekeep-x --manifest-path ... --git-repo ENV3-repo
    python ccp_cli.py extensions list
    python ccp_cli.py daemon-bridges add --ext-id 1 --port 8810 --protocol ws
    python ccp_cli.py telemetry list --ext-id 1 --level error --limit 20
"""

import argparse
import json
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "chromium_meta.db"


def _connect() -> sqlite3.Connection:
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Base CCP introuvable : {DB_PATH}. Exécutez d'abord init_db.py")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ---------------------------------------------------------------------------
# extensions
# ---------------------------------------------------------------------------
def ext_add(args: argparse.Namespace) -> None:
    conn = _connect()
    try:
        conn.execute(
            """INSERT INTO extensions
               (slug, manifest_path, git_repo, git_commit, version, is_unpacked, status, auto_reload)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                args.slug,
                args.manifest_path,
                args.git_repo,
                args.git_commit,
                args.version,
                1 if args.unpacked else 0,
                args.status,
                1 if args.auto_reload else 0,
            ),
        )
        conn.commit()
        print(f"[SUCCÈS] Extension '{args.slug}' ajoutée.")
    except sqlite3.IntegrityError as exc:
        print(f"[ÉCHEC] Slug déjà existant : {args.slug} ({exc})")
    finally:
        conn.close()


def ext_list(args: argparse.Namespace) -> None:
    conn = _connect()
    try:
        rows = conn.execute(
            """SELECT id, slug, version, status, auto_reload, git_commit
               FROM extensions ORDER BY slug"""
        ).fetchall()
        if not rows:
            print("(aucune extension enregistrée)")
            return
        print(f"{'ID':<4} {'Slug':<20} {'Version':<10} {'Status':<10} {'AutoReload':<10} {'Commit'}")
        print("-" * 70)
        for r in rows:
            print(
                f"{r['id']:<4} {r['slug']:<20} {r['version']:<10} "
                f"{r['status']:<10} {('Oui' if r['auto_reload'] else 'Non'):<10} "
                f"{r['git_commit'] or '-'}"
            )
    finally:
        conn.close()


def ext_rm(args: argparse.Namespace) -> None:
    conn = _connect()
    try:
        cur = conn.execute("DELETE FROM extensions WHERE id = ?", (args.ext_id,))
        if cur.rowcount == 0:
            print(f"[ÉCHEC] Aucune extension avec l'ID {args.ext_id}")
        else:
            conn.commit()
            print(f"[SUCCÈS] Extension ID {args.ext_id} supprimée.")
    finally:
        conn.close()


def ext_set_status(args: argparse.Namespace) -> None:
    conn = _connect()
    try:
        cur = conn.execute(
            "UPDATE extensions SET status = ?, updated_at = strftime('%Y-%m-%dT%H:%M:%SZ','now') WHERE id = ?",
            (args.status, args.ext_id),
        )
        if cur.rowcount == 0:
            print(f"[ÉCHEC] Aucune extension avec l'ID {args.ext_id}")
        else:
            conn.commit()
            print(f"[SUCCÈS] Extension ID {args.ext_id} passée en statut '{args.status}'.")
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# daemon-bridges
# ---------------------------------------------------------------------------
def bridge_add(args: argparse.Namespace) -> None:
    conn = _connect()
    try:
        conn.execute(
            """INSERT INTO daemon_bridges
               (extension_id, port, protocol, expected_status, fail_policy, description)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                args.ext_id,
                args.port,
                args.protocol,
                args.expected_status,
                args.fail_policy,
                args.description,
            ),
        )
        conn.commit()
        print(f"[SUCCÈS] Daemon bridge ajouté (port {args.port}, ext ID {args.ext_id}).")
    except sqlite3.IntegrityError as exc:
        print(f"[ÉCHEC] {exc}")
    finally:
        conn.close()


def bridge_list(args: argparse.Namespace) -> None:
    conn = _connect()
    try:
        rows = conn.execute(
            """SELECT d.id, e.slug, d.port, d.protocol, d.fail_policy, d.description
               FROM daemon_bridges d
               JOIN extensions e ON e.id = d.extension_id
               ORDER BY d.port"""
        ).fetchall()
        if not rows:
            print("(aucun daemon bridge enregistré)")
            return
        print(f"{'ID':<4} {'Extension':<20} {'Port':<6} {'Proto':<6} {'FailPolicy':<12} {'Description'}")
        print("-" * 80)
        for r in rows:
            print(
                f"{r['id']:<4} {r['slug']:<20} {r['port']:<6} {r['protocol']:<6} "
                f"{r['fail_policy']:<12} {r['description'] or '-'}"
            )
    finally:
        conn.close()


def bridge_rm(args: argparse.Namespace) -> None:
    conn = _connect()
    try:
        cur = conn.execute("DELETE FROM daemon_bridges WHERE id = ?", (args.bridge_id,))
        if cur.rowcount == 0:
            print(f"[ÉCHEC] Aucun bridge avec l'ID {args.bridge_id}")
        else:
            conn.commit()
            print(f"[SUCCÈS] Bridge ID {args.bridge_id} supprimé.")
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# telemetry
# ---------------------------------------------------------------------------
def telemetry_add(args: argparse.Namespace) -> None:
    conn = _connect()
    try:
        conn.execute(
            """INSERT INTO telemetry_events
               (extension_id, source, level, message, stack_trace)
               VALUES (?, ?, ?, ?, ?)""",
            (
                args.ext_id,
                args.source,
                args.level,
                args.message,
                args.stack_trace,
            ),
        )
        conn.commit()
        print("[SUCCÈS] Événement de télémétrie enregistré.")
    except sqlite3.IntegrityError as exc:
        print(f"[ÉCHEC] {exc}")
    finally:
        conn.close()


def telemetry_list(args: argparse.Namespace) -> None:
    conn = _connect()
    try:
        query = """SELECT t.id, t.timestamp, e.slug, t.source, t.level, t.message
                   FROM telemetry_events t
                   LEFT JOIN extensions e ON e.id = t.extension_id
                   WHERE 1=1"""
        params = []
        if args.ext_id is not None:
            query += " AND t.extension_id = ?"
            params.append(args.ext_id)
        if args.level:
            query += " AND t.level = ?"
            params.append(args.level)
        if args.unresolved:
            query += " AND t.resolved = 0"
        query += " ORDER BY t.timestamp DESC LIMIT ?"
        params.append(args.limit)

        rows = conn.execute(query, params).fetchall()
        if not rows:
            print("(aucun événement)")
            return
        print(f"{'ID':<4} {'Timestamp':<20} {'Ext':<16} {'Source':<10} {'Level':<8} {'Message'}")
        print("-" * 100)
        for r in rows:
            print(
                f"{r['id']:<4} {r['timestamp']:<20} {(r['slug'] or '-'):<16} "
                f"{r['source']:<10} {r['level']:<8} {r['message'][:60]}"
            )
    finally:
        conn.close()


def telemetry_resolve(args: argparse.Namespace) -> None:
    conn = _connect()
    try:
        cur = conn.execute(
            "UPDATE telemetry_events SET resolved = 1 WHERE id = ?", (args.event_id,)
        )
        if cur.rowcount == 0:
            print(f"[ÉCHEC] Aucun événement avec l'ID {args.event_id}")
        else:
            conn.commit()
            print(f"[SUCCÈS] Événement ID {args.event_id} marqué résolu.")
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# snapshots
# ---------------------------------------------------------------------------
def snapshot_add(args: argparse.Namespace) -> None:
    conn = _connect()
    try:
        storage_json = Path(args.storage_file).read_text(encoding="utf-8")
        conn.execute(
            """INSERT INTO snapshots (extension_id, label, storage_json)
               VALUES (?, ?, ?)""",
            (args.ext_id, args.label, storage_json),
        )
        conn.commit()
        print("[SUCCÈS] Snapshot enregistré.")
    except FileNotFoundError:
        print(f"[ÉCHEC] Fichier de stockage introuvable : {args.storage_file}")
    except sqlite3.IntegrityError as exc:
        print(f"[ÉCHEC] {exc}")
    finally:
        conn.close()


def snapshot_list(args: argparse.Namespace) -> None:
    conn = _connect()
    try:
        rows = conn.execute(
            """SELECT s.id, e.slug, s.timestamp, s.label
               FROM snapshots s
               JOIN extensions e ON e.id = s.extension_id
               ORDER BY s.timestamp DESC"""
        ).fetchall()
        if not rows:
            print("(aucun snapshot enregistré)")
            return
        print(f"{'ID':<4} {'Extension':<20} {'Timestamp':<20} {'Label'}")
        print("-" * 70)
        for r in rows:
            print(f"{r['id']:<4} {r['slug']:<20} {r['timestamp']:<20} {r['label'] or '-'}")
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# argparse wiring
# ---------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="CLI du Chromium Control Plane (CCP)")
    sub = parser.add_subparsers(dest="command", required=True)

    # --- extensions ---
    p_ext = sub.add_parser("extensions", help="Gestion des extensions")
    p_ext_sub = p_ext.add_subparsers(dest="action", required=True)

    p_ext_add = p_ext_sub.add_parser("add", help="Ajouter une extension")
    p_ext_add.add_argument("--slug", required=True)
    p_ext_add.add_argument("--manifest-path", required=True)
    p_ext_add.add_argument("--git-repo", required=True)
    p_ext_add.add_argument("--git-commit", default=None)
    p_ext_add.add_argument("--version", default=None)
    p_ext_add.add_argument("--unpacked", action="store_true")
    p_ext_add.add_argument("--status", default="disabled")
    p_ext_add.add_argument("--auto-reload", action="store_true")
    p_ext_add.set_defaults(func=ext_add)

    p_ext_list = p_ext_sub.add_parser("list", help="Lister les extensions")
    p_ext_list.set_defaults(func=ext_list)

    p_ext_rm = p_ext_sub.add_parser("rm", help="Supprimer une extension")
    p_ext_rm.add_argument("--ext-id", type=int, required=True)
    p_ext_rm.set_defaults(func=ext_rm)

    p_ext_status = p_ext_sub.add_parser("set-status", help="Changer le statut d'une extension")
    p_ext_status.add_argument("--ext-id", type=int, required=True)
    p_ext_status.add_argument("--status", required=True, choices=["active", "disabled", "unknown"])
    p_ext_status.set_defaults(func=ext_set_status)

    # --- daemon-bridges ---
    p_bridge = sub.add_parser("daemon-bridges", help="Gestion des ponts de daemons locaux")
    p_bridge_sub = p_bridge.add_subparsers(dest="action", required=True)

    p_bridge_add = p_bridge_sub.add_parser("add", help="Ajouter un bridge")
    p_bridge_add.add_argument("--ext-id", type=int, required=True)
    p_bridge_add.add_argument("--port", type=int, required=True)
    p_bridge_add.add_argument("--protocol", default="ws")
    p_bridge_add.add_argument("--expected-status", type=int, default=200)
    p_bridge_add.add_argument("--fail-policy", default="fail-silent")
    p_bridge_add.add_argument("--description", default=None)
    p_bridge_add.set_defaults(func=bridge_add)

    p_bridge_list = p_bridge_sub.add_parser("list", help="Lister les bridges")
    p_bridge_list.set_defaults(func=bridge_list)

    p_bridge_rm = p_bridge_sub.add_parser("rm", help="Supprimer un bridge")
    p_bridge_rm.add_argument("--bridge-id", type=int, required=True)
    p_bridge_rm.set_defaults(func=bridge_rm)

    # --- telemetry ---
    p_tele = sub.add_parser("telemetry", help="Lecture des événements de télémétrie")
    p_tele_sub = p_tele.add_subparsers(dest="action", required=True)

    p_tele_add = p_tele_sub.add_parser("add", help="Ajouter un événement")
    p_tele_add.add_argument("--ext-id", type=int, default=None)
    p_tele_add.add_argument("--source", required=True)
    p_tele_add.add_argument("--level", required=True)
    p_tele_add.add_argument("--message", required=True)
    p_tele_add.add_argument("--stack-trace", default=None)
    p_tele_add.set_defaults(func=telemetry_add)

    p_tele_list = p_tele_sub.add_parser("list", help="Lister les événements")
    p_tele_list.add_argument("--ext-id", type=int, default=None)
    p_tele_list.add_argument("--level", default=None)
    p_tele_list.add_argument("--unresolved", action="store_true")
    p_tele_list.add_argument("--limit", type=int, default=50)
    p_tele_list.set_defaults(func=telemetry_list)

    p_tele_resolve = p_tele_sub.add_parser("resolve", help="Marquer un événement résolu")
    p_tele_resolve.add_argument("--event-id", type=int, required=True)
    p_tele_resolve.set_defaults(func=telemetry_resolve)

    # --- snapshots ---
    p_snap = sub.add_parser("snapshots", help="Gestion des instantanés d'état")
    p_snap_sub = p_snap.add_subparsers(dest="action", required=True)

    p_snap_add = p_snap_sub.add_parser("add", help="Ajouter un snapshot")
    p_snap_add.add_argument("--ext-id", type=int, required=True)
    p_snap_add.add_argument("--label", default=None)
    p_snap_add.add_argument("--storage-file", required=True)
    p_snap_add.set_defaults(func=snapshot_add)

    p_snap_list = p_snap_sub.add_parser("list", help="Lister les snapshots")
    p_snap_list.set_defaults(func=snapshot_list)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
