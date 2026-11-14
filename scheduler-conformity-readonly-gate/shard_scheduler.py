#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
shard_scheduler.py — Keep 3 shards active (A, C, E) on 16-thread host.
- A: DEEP-X/CDP+auth health (validate_deepseek_auth.py)
- C: conductor integrity (kilocode resolved, DEEP-X manifest consolidated >=24 scripts)
- E: hygiene (watchdog relay patch, env6_exports has valid export > 27 bytes)
Heartbeat -> .swarm/shards_heartbeat.jsonl. Operational autonomy (no HITL).
"""
import json
import os
import sys
import time
import threading
import subprocess
import datetime
import signal
import urllib.request
import glob
import shutil

REPO = r"D:\DO\WEB\TOOLS\L0-CANON\ENV3-repo"
HB = os.path.join(REPO, ".swarm", "shards_heartbeat.jsonl")
MANIFEST = r"D:\DO\WEB\TOOLS\L4-TOOLS\DEEP-X\chrome\manifest.json"
WATCHDOG = os.path.join(REPO, ".swarm", "watchdog_env6.py")
EXPORTS = os.path.join(REPO, ".swarm", "env6_exports")
CDP = "http://127.0.0.1:9222"
SHARD_E_CONFORMITY_EVIDENCE = os.path.join(REPO, "e2e_output", "shard_e_audit_evidence.json")
CONFORMITY_MAX_AGE_S = 300  # evidence older than this => fail-closed to readonly repli
EXT_PATHS = [
    r"D:\DO\WEB\TOOLS\L0-CANON\ENV3-repo\chromium-dom-bridge",
    r"D:\DO\WEB\TOOLS\L4-TOOLS\DEEP-X\chrome",
]
STOP = threading.Event()


def _purge_pycache(ext_paths):
    """Purge __pycache__ recursively in extension dirs to prevent Chromium load failures."""
    purged = []
    for base in ext_paths:
        if not os.path.isdir(base):
            continue
        for p in glob.glob(os.path.join(base, "**", "__pycache__"), recursive=True):
            try:
                shutil.rmtree(p, ignore_errors=True)
                if not os.path.exists(p):
                    purged.append(p)
            except Exception:
                pass
        # top-level __pycache__* variants (files/dirs)
        for p in glob.glob(os.path.join(base, "__pycache__*"), recursive=False):
            try:
                if os.path.isdir(p):
                    shutil.rmtree(p, ignore_errors=True)
                elif os.path.isfile(p):
                    os.remove(p)
                if not os.path.exists(p):
                    purged.append(p)
            except Exception:
                pass
    return purged


def _scan_stray_underscore(ext_paths):
    """Detect entries starting with '_' (excluding __pycache__) - alert only, no auto-delete."""
    strays = []
    for base in ext_paths:
        if not os.path.isdir(base):
            continue
        for root, dirs, files in os.walk(base):
            for name in list(dirs) + list(files):
                if name == "__pycache__" or name.startswith("__pycache__."):
                    continue
                if name.startswith("_"):
                    strays.append(os.path.join(root, name))
    # whitelist MV3 legit dirs
    WHITELIST = {"_locales", "_metadata", "_modules"}
    strays = [p for p in strays if os.path.basename(p) not in WHITELIST]
    return strays


def now():
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")


def heartbeat(shard, state, detail="", **extra):
    line = {"ts": now(), "shard": shard, "state": state, "detail": detail}
    if extra:
        line.update(extra)
    os.makedirs(os.path.dirname(HB), exist_ok=True)
    with open(HB, "a", encoding="utf-8") as f:
        f.write(json.dumps(line, ensure_ascii=False) + "\n")
    print(f"[{line['ts']}][{shard}] {state} {detail}", flush=True)


def shard_e_conformity_status():
    """Read Shard E (Strate CHECK) evidence. Fail-closed: missing/stale/fail => readonly repli."""
    try:
        if not os.path.exists(SHARD_E_CONFORMITY_EVIDENCE):
            return False, "missing_evidence"
        st = os.stat(SHARD_E_CONFORMITY_EVIDENCE)
        age = max(0, time.time() - st.st_mtime)
        with open(SHARD_E_CONFORMITY_EVIDENCE, "r", encoding="utf-8") as f:
            ev = json.load(f)
        if age > CONFORMITY_MAX_AGE_S:
            return False, f"stale_evidence age_s={int(age)}"
        passed = bool(ev.get("PASS"))
        readonly = bool(ev.get("readonly_required", not passed))
        if (not passed) or readonly:
            return False, f"fail_or_readonly PASS={passed} readonly={readonly}"
        return True, f"PASS age_s={int(age)}"
    except Exception as e:
        return False, f"evidence_error:{type(e).__name__}:{e}"


def run_script(path, timeout):
    if not os.path.exists(path):
        return {"rc": None, "ok": False, "note": "missing", "tail": path}
    try:
        p = subprocess.run(
            [sys.executable, path],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=REPO,
        )
        out = (p.stdout or "") + ("\n" + p.stderr if p.stderr else "")
        return {"rc": p.returncode, "ok": p.returncode == 0, "tail": out.strip()[-220:]}
    except subprocess.TimeoutExpired:
        return {"rc": 124, "ok": False, "tail": "timeout"}
    except Exception as e:
        return {"rc": 1, "ok": False, "tail": str(e)[:220]}


def cdp_ok():
    try:
        with urllib.request.urlopen(CDP + "/json/version", timeout=4) as r:
            j = json.loads(r.read().decode("utf-8", "replace"))
        return True, j.get("Browser")
    except Exception as e:
        return False, str(e)


# --- Shard A: DEEP-X/CDP + auth/session health ---
def job_A():
    ok_cdp, cdp_info = cdp_ok()
    if not ok_cdp:
        return {"rc": 1, "ok": False, "tail": f"cdp_unavailable:{cdp_info}"}
    script = os.path.join(REPO, "e2e_output", "validate_deepseek_auth.py")
    res = run_script(script, timeout=60)
    # treat AUTH_OK in output as success even if wrapper differs
    text = (res.get("tail") or "")
    ok = res.get("ok") or ("AUTH_OK" in text)
    return {"rc": 0 if ok else (res.get("rc") or 1), "ok": ok, "tail": f"cdp={cdp_info} {text}"[:240]}


# --- Shard C: conductor integrity (kilocode + manifest consolidated) ---
def job_C():
    try:
        import shutil
        kc = shutil.which("kilocode") or shutil.which("kilocode.cmd") or shutil.which("kilocode.exe")
        js_count = None
        if os.path.exists(MANIFEST):
            with open(MANIFEST, "r", encoding="utf-8") as f:
                m = json.load(f)
            js = ((m.get("content_scripts") or [{}])[0].get("js") or [])
            js_count = len(js)
        ok = bool(kc) and (js_count is not None and js_count >= 24)
        return {
            "rc": 0 if ok else 1,
            "ok": ok,
            "tail": f"kilocode={kc} manifest_js={js_count}",
        }
    except Exception as e:
        return {"rc": 2, "ok": False, "tail": str(e)[:240]}


# --- Shard E: hygiene (watchdog relay + valid export present + extension dir guards) ---
def job_E():
    try:
        purged = _purge_pycache(EXT_PATHS)
        strays = _scan_stray_underscore(EXT_PATHS)

        patched = False
        if os.path.exists(WATCHDOG):
            with open(WATCHDOG, "r", encoding="utf-8", errors="replace") as f:
                src = f.read()
            patched = all(tok in src for tok in ("tâche", "task", "export_")) or ("tâche" in src and "export_" in src)
        latest = None
        latest_size = 0
        if os.path.isdir(EXPORTS):
            files = [os.path.join(EXPORTS, n) for n in os.listdir(EXPORTS) if n.lower().endswith((".md", ".json"))]
            if files:
                latest = max(files, key=os.path.getmtime)
                latest_size = os.path.getsize(latest)
        ok = patched and latest_size > 27 and len(strays) == 0
        name = os.path.basename(latest) if latest else None
        detail = f"watchdog_patched={patched} latest={name} size={latest_size} purged={len(purged)} strays={len(strays)}"
        if purged:
            detail += f" purged_paths={purged[:3]}"
        if strays:
            detail += f" STRAY_UNDERSCORE={strays[:3]}"
        return {
            "rc": 0 if ok else 1,
            "ok": ok,
            "tail": detail[:280],
            "purged": purged,
            "strays": strays,
        }
    except Exception as e:
        return {"rc": 2, "ok": False, "tail": str(e)[:240]}


SHARDS = [
    ("A", 180, job_A),  # auth/CDP health
    ("C", 240, job_C),  # conductor/manifest integrity
    ("E", 120, job_E),  # hygiene/relay
]


def loop(shard, cadence, job):
    heartbeat(shard, "start", f"cadence={cadence}s")
    while not STOP.is_set():
        t0 = time.time()
        try:
            ok_e, e_detail = shard_e_conformity_status()
            if not ok_e:
                # Shard E (conformity) failed/stale => other shards must go read-only (repli)
                heartbeat(
                    shard,
                    "readonly_repli",
                    f"shard_e_conformity_blocked: {e_detail}",
                    rc=3,
                    conformity_ok=False,
                )
            else:
                res = job() or {}
                state = "ok" if res.get("ok") else "fail"
                heartbeat(shard, state, res.get("tail", ""), rc=res.get("rc"), conformity_ok=True)
        except Exception as e:
            heartbeat(shard, "error", str(e)[:240])
        elapsed = time.time() - t0
        wait = max(2.0, cadence - elapsed)
        STOP.wait(wait)
    heartbeat(shard, "stop")


def main():
    def _stop(*_):
        STOP.set()

    signal.signal(signal.SIGINT, _stop)
    try:
        signal.signal(signal.SIGTERM, _stop)
    except Exception:
        pass

    print(f"[scheduler] host=2xE5620 16T | active_shards=A,C,E | reserve=OS/CDP/Chromium/daemons | hb={HB} | shard_e_conformity_gate={SHARD_E_CONFORMITY_EVIDENCE}", flush=True)
    threads = [
        threading.Thread(target=loop, args=(name, cadence, job), daemon=True, name=f"shard-{name}")
        for name, cadence, job in SHARDS
    ]
    for t in threads:
        t.start()

    try:
        while not STOP.is_set():
            time.sleep(1)
    finally:
        STOP.set()
        for t in threads:
            t.join(timeout=5)
        print("[scheduler] stopped", flush=True)


if __name__ == "__main__":
    main()
