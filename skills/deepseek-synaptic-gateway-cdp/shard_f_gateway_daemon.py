
import os, json, time, sqlite3, urllib.request, urllib.error, base64, hashlib, datetime

REPO = r"D:\DO\WEB\TOOLS\L0-CANON\ENV3-repo"
DB = os.path.join(REPO, ".swarm", "relate_graph.db")
CTX = os.path.join(REPO, ".swarm", "context_live.json")
TOKEN_PATH = os.path.join(REPO, "e2e_output", "current_token.json")
AUTH_PATH = os.path.join(REPO, "e2e_output", "captured_extra_info.json")
CAPTURE_PATH = os.path.join(REPO, "e2e_output", "captured_chat_completion_v2.json")
EVID = os.path.join(REPO, "e2e_output", "shard_f_gateway_evidence.json")
SESSION_ID_DEFAULT = "3e3c4b19-a15f-466e-9cad-6c0581107bf1"


def get_token():
    with open(TOKEN_PATH, "r", encoding="utf-8") as f:
        d = json.load(f)
    return d.get("token") or d.get("value") or d


def get_cookie_header():
    # prefer full captured_extra_info.json, fallback to v2 capture associated cookies
    try:
        if os.path.exists(AUTH_PATH):
            with open(AUTH_PATH, "r", encoding="utf-8") as f:
                d = json.load(f)
            h = d.get("headers") or {}
            for k in ("Cookie", "cookie"):
                if h.get(k):
                    return h[k]
    except Exception:
        pass
    try:
        if os.path.exists(CAPTURE_PATH):
            with open(CAPTURE_PATH, "r", encoding="utf-8") as f:
                d = json.load(f)
            extra = ((d.get("data") or {}).get("requestWillBeSentExtraInfo") or {})
            h = extra.get("headers") or {}
            for k in ("cookie", "Cookie"):
                if h.get(k):
                    return h[k]
            cookies = extra.get("associatedCookies") or []
            parts = []
            for ac in cookies:
                c = (ac or {}).get("cookie") or {}
                if c.get("name") and c.get("value") is not None:
                    parts.append(f"{c['name']}={c['value']}")
            if parts:
                return "; ".join(parts)
    except Exception:
        pass
    return None


def get_pow_challenge(token, target_path="/api/v0/chat/completion"):
    req = urllib.request.Request(
        "https://chat.deepseek.com/api/v0/chat/create_pow_challenge",
        data=json.dumps({"target_path": target_path}).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        data = json.loads(r.read().decode())
        biz = (data.get("data") or {}).get("biz_data") or {}
        ch = biz.get("challenge")
        if not ch:
            raise RuntimeError(f"no_challenge:{json.dumps(data, ensure_ascii=False)[:500]}")
        return ch


def solve_pow(challenge):
    salt = challenge["salt"]
    ch = challenge["challenge"]
    diff = int(challenge["difficulty"])
    target = (1 << 256) // diff
    nonce = 0
    t0 = time.time()
    # DeepSeekHashV1 (WebAI2API-style): concat salt+challenge+nonce, compare full hash int to target
    while True:
        h = hashlib.sha256(f"{salt}{ch}{nonce}".encode()).hexdigest()
        if int(h, 16) <= target:
            break
        nonce += 1
        if nonce % 500000 == 0 and (time.time() - t0) > 180:
            raise TimeoutError(f"pow_solve_timeout nonce={nonce} ms={int((time.time()-t0)*1000)}")
    ans = {
        "algorithm": challenge.get("algorithm", "DeepSeekHashV1"),
        "challenge": challenge["challenge"],
        "salt": challenge["salt"],
        "answer": nonce,
        "signature": challenge.get("signature", ""),
        "target_path": challenge.get("target_path", "/api/v0/chat/completion"),
    }
    # include expire fields if present (harmless, some impls expect them)
    for k in ("expire_at", "expire_after"):
        if k in challenge:
            ans[k] = challenge[k]
    pow_b64 = base64.b64encode(json.dumps(ans, separators=(",", ":")).encode()).decode()
    return pow_b64, {"nonce": nonce, "ms": int((time.time()-t0)*1000), "difficulty": diff, "answer_type": "int"}


def parse_stream(raw_bytes):
    text_parts = []
    saw_sse = False
    for raw in raw_bytes.splitlines():
        line = raw.decode("utf-8", errors="replace").strip()
        if not line.startswith("data:"):
            continue
        saw_sse = True
        data_str = line[5:].strip()
        if not data_str or data_str == "[DONE]":
            continue
        try:
            chunk = json.loads(data_str)
        except Exception:
            continue
        if not isinstance(chunk, dict):
            continue
        v = chunk.get("v")
        p = chunk.get("p")
        if isinstance(v, str):
            # accumulate content-like v fields
            if p in (None, "response/content", "content") or (isinstance(p, str) and "content" in p):
                if v:
                    text_parts.append(v)
        choices = chunk.get("choices") or []
        for ch in choices:
            if not isinstance(ch, dict):
                continue
            delta = ch.get("delta") or {}
            if isinstance(delta, dict) and isinstance(delta.get("content"), str):
                text_parts.append(delta["content"])
            msg = ch.get("message") or {}
            if isinstance(msg, dict) and isinstance(msg.get("content"), str):
                text_parts.append(msg["content"])
        dobj = chunk.get("data")
        if isinstance(dobj, dict) and isinstance(dobj.get("content"), str):
            text_parts.append(dobj["content"])
    text = "".join(text_parts).strip()
    if text:
        return text, saw_sse
    raw_s = raw_bytes.decode("utf-8", errors="replace")
    try:
        j = json.loads(raw_s)
        return json.dumps(j, ensure_ascii=False), saw_sse
    except Exception:
        return raw_s[:8000], saw_sse


def call_api(token, prompt, session_id):
    cookie = get_cookie_header()
    try:
        challenge = get_pow_challenge(token)
        pow_header, pow_meta = solve_pow(challenge)
    except Exception as e:
        return {"ok": False, "error": f"pow_failed: {e}", "cookie_present": bool(cookie)}

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "text/event-stream, application/json",
        "x-ds-pow-response": pow_header,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
        "Origin": "https://chat.deepseek.com",
        "Referer": f"https://chat.deepseek.com/a/chat/s/{session_id}",
    }
    if cookie:
        headers["Cookie"] = cookie
    payload = {
        "chat_session_id": session_id,
        "prompt": prompt,
        "ref_file_ids": [],
        "thinking_enabled": False,
    }
    req = urllib.request.Request(
        "https://chat.deepseek.com/api/v0/chat/completion",
        data=json.dumps(payload).encode(),
        headers=headers, method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            status = r.status
            ctype = r.headers.get("Content-Type")
            raw = r.read()
        raw_s = raw.decode("utf-8", errors="replace")
        # detect API-level errors
        try:
            j = json.loads(raw_s)
            if isinstance(j, dict) and j.get("code") not in (None, 0):
                return {"ok": False, "error": f"API_{j.get('code')}", "msg": j.get("msg"), "body": raw_s[:1200], "status": status, "ctype": ctype, "pow": pow_meta, "cookie_present": bool(cookie)}
        except Exception:
            pass
        text, saw_sse = parse_stream(raw)
        if isinstance(text, str) and text.strip():
            if text.startswith("{") and '"code"' in text:
                try:
                    jj = json.loads(text)
                    if isinstance(jj, dict) and jj.get("code") not in (None, 0):
                        return {"ok": False, "error": f"API_{jj.get('code')}", "msg": jj.get("msg"), "body": text[:1200], "status": status, "ctype": ctype, "pow": pow_meta, "saw_sse": saw_sse, "cookie_present": bool(cookie)}
                except Exception:
                    pass
            return {"ok": True, "text": text, "status": status, "ctype": ctype, "saw_sse": saw_sse, "pow": pow_meta, "raw_len": len(raw), "cookie_present": bool(cookie)}
        return {"ok": False, "error": "EMPTY_RESPONSE", "body": raw_s[:1200], "status": status, "ctype": ctype, "saw_sse": saw_sse, "pow": pow_meta, "cookie_present": bool(cookie)}
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace") if hasattr(e, "read") else str(e)
        return {"ok": False, "error": f"HTTP_{e.code}", "body": body[:1200], "pow": pow_meta, "cookie_present": bool(cookie)}
    except Exception as e:
        return {"ok": False, "error": str(e), "pow": pow_meta, "cookie_present": bool(cookie)}


def write_db(text, session_id, meta):
    conn = sqlite3.connect(DB)
    try:
        ts = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
        nid = f"env6:decision:{ts.replace(':','').replace('+','p')}"
        props = {
            "text": (text or "")[:8000],
            "source": "ENV6",
            "ts": ts,
            "session_id": session_id,
            "mode": "http_pow_v2",
            "meta": meta or {},
        }
        conn.execute(
            "INSERT OR REPLACE INTO nodes (id, label, props) VALUES (?, ?, ?)",
            (nid, "Decision", json.dumps(props, ensure_ascii=False)),
        )
        conn.execute(
            "INSERT OR IGNORE INTO edges (src, rel, dst) VALUES (?, ?, ?)",
            (f"session:{session_id}", "CONTAINS", nid),
        )
        conn.commit()
        return nid
    finally:
        conn.close()


def shrink(v, n=600):
    if isinstance(v, str) and len(v) > n:
        return v[:n] + f"...(+{len(v)-n})"
    if isinstance(v, dict):
        return {k: shrink(vv, n) for k, vv in v.items()}
    if isinstance(v, list):
        return [shrink(x, n) for x in v[:20]]
    return v


def main():
    print("[ShardF] Démarrage avec résolution PoW v2 (DeepSeekHashV1 concat, target 1<<256//diff, cookies).", flush=True)
    last_ctx = None
    while True:
        try:
            if not os.path.exists(CTX):
                time.sleep(10); continue
            with open(CTX, "r", encoding="utf-8") as f:
                ctx = json.load(f)
            if not ctx.get("recent_turns"):
                time.sleep(10); continue

            ctx_ts = ctx.get("generated_at") or json.dumps(ctx.get("frontispice", {}), sort_keys=True)
            if ctx_ts == last_ctx:
                time.sleep(30); continue

            session_id = SESSION_ID_DEFAULT
            sid = (ctx.get("frontispice") or {}).get("shard_id", "")
            if isinstance(sid, str) and sid.startswith("session:"):
                session_id = sid.split("session:", 1)[1]

            prompt = f"Contexte synaptique: {json.dumps(ctx, ensure_ascii=False)[:3500]}. Analyse et génère ta prochaine directive d'audit courte et traçable."
            print(f"[ShardF] Appel API avec PoW v2 session={session_id}...", flush=True)
            res = call_api(get_token(), prompt, session_id)

            ev = {"ts": datetime.datetime.now().astimezone().isoformat(timespec="seconds"), "session_id": session_id}
            if res.get("ok") and res.get("text"):
                nid = write_db(res["text"], session_id, {"pow": res.get("pow"), "status": res.get("status"), "ctype": res.get("ctype"), "saw_sse": res.get("saw_sse"), "raw_len": res.get("raw_len"), "cookie_present": res.get("cookie_present")})
                ev["ok"] = True
                ev["db_node"] = nid
                ev["response_chars"] = len(res["text"])
                ev["api"] = shrink({k:v for k,v in res.items() if k != "text"})
                ev["text_preview"] = res["text"][:500]
                print(f"[ShardF] SUCCESS: {nid} chars={len(res['text'])} pow_ms={((res.get('pow') or {}).get('ms'))}", flush=True)
                last_ctx = ctx_ts
            else:
                ev["ok"] = False
                ev["api"] = shrink(res)
                print(f"[ShardF] FAIL: {json.dumps(shrink({k:v for k,v in res.items() if k!='text'}), ensure_ascii=False)[:1600]}", flush=True)

            with open(EVID, "w", encoding="utf-8") as f:
                json.dump(ev, f, indent=2, ensure_ascii=False)
            time.sleep(60)
        except Exception as e:
            print(f"[ShardF] ERREUR: {e!r}", flush=True)
            try:
                with open(EVID, "w", encoding="utf-8") as f:
                    json.dump({"ts": datetime.datetime.now().astimezone().isoformat(timespec="seconds"), "ok": False, "exception": repr(e)}, f, indent=2, ensure_ascii=False)
            except Exception:
                pass
            time.sleep(30)


if __name__ == "__main__":
    main()
