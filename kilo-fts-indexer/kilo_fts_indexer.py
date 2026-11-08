#!/usr/bin/env python3
"""
Skill: kilo-fts-indexer
Rôle: Indexer l'historique KiloCode (kilo.db) dans une table FTS5 pour une recherche plein-texte instantanée.
Contrainte: Ne JAMAIS modifier kilo.db source. L'index est créé dans une base séparée.
"""
import sys
import json
import sqlite3
import argparse
from pathlib import Path

KILO_DB_DEFAULT = r"C:\Users\GG\.local\share\kilo\kilo.db"
INDEX_DB_DEFAULT = r"C:\Users\GG\.local\share\kilo\kilo_fts_index.db"


def connect_source(db_path: str) -> sqlite3.Connection:
    """Ouvre kilo.db en lecture seule (mode immutable pour éviter tout verrouillage)."""
    uri = f"file:{db_path}?mode=ro"
    conn = sqlite3.connect(uri, uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def discover_tables(conn: sqlite3.Connection) -> list[str]:
    """Liste les tables contenant des messages/conversations."""
    cur = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    )
    return [r[0] for r in cur.fetchall()]


def build_index(source_db: str, index_db: str, limit: int | None = None, offset: int = 0) -> dict:
    """Construit (ou incrémente) l'index FTS5 depuis kilo.db vers une base séparée."""
    src = connect_source(source_db)
    tables = discover_tables(src)

    # Cherche une table de messages
    msg_table = None
    for t in tables:
        tl = t.lower()
        if "message" in tl or "part" in tl or "conversation" in tl:
            msg_table = t
            break

    if msg_table is None:
        src.close()
        return {"error": f"Aucune table de messages trouvée dans {tables}"}

    # Inspecter le schéma
    cur = src.execute(f"PRAGMA table_info({msg_table})")
    cols = [r[1] for r in cur.fetchall()]

    # Colonnes utiles pour le contenu et l'id
    content_col = None
    id_col = None
    for c in cols:
        cl = c.lower()
        if cl in ("content", "body", "text", "message"):
            content_col = c
        if cl in ("id", "message_id", "rowid"):
            id_col = c

    if content_col is None:
        src.close()
        return {"error": f"Aucune colonne de contenu trouvée dans {msg_table} ({cols})"}

    # Créer l'index FTS5 dans une base séparée
    idx = sqlite3.connect(index_db)
    idx.execute("CREATE VIRTUAL TABLE IF NOT EXISTS search_index USING fts5(content, session_id, id)")

    # Compter déjà indexé
    already = idx.execute("SELECT count(*) FROM search_index").fetchone()[0]

    # Insérer par lots
    batch = []
    batch_size = 1000
    inserted = 0
    scanned = 0

    query = f"SELECT {id_col or 'rowid'} as rid, {content_col} as cnt FROM {msg_table}"
    if limit:
        query += f" LIMIT {limit} OFFSET {offset}"

    cur = src.execute(query)
    for row in cur:
        scanned += 1
        rid = row["rid"] if row["rid"] is not None else scanned
        cnt = row["cnt"] or ""
        if not cnt.strip():
            continue
        batch.append((cnt, f"session_{scanned}", str(rid)))
        if len(batch) >= batch_size:
            idx.executemany(
                "INSERT OR IGNORE INTO search_index(content, session_id, id) VALUES (?, ?, ?)",
                batch,
            )
            idx.commit()
            inserted += len(batch)
            batch.clear()

    if batch:
        idx.executemany(
            "INSERT OR IGNORE INTO search_index(content, session_id, id) VALUES (?, ?, ?)",
            batch,
        )
        idx.commit()
        inserted += len(batch)

    src.close()
    idx.close()

    return {
        "table": msg_table,
        "columns": cols,
        "scanned": scanned,
        "inserted": inserted,
        "already_indexed": already,
        "index_db": index_db,
    }


def search(index_db: str, query: str, limit: int = 20) -> list[dict]:
    """Recherche plein-texte dans l'index FTS5."""
    idx = sqlite3.connect(index_db)
    idx.row_factory = sqlite3.Row
    cur = idx.execute(
        "SELECT id, session_id, content, bm25(search_index) as rank FROM search_index "
        "WHERE search_index MATCH ? ORDER BY rank LIMIT ?",
        (query, limit),
    )
    rows = [dict(r) for r in cur.fetchall()]
    idx.close()
    return rows


def main():
    parser = argparse.ArgumentParser(description="Indexeur FTS5 pour kilo.db (KiloCode)")
    sub = parser.add_subparsers(dest="command")

    p_build = sub.add_parser("build", help="Construire l'index FTS5")
    p_build.add_argument("--source", default=KILO_DB_DEFAULT, help="Chemin vers kilo.db")
    p_build.add_argument("--index", default=INDEX_DB_DEFAULT, help="Chemin de l'index de sortie")
    p_build.add_argument("--limit", type=int, default=None, help="Nombre max de messages à indexer")
    p_build.add_argument("--offset", type=int, default=0, help="Décalage pour reprise")

    p_search = sub.add_parser("search", help="Rechercher dans l'index")
    p_search.add_argument("--index", default=INDEX_DB_DEFAULT, help="Chemin de l'index")
    p_search.add_argument("q", help="Requête de recherche")
    p_search.add_argument("--limit", type=int, default=20, help="Nombre max de résultats")

    p_info = sub.add_parser("info", help="Informations sur les tables de kilo.db")
    p_info.add_argument("--source", default=KILO_DB_DEFAULT, help="Chemin vers kilo.db")

    args = parser.parse_args()

    if args.command == "build":
        result = build_index(args.source, args.index, args.limit, args.offset)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif args.command == "search":
        results = search(args.index, args.q, args.limit)
        print(json.dumps({"query": args.q, "count": len(results), "results": results}, indent=2, ensure_ascii=False))
    elif args.command == "info":
        src = connect_source(args.source)
        tables = discover_tables(src)
        info = {"tables": tables}
        for t in tables[:5]:
            cur = src.execute(f"PRAGMA table_info({t})")
            info[t] = [r[1] for r in cur.fetchall()]
        src.close()
        print(json.dumps(info, indent=2, ensure_ascii=False))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
