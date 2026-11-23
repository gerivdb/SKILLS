import json, os, sys, time, sqlite3, urllib.request, datetime, signal, threading

REPO   = r"D:\DO\WEB\TOOLS\L0-CANON\ENV3-repo"
CDP    = "http://127.0.0.1:9222"
CYPHER = "http://127.0.0.1:8080/cypher"
DB     = os.path.join(REPO, ".swarm", "relate_graph.db")
EVID   = os.path.join(REPO, "e2e_output", "queue_drain_evidence.json")
SESSION_ID = "session:3e3c4b19-a15f-466e-9cad-6c0581107bf1"
STOP = threading.Event()

def http_json(url, payload=None, timeout=5):
    data = json.dumps(payload).encode() if payload else None
    req = urllib.request.Request(url, data=data,
        headers={"Content-Type": "application/json"}, method="POST" if payload else "GET")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())

def cdp_eval(ws_url, expr, timeout=10):
    import websocket
    ws = websocket.create_connection(ws_url, timeout=timeout, suppress_origin=True)
    try:
        ws.send(json.dumps({"id": 1, "method": "Runtime.evaluate",
            "params": {"expression": expr, "returnByValue": True, "awaitPromise": True}}))
        t0 = time.time()
        while time.time() - t0 < timeout:
            r = json.loads(ws.recv())
            if r.get("id") == 1:
                return r.get("result", {}).get("result", {}).get("value")
    finally:
        ws.close()

def find_tab():
    try:
        tabs = json.loads(urllib.request.urlopen(CDP + "/json/list", timeout=5).read())
    except Exception:
        return None
    # prefer protected session
    for t in tabs:
        if t.get("type") == "page" and "3e3c4b19-a15f-466e-9cad-6c0581107bf1" in t.get("url", ""):
            return t
    return next((t for t in tabs if t.get("type") == "page" and "chat.deepseek.com" in t.get("url", "")), None)

def drain_queue():
    tab = find_tab()
    if not tab or not tab.get("webSocketDebuggerUrl"):
        return {"drained": 0, "error": "no_tab"}
    try:
        raw = cdp_eval(tab["webSocketDebuggerUrl"],
            "JSON.stringify(window.__RELATE_QUEUE || [])")
        queue = json.loads(raw) if raw else []
    except Exception as e:
        return {"drained": 0, "error": str(e)}
    if not queue:
        return {"drained": 0, "total": 0}

    drained = 0
    for item in queue:
        try:
            payload = item.get("payload") or item
            # cypher payload
            if isinstance(payload, dict) and "query" in payload:
                http_json(CYPHER, payload)
                drained += 1
                continue
            # raw pulse fallback (Option 2 adapter enqueues {sid,tid,type,role,turn,...} on fetch failure)
            if isinstance(item, dict) and ("turn" in item or "tid" in item):
                sid = item.get("sid") or SESSION_ID
                tid = item.get("tid") or ("turn:" + str(item.get("turn")))
                typ = item.get("type") or "TURN_COMPLETE"
                role = item.get("role") or "assistant"
                http_json(CYPHER, {"query":"MERGE (t:Turn {id: $id}) SET t.type=$type,t.role=$role RETURN t","params":{"id":tid,"type":typ,"role":role}})
                http_json(CYPHER, {"query":"MERGE (s)-[:CONTAINS]->(t)","params":{"from":sid,"to":tid,"sid":sid,"tid":tid}})
                drained += 1
                continue
        except Exception as e:
            print(f"[Drain] Item failed: {e}")
    try:
        cdp_eval(tab["webSocketDebuggerUrl"], "window.__RELATE_QUEUE = []; 'cleared'")
    except Exception:
        pass
    return {"drained": drained, "total": len(queue)}

def backfill_orphans():
    """Relie les Turn sans arête CONTAINS à la session active."""
    conn = sqlite3.connect(DB)
    try:
        # schema: nodes(id,label,props), edges(src,rel,dst)
        rows = conn.execute("""
            SELECT id FROM nodes WHERE label='Turn'
            AND id NOT IN (SELECT dst FROM edges WHERE rel='CONTAINS' AND src LIKE 'session:%')
        """).fetchall()
        orphans = [r[0] for r in rows]
        for tid in orphans:
            conn.execute("INSERT INTO edges (src, rel, dst) VALUES (?, ?, ?)",
                         (SESSION_ID, "CONTAINS", tid))
        conn.commit()
        # report
        linked = conn.execute("SELECT COUNT(*) FROM edges WHERE rel='CONTAINS' AND src LIKE 'session:%' AND dst LIKE 'turn:%'").fetchone()[0]
        return {"orphans_fixed": len(orphans), "linked_session_to_turn": linked}
    finally:
        conn.close()

def loop():
    cycle = 0
    while not STOP.is_set():
        cycle += 1
        ts = datetime.datetime.now().isoformat(timespec="seconds")
        d = drain_queue()
        b = backfill_orphans() if cycle % 4 == 0 or cycle == 1 else {"orphans_fixed": 0}
        entry = {"ts": ts, "cycle": cycle, "drain": d, "backfill": b}
        try:
            with open(EVID, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except Exception as e:
            print(f"[Drain-Daemon] evidence write failed: {e}")
        print(f"[Drain-Daemon] cycle={cycle} drain={d.get('drained')} total={d.get('total')} backfill={b.get('orphans_fixed')} linked={b.get('linked_session_to_turn')}")
        STOP.wait(20)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, lambda *a: STOP.set())
    print("[Drain-Daemon] Start (drain 20s, backfill 80s + cycle1)")
    t = threading.Thread(target=loop, daemon=True)
    t.start()
    try:
        while not STOP.is_set():
            time.sleep(1)
    except KeyboardInterrupt:
        STOP.set()
    print("[Drain-Daemon] Stopped.")
