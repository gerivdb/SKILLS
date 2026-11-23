#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
preflight_sentinel.py — CDP Preflight Sentinel
Test de connectivité CDP (port 9222, Runtime.enable, Runtime.evaluate) en < 2s
avant tout envoi vers Gemini ou DeepSeek.
Usage: python preflight_sentinel.py [--target gemini|deepseek|auto] [--timeout-ms 2000]
"""
import asyncio
import json
import sys
import time
import urllib.request
import websockets
from typing import Optional, Dict, Any

CDP_HOST = "127.0.0.1"
CDP_PORT = 9222
CDP_VERSION_URL = f"http://{CDP_HOST}:{CDP_PORT}/json/version"
CDP_LIST_URL = f"http://{CDP_HOST}:{CDP_PORT}/json/list"

TARGET_CONFIGS = {
    "gemini": {"url_contains": "gemini.google.com", "title_contains": "Gemini"},
    "deepseek": {"url_contains": "chat.deepseek.com", "title_contains": "DeepSeek"},
    "auto": {"url_contains": "", "title_contains": ""},
}

TOTAL_TIMEOUT_MS = 2000


def http_get(url: str, timeout_ms: int) -> Dict[str, Any]:
    try:
        with urllib.request.urlopen(url, timeout=timeout_ms / 1000) as r:
            return {"ok": True, "data": json.loads(r.read().decode())}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def find_target_tab(tabs, target_config: Dict[str, str]) -> Optional[Dict]:
    for t in tabs:
        title = t.get("title", "") or ""
        url = t.get("url", "") or ""
        if target_config.get("url_contains") and target_config["url_contains"] not in url:
            continue
        if target_config.get("title_contains") and target_config["title_contains"] not in title:
            continue
        return t
    return None


async def cdp_send(ws, method: str, params=None, msg_id=1):
    """Envoie commande CDP et attend réponse (pattern original qui marche)."""
    msg = {"id": msg_id, "method": method, "params": params or {}}
    await ws.send(json.dumps(msg))
    while True:
        raw = await ws.recv()
        resp = json.loads(raw)
        if resp.get("id") == msg_id:
            return resp


async def preflight_check(target: str = "auto", timeout_ms: int = 2000) -> Dict[str, Any]:
    start_time = time.perf_counter()
    deadline = start_time + timeout_ms / 1000
    target_config = TARGET_CONFIGS.get(target, TARGET_CONFIGS["auto"])

    def time_left_ms():
        return max(0, int((deadline - time.perf_counter()) * 1000))

    # GESTE-1: Port CDP
    if time_left_ms() <= 0:
        return {"ok": False, "error": "Timeout before port check", "stage": "port", "latency_ms": int((time.perf_counter() - start_time) * 1000)}
    
    version_result = http_get(CDP_VERSION_URL, min(time_left_ms(), 1000))
    if not version_result["ok"]:
        return {"ok": False, "error": f"CDP port unreachable: {version_result['error']}", "stage": "port", "latency_ms": int((time.perf_counter() - start_time) * 1000)}

    # GESTE-2: List tabs
    if time_left_ms() <= 0:
        return {"ok": False, "error": "Timeout after port check", "stage": "port", "latency_ms": int((time.perf_counter() - start_time) * 1000)}
    
    tabs_result = http_get(CDP_LIST_URL, min(time_left_ms(), 1000))
    if not tabs_result["ok"]:
        return {"ok": False, "error": f"Tabs list failed: {tabs_result['error']}", "stage": "tabs", "latency_ms": int((time.perf_counter() - start_time) * 1000)}
    
    tabs = tabs_result["data"]
    tab = None
    for t in tabs:
        url = t.get("url", "") or ""
        title = t.get("title", "") or ""
        if target != "auto":
            if target == "gemini" and "gemini.google.com" not in url:
                continue
            if target == "deepseek" and "chat.deepseek.com" not in url:
                continue
        if "gemini.google.com" in url or "Gemini" in title:
            tab = t
            break
    if not tab:
        return {"ok": False, "error": "No target tab found", "stage": "tabs", "latency_ms": int((time.perf_counter() - start_time) * 1000)}

    # GESTE-3: WebSocket + Runtime.enable + Evaluate
    tab_id = tab["id"]
    ws_url = f"ws://127.0.0.1:9222/devtools/page/{tab_id}"
    
    if time_left_ms() <= 0:
        return {"ok": False, "error": "Timeout before WS connect", "stage": "ws", "latency_ms": int((time.perf_counter() - start_time) * 1000)}

    try:
        async with websockets.connect(ws_url, ping_interval=None, close_timeout=1) as ws:
            # Runtime.enable
            msg = {"id": 1, "method": "Runtime.enable"}
            await ws.send(json.dumps(msg))
            while True:
                raw = await ws.recv()
                resp = json.loads(raw)
                if resp.get("id") == 1:
                    break
            
            # Runtime.evaluate
            msg = {
                "id": 2,
                "method": "Runtime.evaluate",
                "params": {"expression": "'preflight_ok'", "returnByValue": True}
            }
            await ws.send(json.dumps(msg))
            while True:
                raw = await ws.recv()
                resp = json.loads(raw)
                if resp.get("id") == 2:
                    break
            
            result_val = resp.get("result", {}).get("result", {}).get("value", "")
            if result_val != "preflight_ok":
                return {"ok": False, "error": f"Evaluate returned unexpected: {result_val}", "stage": "evaluate", "latency_ms": int((time.perf_counter() - start_time) * 1000)}

    except asyncio.TimeoutError:
        return {"ok": False, "error": "WebSocket timeout", "stage": "ws", "latency_ms": int((time.perf_counter() - start_time) * 1000)}
    except Exception as e:
        return {"ok": False, "error": f"WS error: {e}", "stage": "ws", "latency_ms": int((time.perf_counter() - start_time) * 1000)}

    total_latency = int((time.perf_counter() - start_time) * 1000)
    return {
        "ok": True,
        "latency_ms": total_latency,
        "tab_id": tab["id"],
        "tab_title": tab.get("title"),
        "tab_url": tab.get("url")
    }


async def main():
    import argparse
    parser = argparse.ArgumentParser(description="CDP Preflight Sentinel - Test connectivité < 2s")
    parser.add_argument("--target", choices=["gemini", "deepseek", "auto"], default="auto")
    parser.add_argument("--timeout-ms", type=int, default=2000)
    args = parser.parse_args()

    start_time = time.perf_counter()
    result = await preflight_check(args.target, args.timeout_ms)
    result["total_latency_ms"] = int((time.perf_counter() - start_time) * 1000)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    import time
    sys.exit(asyncio.run(main()))