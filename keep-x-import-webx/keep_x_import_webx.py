#!/usr/bin/env python3
# =============================================================================
# keep_x_import_webx.py — Import de notes Google Keep via WEBX
#
# Utilise WEBX (D:\DO\WEB\TOOLS\L2-PLATFORM\WEBX\src) pour piloter un navigateur
# headless (CamoFox, Obscura, Chrome) et extraire les notes Google Keep via
# scraping DOM/CDP, puis les injecter dans DuckDB.
#
# Politique :
# - Zéro dépendance gkeepapi
# - Zéro dialogue LLM requis
# - Déduplication par hash SHA-256
# - Merkle seal WAL-0x243
# =============================================================================
from __future__ import annotations

import hashlib
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import duckdb

# Ajout du chemin WEBX au PYTHONPATH
WEBX_SRC = r"D:\DO\WEB\TOOLS\L2-PLATFORM\WEBX\src"
if WEBX_SRC not in sys.path:
    sys.path.insert(0, WEBX_SRC)

from webx.cluster import WebCluster  # noqa: E402
from webx.skills.scrape_dom import ScrapeDom  # noqa: E402

WAL_SEAL = "WAL-0x243-KEEP-IMPORT-WEBX"
DUCKDB_PATH = r"D:\DO\WEB\TOOLS\L0-CANON\ENV3-repo\WAL\do_core_inference.duckdb"
KEEP_URL = "https://keep.google.com"


class KeepXImportWebX:
    """Importe les notes Google Keep via WEBX (navigateur headless ou Chrome ouvert)."""

    def __init__(self, duckdb_path: str = DUCKDB_PATH) -> None:
        self.duckdb_path = duckdb_path
        self.cluster: Optional[WebCluster] = None
        self.session_id: Optional[str] = None

    # ------------------------------------------------------------------
    # DuckDB
    # ------------------------------------------------------------------
    def _ensure_table(self, con: duckdb.DuckDBPyConnection) -> None:
        con.execute("""
            CREATE TABLE IF NOT EXISTS keep_entities (
                entity_id VARCHAR PRIMARY KEY,
                timestamp TIMESTAMP,
                title VARCHAR,
                body_text TEXT,
                labels JSON,
                merkle_seal VARCHAR,
                hash_sha256 VARCHAR UNIQUE
            )
        """)

    def _compute_hash(self, title: str, body: str) -> str:
        return hashlib.sha256((title + body).encode("utf-8")).hexdigest()

    def _insert_note(self, con: duckdb.DuckDBPyConnection, title: str, body: str) -> bool:
        h = self._compute_hash(title, body)
        entity_id = f"keep-{h[:8]}"
        try:
            con.execute("""
                INSERT INTO keep_entities (entity_id, timestamp, title, body_text, labels, merkle_seal, hash_sha256)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT (hash_sha256) DO NOTHING
            """, [entity_id, datetime.now(timezone.utc), title, body, "[]", WAL_SEAL, h])
            return True
        except Exception:
            return False

    # ------------------------------------------------------------------
    # Extraction DOM via ScrapeDom
    # ------------------------------------------------------------------
    def _extract_notes_from_dom(self, scraper: ScrapeDom) -> List[Dict[str, str]]:
        """Extrait les notes depuis le DOM de Google Keep via JS."""
        js = """
        () => {
            const allDivs = document.querySelectorAll('div');
            const notes = [];
            allDivs.forEach(div => {
                const text = (div.innerText || '').trim();
                if (text.length > 5 && text.length < 2000) {
                    const lines = text.split('\\n');
                    const title = lines[0] || '';
                    const body = lines.slice(1).join('\\n') || '';
                    notes.push({title, body});
                }
            });
            const seen = new Set();
            return notes.filter(n => {
                const key = n.title + '|' + n.body;
                if (seen.has(key)) return false;
                seen.add(key);
                return true;
            });
        }
        """
        try:
            result = scraper._context.pages[0].evaluate(js)
            return result if result is not None else []
        except Exception:
            return []

    # ------------------------------------------------------------------
    # Import via navigateur headless (WEBX)
    # ------------------------------------------------------------------
    def import_from_keep(self, browser: str = "camofox") -> Dict[str, Any]:
        """Importe les notes Google Keep via navigateur headless (WEBX)."""
        from webx.cluster import WebCluster

        self.cluster = WebCluster()
        result = self.cluster.launch(browser=browser, profile_template="bdcp-base")
        self.session_id = result["session"]
        self.driver = result["driver"]

        cdp_port = self.driver.get("cdp_port", 9225)
        cdp_url = f"http://127.0.0.1:{cdp_port}"

        scraper = ScrapeDom(cdp_url=cdp_url)
        try:
            scraper.connect()
            page = scraper._context.pages[0] if scraper._context.pages else scraper._context.new_page()
            page.goto(KEEP_URL, wait_until="domcontentloaded", timeout=30000)

            import time
            time.sleep(8)  # Attendre le chargement des notes

            notes = self._extract_notes_from_dom(scraper)
            return self._insert_notes_into_duckdb(notes, browser)
        finally:
            scraper.close()
            if self.session_id:
                self.cluster.shutdown(self.session_id)

    def _insert_notes_into_duckdb(self, notes: List[Dict[str, str]], browser: str) -> Dict[str, Any]:
        con = duckdb.connect(self.duckdb_path)
        self._ensure_table(con)
        inserted = 0
        for n in notes:
            title = n.get("title", "")
            body = n.get("body", "")
            if title or body:
                if self._insert_note(con, title, body):
                    inserted += 1

        total = con.execute("SELECT count(*) FROM keep_entities").fetchone()[0]
        con.close()

        return {
            "status": "ok",
            "browser": browser,
            "notes_extracted": len(notes),
            "notes_inserted": inserted,
            "total_in_db": total,
            "merkle_seal": WAL_SEAL,
        }


def main() -> int:
    importer = KeepXImportWebX()
    try:
        result = importer.import_from_keep(browser="camofox")
        import json
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0 if result["status"] == "ok" else 1
    except Exception as exc:  # noqa: BLE001
        print(f"[ERREUR] {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())