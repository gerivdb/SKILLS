#!/usr/bin/env python3
# Test ultra-rapide : se connecter au CDP de Chrome, prendre l'onglet Keep existant, extraire les notes
import sys
sys.path.insert(0, r'D:\DO\WEB\TOOLS\L2-PLATFORM\WEBX\src')

from playwright.sync_api import sync_playwright
import duckdb
import hashlib
from datetime import datetime, timezone

CDP_URL = "http://127.0.0.1:9222"
DUCKDB_PATH = r"D:\DO\WEB\TOOLS\L0-CANON\ENV3-repo\WAL\do_core_inference.duckdb"
WAL_SEAL = "WAL-0x243-KEEP-IMPORT-WEBX"

def main():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP_URL)
        contexts = browser.contexts
        if not contexts:
            print("ERREUR: Aucun contexte de navigateur")
            return 1
        context = contexts[0]
        pages = context.pages
        
        print(f"Onglets ouverts : {len(pages)}")
        for i, pg in enumerate(pages):
            print(f"  Onglet {i}: {pg.url[:80]} | {pg.title()[:60]}")
        
        # Chercher un onglet Keep
        keep_page = None
        for pg in pages:
            if "keep.google.com" in pg.url:
                keep_page = pg
                break
        
        if keep_page is None:
            print("ERREUR: Aucun onglet keep.google.com ouvert")
            print("Veuillez ouvrir keep.google.com dans Chrome")
            return 1
        
        print(f"\nExtraction depuis l'onglet Keep : {keep_page.url}")
        
        # Attendre un peu que le contenu se charge
        keep_page.wait_for_timeout(3000)
        
        # Extraire les notes via JS
        notes = keep_page.evaluate("""
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
        """)
        
        print(f"\nNotes extraites : {len(notes)}")
        for n in notes[:10]:
            print(f"  - {n['title'][:50]}: {n['body'][:80]}")
        
        # Insérer dans DuckDB
        con = duckdb.connect(DUCKDB_PATH)
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
        inserted = 0
        for n in notes:
            title = n.get("title", "")
            body = n.get("body", "")
            if title or body:
                h = hashlib.sha256((title + body).encode("utf-8")).hexdigest()
                entity_id = f"keep-{h[:8]}"
                try:
                    con.execute("""
                        INSERT INTO keep_entities (entity_id, timestamp, title, body_text, labels, merkle_seal, hash_sha256)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        ON CONFLICT (hash_sha256) DO NOTHING
                    """, [entity_id, datetime.now(timezone.utc), title, body, "[]", WAL_SEAL, h])
                    inserted += 1
                except Exception as e:
                    print(f"  Erreur insertion: {e}")
        
        total = con.execute("SELECT count(*) FROM keep_entities").fetchone()[0]
        con.close()
        
        print(f"\n=== RÉSULTAT ===")
        print(f"Notes extraites : {len(notes)}")
        print(f"Notes insérées : {inserted}")
        print(f"Total dans DuckDB : {total}")
        
        browser.close()
        return 0

if __name__ == "__main__":
    sys.exit(main())