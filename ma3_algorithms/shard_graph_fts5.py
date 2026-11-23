"""BinarySearch integration pour shard_graph.db (M3-Graph) — optimisation FTS5.

Fournit une recherche binaire sur les rowids retournes par les requetes FTS5,
evitant un scan lineaire et accelerant les requetes de graph M3-Graph.
"""

import sqlite3
from pathlib import Path
from typing import Optional

try:
    from .binary_search import BinarySearch
except ImportError:
    from binary_search import BinarySearch


class ShardGraphFTS5:
    """Wrapper autour d une base shard_graph.db (SQLite FTS5) utilisant
    BinarySearch pour optimiser les recherches de rowids."""

    def __init__(self, db_path: str | Path):
        self.db_path = str(db_path)
        self._conn: Optional[sqlite3.Connection] = None

    def _connect(self) -> sqlite3.Connection:
        if self._conn is None:
            self._conn = sqlite3.connect(self.db_path)
            self._conn.row_factory = sqlite3.Row
        return self._conn

    def close(self) -> None:
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def fts5_rowids(self, fts_table: str, query: str) -> list[int]:
        """Retourne la liste triee des rowids correspondants a une requete FTS5."""
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(
            f"SELECT rowid FROM {fts_table} WHERE {fts_table} MATCH ? ORDER BY rowid",
            (query,),
        )
        return [row[0] for row in cur.fetchall()]

    def find_rowid(self, fts_table: str, query: str, target_rowid: int) -> int:
        """Recherche binaire du target_rowid parmi les resultats FTS5.

        Retourne l index dans la liste des rowids, ou -1 si absent.
        """
        rowids = self.fts5_rowids(fts_table, query)
        return BinarySearch.fts5_rowid_lookup(rowids, target_rowid)

    def rowid_exists(self, fts_table: str, query: str, target_rowid: int) -> bool:
        """Verifie si target_rowid est present parmi les resultats FTS5."""
        return self.find_rowid(fts_table, query, target_rowid) != -1

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

