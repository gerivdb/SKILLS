# cdp_sniffer_extra_info.py — Capture requestWillBeSentExtraInfo (headers réels)
import json, sys, time, urllib.request, websocket

CDP = "http://127.0.0.1:9222"
TARGET = "/api/v0/chat/completion"
OUT = r"D:\DO\WEB\TOOLS\L0-CANON\ENV3-repo\e2e_output\captured_extra_info.json"

def main():
    tabs = json.loads(urllib.request.urlopen(CDP + "/json/list").read())
    tab = next((t for t in tabs if "chat.deepseek.com" in t.get("url", "")), None)
    if not tab:
        print("ERREUR: pas d'onglet DeepSeek."); return 1

    ws = websocket.create_connection(tab["webSocketDebuggerUrl"], suppress_origin=True, timeout=300)
    ws.send(json.dumps({"id": 1, "method": "Network.enable"}))
    ws.recv()
    print("[ExtraInfo] Network activé. Envoie un message dans DeepSeek maintenant...")

    request_id_to_url = {}
    captured = None
    deadline = time.time() + 300

    while time.time() < deadline:
        try:
            msg = json.loads(ws.recv())
        except websocket.WebSocketTimeoutException:
            break

        method = msg.get("method")
        params = msg.get("params", {})

        if method == "Network.requestWillBeSent":
            rid = params.get("requestId")
            url = params.get("request", {}).get("url", "")
            if TARGET in url:
                request_id_to_url[rid] = url
                print(f"[ExtraInfo] Requête cible détectée: {rid}")

        elif method == "Network.requestWillBeSentExtraInfo":
            rid = params.get("requestId")
            if rid in request_id_to_url:
                headers = params.get("headers", {})
                associated_cookies = params.get("associatedCookies", [])
                captured = {
                    "url": request_id_to_url[rid],
                    "headers": headers,
                    "associatedCookies": associated_cookies,
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")
                }
                print("\n" + "="*60)
                print("[CAPTURE] ExtraInfo:")
                print("HEADERS RÉELS:")
                for k, v in headers.items():
                    if k.lower() in ("authorization", "cookie", "x-ds-pow-response", "x-ds-pow", "x-client-*"):
                        print(f"  >>> {k}: {v[:200]}")
                    else:
                        print(f"  {k}: {str(v)[:120]}")
                print(f"COOKIES: {len(associated_cookies)} associés")
                for c in associated_cookies[:5]:
                    print(f"  {c.get('cookie', {}).get('name')}: blocked={c.get('blockedReasons')}")
                print("="*60)
                break

    ws.close()

    if captured:
        with open(OUT, "w", encoding="utf-8") as f:
            json.dump(captured, f, indent=2, ensure_ascii=False)
        print(f"[ExtraInfo] Sauvegardé: {OUT}")
        # Détection de headers suspects
        h = {k.lower(): v for k, v in captured["headers"].items()}
        if "authorization" in h:
            print(f"[ExtraInfo] AUTHENTIFICATION TROUVÉE: Authorization présent")
        if any("pow" in k.lower() for k in h):
            print(f"[ExtraInfo] POW TROUVÉ: {[k for k in h if 'pow' in k.lower()]}")
        if not captured["associatedCookies"]:
            print(f"[ExtraInfo] ATTENTION: aucun cookie associé — API n'utilise pas les cookies")
    else:
        print("[ExtraInfo] Pas de capture. Réessaie en envoyant un message.")
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())