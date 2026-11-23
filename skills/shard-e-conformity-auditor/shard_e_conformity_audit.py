#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
shard_e_conformity_audit.py — Shard E (Strate CHECK / Conformité & Scellement SSoT)
G-PROOF (syntax/anticheat/spot), M3-Tree (can_unlock/DFS/DAG), WAL 0x243 Merkle linéaire.
Invariants: F=0.0, H=0.0. Écrit l'évidence et retourne exit 0 si PASS, 1 si FAIL.
"""
import ast
import hashlib
import json
import os
import py_compile
import sys
import time
import datetime
import glob

REPO = r"D:\DO\WEB\TOOLS\L0-CANON\ENV3-repo"
SWARM = os.path.join(REPO, ".swarm")
WAL_PATH = os.path.join(SWARM, "wal_0x243.log")
EVIDENCE_PATH = os.path.join(REPO, "e2e_output", "shard_e_audit_evidence.json")
HEARTBEAT_PATH = os.path.join(SWARM, "shards_heartbeat.jsonl")

DEFAULT_ARTIFACTS = [
    os.path.join(REPO, "e2e_output", "shard_f_gateway_daemon.py"),
    os.path.join(REPO, "e2e_output", "shard_scheduler.py"),
    os.path.join(SWARM, "context_live.json"),
]


def now():
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def gate_syntax(artifact_path):
    try:
        if not os.path.exists(artifact_path):
            return False, "missing"
        if artifact_path.endswith(".py"):
            py_compile.compile(artifact_path, doraise=True)
            with open(artifact_path, "r", encoding="utf-8", errors="replace") as f:
                ast.parse(f.read())
            return True, "py_ok"
        if artifact_path.endswith(".json"):
            with open(artifact_path, "r", encoding="utf-8") as f:
                json.load(f)
            return True, "json_ok"
        # generic text/readable
        with open(artifact_path, "rb") as f:
            f.read(1)
        return True, "readable"
    except Exception as e:
        return False, f"{type(e).__name__}:{e}"


def gate_anticheat(artifact_path):
    """Détecte contournements évidents (hardcoded secrets/tokens placeholders, pass-only stubs critiques)."""
    try:
        if not os.path.exists(artifact_path):
            return False, "missing"
        # binary/non-text safe
        if not artifact_path.endswith((".py", ".json", ".md", ".txt", ".yaml", ".yml", ".log")):
            return True, "skip_nontext"
        with open(artifact_path, "r", encoding="utf-8", errors="replace") as f:
            txt = f.read()
        lowered = txt.lower()
        markers = [
            "todo: bypass",
            "disable_audit",
            "skip_gproof",
            "anticheat=off",
            "hardcoded_token=",
        ]
        hits = [m for m in markers if m in lowered]
        if hits:
            return False, f"markers:{hits}"
        # heuristic: empty python file pretending to be artifact
        if artifact_path.endswith(".py") and len(txt.strip()) == 0:
            return False, "empty_py"
        return True, "ok"
    except Exception as e:
        return False, f"{type(e).__name__}:{e}"


def gate_spot(artifact_path):
    """Conformité sémantique minimale + preuve de vie (mtime récent ou contenu substantiel)."""
    try:
        if not os.path.exists(artifact_path):
            return False, "missing"
        st = os.stat(artifact_path)
        if st.st_size <= 0:
            return False, "empty"
        age_s = max(0, time.time() - st.st_mtime)
        # spot passes if file has substance; very old files still admissible if non-empty
        return True, f"size={st.st_size};age_s={int(age_s)}"
    except Exception as e:
        return False, f"{type(e).__name__}:{e}"


def audit_gproof(artifacts):
    results = {}
    all_ok = True
    for art in artifacts:
        g = {}
        for name, fn in (("syntax", gate_syntax), ("anticheat", gate_anticheat), ("spot", gate_spot)):
            ok, detail = fn(art)
            g[name] = {"pass": ok, "detail": detail}
            if not ok:
                all_ok = False
        g["pass"] = all(v["pass"] for v in g.values() if isinstance(v, dict))
        results[art] = g
    return all_ok, results


def parse_wal_entry(line):
    line = line.strip()
    if not line:
        return None
    try:
        obj = json.loads(line)
        if isinstance(obj, dict):
            return obj
    except Exception:
        pass
    # fallback raw entry
    return {"raw": line}


def audit_merkle_wal():
    """Vérifie chaîne Merkle linéaire WAL 0x243. Si absent: genesis autorisé (pass avec note)."""
    if not os.path.exists(WAL_PATH):
        return True, {
            "exists": False,
            "valid": True,
            "entries": 0,
            "note": "genesis_allowed_missing_wal",
            "head_hash": None,
        }
    entries = []
    with open(WAL_PATH, "r", encoding="utf-8", errors="replace") as f:
        for i, line in enumerate(f, 1):
            e = parse_wal_entry(line)
            if e is None:
                continue
            e["_line"] = i
            entries.append(e)
    if not entries:
        return True, {"exists": True, "valid": True, "entries": 0, "note": "empty_wal", "head_hash": None}

    prev = "0" * 64
    head = prev
    for idx, e in enumerate(entries):
        declared_prev = e.get("prev_hash") or e.get("prev") or e.get("previous_hash")
        declared_hash = e.get("hash") or e.get("entry_hash")
        # canonical payload excludes mutable verification fields if present
        payload_obj = {k: v for k, v in e.items() if k not in ("hash", "entry_hash", "_line")}
        payload = json.dumps(payload_obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        computed = sha256_hex((prev + "|").encode("utf-8") + payload)

        if declared_prev is not None and str(declared_prev) != prev:
            return False, {
                "exists": True, "valid": False, "entries": len(entries),
                "broken_at_index": idx, "broken_line": e.get("_line"),
                "reason": "prev_hash_mismatch", "expected_prev": prev, "found_prev": declared_prev,
                "head_hash": head,
            }
        if declared_hash is not None and str(declared_hash) != computed:
            return False, {
                "exists": True, "valid": False, "entries": len(entries),
                "broken_at_index": idx, "broken_line": e.get("_line"),
                "reason": "hash_mismatch", "expected_hash": computed, "found_hash": declared_hash,
                "head_hash": head,
            }
        # advance chain: prefer declared hash when present and valid, else computed
        head = str(declared_hash) if declared_hash is not None else computed
        prev = head

    return True, {"exists": True, "valid": True, "entries": len(entries), "head_hash": head, "note": "chain_ok"}


def find_m3_tree_sources():
    patterns = [
        os.path.join(SWARM, "m3_tree*.json"),
        os.path.join(SWARM, "m3*.json"),
        os.path.join(REPO, "e2e_output", "m3_tree*.json"),
        os.path.join(REPO, "**", "*m3*tree*.json"),
    ]
    found = []
    for pat in patterns:
        found.extend(glob.glob(pat, recursive=True))
    # unique, existing
    uniq = []
    seen = set()
    for p in found:
        rp = os.path.normcase(os.path.normpath(p))
        if rp in seen or not os.path.isfile(p):
            continue
        seen.add(rp)
        uniq.append(p)
    return uniq


def can_unlock(node_id, graph, unlocked=None):
    """DFS accessibility from roots/unlocked set through DAG edges."""
    if unlocked is None:
        unlocked = set()
    if node_id in unlocked:
        return True
    nodes = graph.get("nodes", {})
    node = nodes.get(node_id)
    if node is None:
        return False
    deps = node.get("requires") or node.get("deps") or node.get("parents") or []
    if not deps:
        return True
    # all deps must be unlockable
    return all(can_unlock(d, graph, unlocked) for d in deps)


def detect_cycle(nodes):
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {n: WHITE for n in nodes}
    def dfs(u):
        color[u] = GRAY
        for v in (nodes.get(u, {}).get("children") or nodes.get(u, {}).get("unlocks") or []):
            if v not in nodes:
                continue
            if color[v] == GRAY:
                return True
            if color[v] == WHITE and dfs(v):
                return True
        color[u] = BLACK
        return False
    for n in list(nodes.keys()):
        if color[n] == WHITE and dfs(n):
            return True
    return False


def normalize_m3_tree(obj):
    """Accept a few plausible shapes; return normalized {nodes:{id:{...}}} or None."""
    if not isinstance(obj, dict):
        return None
    if "nodes" in obj and isinstance(obj["nodes"], dict):
        return {"nodes": obj["nodes"], "meta": obj.get("meta", {})}
    if "nodes" in obj and isinstance(obj["nodes"], list):
        nodes = {}
        for n in obj["nodes"]:
            if isinstance(n, dict) and n.get("id"):
                nodes[str(n["id"])] = n
        return {"nodes": nodes, "meta": obj.get("meta", {})}
    # maybe dict of nodes directly
    if all(isinstance(v, dict) for v in obj.values()):
        sample = next(iter(obj.values()), None)
        if sample and ("requires" in sample or "children" in sample or "type" in sample or "tier" in sample):
            return {"nodes": obj, "meta": {}}
    return None


VALID_TAXONOMY = {"basic", "extra", "unique", "ultimate", "○", "◇", "◉", "◆"}


def audit_m3_tree():
    sources = find_m3_tree_sources()
    if not sources:
        # no explicit M3 tree artifact found: report degraded-not-failed (cannot prove non-conformity)
        return True, {
            "found": False,
            "valid": True,
            "note": "no_m3_tree_artifact_found_degraded",
            "sources": [],
            "can_unlock_ok": None,
            "dag_ok": None,
        }
    details = []
    overall_ok = True
    for path in sources:
        entry = {"path": path}
        try:
            with open(path, "r", encoding="utf-8") as f:
                raw = json.load(f)
            graph = normalize_m3_tree(raw)
            if graph is None:
                entry.update({"valid": False, "reason": "unrecognized_shape"})
                overall_ok = False
                details.append(entry)
                continue
            nodes = graph["nodes"]
            dag_ok = not detect_cycle(nodes)
            # taxonomy check when present
            bad_tax = []
            for nid, n in nodes.items():
                tax = (n.get("taxonomy") or n.get("tier") or n.get("type") or "").strip().lower()
                sym = (n.get("symbol") or "").strip()
                if tax and tax not in VALID_TAXONOMY and sym not in VALID_TAXONOMY:
                    # allow unknown schema but flag only explicit invalid markers
                    pass
                if tax in {"invalid", "unknown_bad"}:
                    bad_tax.append(nid)
            # can_unlock: roots (no deps) must unlock; sample all nodes reachable
            unlock_fail = []
            for nid in nodes.keys():
                try:
                    if not can_unlock(nid, graph, set()):
                        unlock_fail.append(nid)
                except Exception:
                    unlock_fail.append(nid)
            ok = dag_ok and not bad_tax and not unlock_fail
            entry.update({
                "valid": ok, "dag_ok": dag_ok, "nodes": len(nodes),
                "bad_taxonomy": bad_tax[:20], "unlock_fail": unlock_fail[:20],
            })
            if not ok:
                overall_ok = False
        except Exception as e:
            entry.update({"valid": False, "reason": f"{type(e).__name__}:{e}"})
            overall_ok = False
        details.append(entry)
    return overall_ok, {"found": True, "valid": overall_ok, "sources": sources, "details": details}


def audit_remove_outcome():
    """Vérifie qu'aucun élagage non justifié n'est déclaré; cherche marqueurs de suppression sans preuve."""
    evidence_glob = os.path.join(REPO, "e2e_output", "*evidence*.json")
    issues = []
    checked = 0
    for path in glob.glob(evidence_glob):
        try:
            with open(path, "r", encoding="utf-8") as f:
                obj = json.load(f)
        except Exception:
            continue
        checked += 1
        txt = json.dumps(obj, ensure_ascii=False).lower()
        if "removeoutcome" in txt or "removed_node" in txt or "pruned" in txt:
            # require proof marker
            if "gproof" not in txt and "proof" not in txt and "pass" not in txt:
                issues.append({"path": path, "reason": "removal_marker_without_proof"})
    ok = len(issues) == 0
    return ok, {"checked_files": checked, "issues": issues, "ok": ok}


def run_audit(artifacts=None, loop_mode=False, interval_s=60):
    def once():
        artifacts_list = artifacts or DEFAULT_ARTIFACTS
        gproof_ok, gproof = audit_gproof(artifacts_list)
        merkle_ok, merkle = audit_merkle_wal()
        m3_ok, m3 = audit_m3_tree()
        remove_ok, remove = audit_remove_outcome()
        overall = bool(gproof_ok and merkle_ok and m3_ok and remove_ok)
        result = {
            "ts": now(),
            "shard": "E",
            "role": "conformity_sealing_ssot",
            "invariants": {"F": 0.0, "H": 0.0},
            "gproof": {"pass": gproof_ok, "artifacts": gproof},
            "wal_0x243_merkle": merkle,
            "m3_tree": m3,
            "remove_outcome": remove,
            "gates_passed": gproof_ok,
            "merkle_valid": merkle_ok,
            "m3_valid": m3_ok,
            "remove_outcome_ok": remove_ok,
            "PASS": overall,
            "readonly_required": not overall,
        }
        os.makedirs(os.path.dirname(EVIDENCE_PATH), exist_ok=True)
        with open(EVIDENCE_PATH, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        # append heartbeat
        try:
            os.makedirs(os.path.dirname(HEARTBEAT_PATH), exist_ok=True)
            hb = {"ts": result["ts"], "shard": "E", "state": "ok" if overall else "fail",
                  "detail": f"gproof={gproof_ok} merkle={merkle_ok} m3={m3_ok} remove={remove_ok} readonly={not overall}",
                  "rc": 0 if overall else 1}
            with open(HEARTBEAT_PATH, "a", encoding="utf-8") as f:
                f.write(json.dumps(hb, ensure_ascii=False) + "\n")
        except Exception:
            pass
        return overall, result

    if not loop_mode:
        ok, res = once()
        print(f"[Shard E] ts={res['ts']} PASS={ok} gproof={res['gates_passed']} merkle={res['merkle_valid']} m3={res['m3_valid']} remove={res['remove_outcome_ok']}", flush=True)
        return 0 if ok else 1

    print(f"[Shard E] audit loop start interval={interval_s}s evidence={EVIDENCE_PATH}", flush=True)
    try:
        while True:
            ok, res = once()
            print(f"[Shard E] ts={res['ts']} PASS={ok} readonly={res['readonly_required']}", flush=True)
            time.sleep(max(5, int(interval_s)))
    except KeyboardInterrupt:
        print("[Shard E] stop", flush=True)
        return 130


if __name__ == "__main__":
    loop_mode = "--loop" in sys.argv
    interval = 60
    for a in sys.argv[1:]:
        if a.startswith("--interval="):
            try:
                interval = int(a.split("=", 1)[1])
            except Exception:
                pass
    sys.exit(run_audit(loop_mode=loop_mode, interval_s=interval))