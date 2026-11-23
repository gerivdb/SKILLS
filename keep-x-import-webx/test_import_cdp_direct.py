#!/usr/bin/env python3
# Test d'extraction Keep via CDP WebSocket direct (sans Playwright)
import asyncio
import websockets
import json
import duckdb
import hashlib
from datetime import datetime, timezone

CDP_WS_URL = "ws://127.0.0.1:9222/devtools/page/7512BE6D"
DUCKDB_PATH = r"D:\DO\WEB\TOOLS\L0-CANON\ENV3-repo\WAL\do_core_inference.duckdb"
WAL_SEAL = "WAL-0x243-KEEP-IMPORT-WEBX"

async def cdp_call(ws, method, params=None, timeout=10):
    msg_id = 1
    msg = {"id": msg_id, "method": method}
    if params:
        msg["params"] = params
    await ws.send(json.dumps(msg))
    deadline = asyncio.get_event_loop().time() + timeout
    while True:
        remaining = deadline - asyncio.get_event_loop().time()
        if remaining <= 0:
            raise TimeoutError("CDP timeout")
        try:
            resp = await asyncio.wait_for(ws.recv(), timeout=remaining)
        except asyncio.TimeoutError:
            raise TimeoutError("CDP recv timeout")
        data = json.loads(resp)
        if data.get("id") == msg_id:
            return data

async def main():
    async with websockets.connect(CDP_WS_URL) as ws:
        # Activer Runtime et Page
        await cdp_call(ws, "Runtime.enable")
        await cdp_call(ws, "Page.enable")

        # Extraire les notes via JS
        result = await cdp_call(ws, "Runtime.evaluate", {
            "expression": """
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
            """,
            "returnByValue": True
        })

        notes = []
        if "result" in result and "value" in result["result"]:
            notes = result["result"]["value"]

        print(f"Notes extraites : {len(notes)}")
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

        print(f"\n=== RESULTAT ===")
        print(f"Notes extraites : {len(notes)}")
        print(f"Notes inserees : {inserted}")
        print(f"Total dans DuckDB : {total}")

        return 0

if __name__ == "__main__":
    import sys
    sys.exit(asyncio.run(main()))