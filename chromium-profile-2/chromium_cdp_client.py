#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
chromium_cdp_client.py — Skill chromium-profile-2
Client CDP basé sur cdp-use pour le profil 2 de Chromium.

Architecture CDP respectée :
  • Commandes de niveau Browser (Browser.getVersion, Target.*)  -> endpoint /devtools/browser/<guid>
  • Commandes de niveau Page/DOM/Runtime/Input                   -> endpoint /devtools/page/<page_id>
    via attach_to_tab(target_id) qui reconnecte le client sur l'URL de la page.

Blocage connu :
  Le WebSocket CDP est refusé (403 Forbidden) si Chromium a été lancé sans
  --remote-allow-origins=*. Relancer Chromium avec ce flag pour activer
  send/navigate/click/etc.
"""

from __future__ import annotations

import asyncio
import importlib
import json
import os
import queue
import sqlite3
import subprocess
import sys
import threading
import time
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path
from typing import Any, Dict, List, Optional

import websockets

from cdp_use import CDPClient

# ---------------------------------------------------------------------------
# Constantes — Profil 2 (source de vérité)
# ---------------------------------------------------------------------------
CHROMIUM_EXE = r"C:\Users\GG\AppData\Local\Chromium\Application\chrome.exe"
USER_DATA_DIR = r"C:\Users\GG\AppData\Local\Chromium\User Data"
PROFILE_DIR = "Profile 2"
PROFILE_PATH = os.path.join(USER_DATA_DIR, PROFILE_DIR)
DEBUG_PORT = 9222
DEBUG_HOST = "127.0.0.1"

BOOKMARKS_FILE = os.path.join(PROFILE_PATH, "Bookmarks")
HISTORY_FILE = os.path.join(PROFILE_PATH, "History")
EXTENSIONS_DIR = os.path.join(PROFILE_PATH, "Extensions")


class ChromiumCDPClient:
    """Client CDP asynchrone basé sur cdp-use pour le profil 2 de Chromium."""

    def __init__(self, host: str = DEBUG_HOST, port: int = DEBUG_PORT):
        self.host = host
        self.port = port
        self._ws = None                      # WebSocket persistant (session pooling) — endpoint Browser
        self._ws_url: Optional[str] = None   # URL du WebSocket CDP (Browser)
        self._page_ws = None                 # WebSocket persistant — endpoint Page (pour Runtime/DOM/Page)
        self._page_ws_url: Optional[str] = None
        self._page_tab_id: Optional[str] = None
        self._client: Optional[CDPClient] = None
        self._active_tab_id: Optional[str] = None
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._tab_ws_urls: Dict[str, str] = {}
        self._msg_id = 0                     # Compteur d'ID JSON-RPC
        self._session_ids: Dict[str, str] = {}  # tab_id -> sessionId (Target.attachToTarget flatten)
        self._event_queue: "queue.Queue[str]" = queue.Queue()  # Événements CDP reçus
        self._event_thread: Optional[threading.Thread] = None  # Thread d'écoute événements
        self._page_ws_events = None          # WebSocket dédié aux événements (séparé des requêtes)
        self._event_listener_running = False # Flag d'arrêt du listener

    # Domaines CDP de niveau Page (disponibles uniquement sur /devtools/page/<id>)
    # "Page" est EXCLU car Page.navigate fonctionne sur l'endpoint Browser.
    PAGE_DOMAINS = frozenset({
        "Runtime", "DOM", "Input", "Network", "CSS", "Overlay",
        "Emulation", "LayerTree", "Log", "Animation", "Accessibility",
        "Performance", "Profiler", "Security", "Storage", "Debugger",
        "HeapProfiler", "Inspector", "Tracing", "Worker", "Fetch",
    })

    # ------------------------------------------------------------------ cycle
    def start_browser(self) -> Dict[str, Any]:
        try:
            with urllib.request.urlopen(f"http://{self.host}:{self.port}/json/version", timeout=2):
                return {"status": "already_running", "port": self.port}
        except Exception:
            pass
        subprocess.Popen(
            [
                CHROMIUM_EXE,
                f"--user-data-dir={USER_DATA_DIR}",
                f"--profile-directory={PROFILE_DIR}",
                f"--remote-debugging-port={self.port}",
                "--remote-allow-origins=*",
            ],
            cwd=os.path.dirname(CHROMIUM_EXE),
        )
        deadline = time.time() + 15
        while time.time() < deadline:
            try:
                with urllib.request.urlopen(f"http://{self.host}:{self.port}/json/version", timeout=2):
                    return {"status": "started", "port": self.port}
            except Exception:
                time.sleep(0.5)
        raise TimeoutError(f"Chromium n'a pas initialisé le port {self.port}")

    def stop_browser(self) -> Dict[str, Any]:
        raise NotImplementedError(
            "stop_browser est desactive : ne jamais tuer une session utilisateur ouverte."
        )

    def get_status(self) -> Dict[str, Any]:
        tabs = self.list_tabs()
        ws_ok = self._test_websocket()
        return {
            "port": self.port,
            "tabs_open": len(tabs),
            "websocket_cdp": ws_ok,
            "tabs": tabs,
        }

    def _test_websocket(self) -> bool:
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            ws_url = self._discover_ws_url()
            client = CDPClient(url=ws_url)
            loop.run_until_complete(client.start())
            loop.run_until_complete(client.stop())
            loop.close()
            return True
        except Exception:
            return False

    def _discover_ws_url(self) -> str:
        if self._active_tab_id:
            if self._active_tab_id in self._tab_ws_urls:
                return self._tab_ws_urls[self._active_tab_id]
            tabs = self.list_tabs()
            for t in tabs:
                if t["id"] == self._active_tab_id and t.get("webSocketDebuggerUrl"):
                    self._tab_ws_urls[self._active_tab_id] = t["webSocketDebuggerUrl"]
                    return self._tab_ws_urls[self._active_tab_id]
            raise RuntimeError(
                f"Onglet {self._active_tab_id} n'a pas encore d'URL de debug WebSocket. "
                "Attendez que la page charge."
            )
        with urllib.request.urlopen(f"http://{self.host}:{self.port}/json/version", timeout=5) as r:
            version_info = json.loads(r.read().decode())
        ws_url = version_info.get("webSocketDebuggerUrl")
        if not ws_url:
            raise RuntimeError(
                f"Aucune webSocketDebuggerUrl retournée par {self.host}:{self.port}/json/version"
            )
        return ws_url

    def attach_to_tab(self, target_id: str) -> Dict[str, Any]:
        tabs = self.list_tabs()
        for t in tabs:
            if t["id"] == target_id:
                self._active_tab_id = target_id
                if t.get("webSocketDebuggerUrl"):
                    self._tab_ws_urls[target_id] = t["webSocketDebuggerUrl"]
                self._client = None
                return {
                    "targetId": target_id,
                    "title": t.get("title"),
                    "url": t.get("url"),
                    "webSocketDebuggerUrl": t.get("webSocketDebuggerUrl"),
                }
        raise RuntimeError(f"Onglet {target_id} introuvable dans /json/list")

    def _get_loop(self) -> asyncio.AbstractEventLoop:
        if self._loop is None or self._loop.is_closed():
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
        return self._loop

    def _ensure_connected(self):
        """Ouvre (ou réutilise) un WebSocket persistant vers Chromium CDP."""
        if self._ws is not None:
            try:
                # Vérifier que la socket est encore vivante avec un ping léger
                loop = self._get_loop()
                loop.run_until_complete(self._ws.ping())
                return self._ws
            except Exception:
                # Socket morte : fermer et recréer
                try:
                    loop.run_until_complete(self._ws.close())
                except Exception:
                    pass
                self._ws = None
                self._ws_url = None

        loop = self._get_loop()
        ws_url = self._discover_ws_url()
        self._ws = loop.run_until_complete(websockets.connect(ws_url))
        self._ws_url = ws_url
        return self._ws

    def _ensure_page_connected(self, tab_id: Optional[str] = None) -> Optional[str]:
        """
        Attache un sessionId stable à l'onglet cible via Target.attachToTarget (flatten: true)
        sur la connexion WebSocket Browser existante (self._ws).
        Le sessionId est capturé depuis l'événement Target.attachedToTarget (dispatché sur
        la connexion Browser quand flatten: true).
        Retourne le sessionId à utiliser dans les params des commandes de domaine Page.
        """
        target_id = tab_id or self._active_tab_id
        if not target_id:
            return None

        # Si on a déjà un sessionId pour cet onglet, le réutiliser
        if target_id in self._session_ids:
            return self._session_ids[target_id]

        ws = self._ensure_connected()  # connexion Browser persistante
        loop = self._get_loop()
        msg_id = self._next_id()
        message = json.dumps({
            "id": msg_id,
            "method": "Target.attachToTarget",
            "params": {
                "targetId": target_id,
                "flatten": True,
            },
        })

        def _do_attach():
            return loop.run_until_complete(self._ws_send_recv(ws, message))

        try:
            response_str = _do_attach()
        except websockets.ConnectionClosed:
            try:
                loop.run_until_complete(ws.close())
            except Exception:
                pass
            self._ws = None
            ws = self._ensure_connected()
            response_str = _do_attach()

        # La réponse directe ne contient PAS le sessionId (flatten: true l'envoie
        # comme événement Target.attachedToTarget sur la connexion Browser).
        # On démarre un listener temporaire sur self._ws pour le capturer.
        session_id = self._capture_attached_session(target_id, timeout=5.0)

        if session_id:
            self._session_ids[target_id] = session_id
            return session_id

        return None

    def _capture_attached_session(self, target_id: str, timeout: float = 5.0) -> Optional[str]:
        """
        Écoute l'événement Target.attachedToTarget sur la connexion Browser
        pour extraire le sessionId. Utilise un thread dédié avec une boucle
        asyncio sur self._ws.
        """
        if self._ws is None:
            return None

        captured: list[str] = []

        async def _listen():
            try:
                while self._ws.open:
                    try:
                        msg = await asyncio.wait_for(self._ws.recv(), timeout=timeout)
                        evt = json.loads(msg)
                        if evt.get("method") == "Target.attachedToTarget":
                            params = evt.get("params", {})
                            if params.get("targetInfo", {}).get("targetId") == target_id:
                                captured.append(params.get("sessionId", ""))
                                return
                    except asyncio.TimeoutError:
                        return
                    except Exception:
                        continue
            except Exception:
                pass

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(_listen())
        finally:
            loop.close()

        return captured[0] if captured else None

    # ------------------------------------------------------------------ événements CDP (Event-driven navigation)
    def _event_listener_coro(self, ws_url: str):
        """Coroutine d'écoute des événements CDP sur le WebSocket Page."""
        async def _run():
            try:
                async with websockets.connect(ws_url) as ws:
                    # Activer le domaine Page pour recevoir loadEventFired
                    enable_msg = json.dumps({
                        "id": 0,
                        "method": "Page.enable",
                        "params": {},
                    })
                    await ws.send(enable_msg)
                    await ws.recv()  # consommation de la réponse à Page.enable

                    while self._event_listener_running:
                        try:
                            msg = await asyncio.wait_for(ws.recv(), timeout=1.0)
                            self._event_queue.put(msg)
                        except asyncio.TimeoutError:
                            continue
            except Exception:
                pass

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(_run())
        loop.close()

    def _start_event_listener(self, tab_id: str) -> None:
        """Démarre un thread dédié à l'écoute des événements CDP de l'onglet."""
        self._stop_event_listener()  # s'assurer qu'aucun listener n'est déjà actif

        # Récupérer l'URL WebSocket de l'onglet
        page_url = self._tab_ws_urls.get(tab_id)
        if not page_url:
            tabs = self.list_tabs()
            for t in tabs:
                if t["id"] == tab_id and t.get("webSocketDebuggerUrl"):
                    page_url = t["webSocketDebuggerUrl"]
                    break
        if not page_url:
            return

        self._event_listener_running = True
        self._event_thread = threading.Thread(
            target=self._event_listener_coro,
            args=(page_url,),
            daemon=True,
        )
        self._event_thread.start()

    def _stop_event_listener(self) -> None:
        """Arrête le thread d'écoute des événements."""
        self._event_listener_running = False
        if self._event_thread is not None and self._event_thread.is_alive():
            self._event_thread.join(timeout=2.0)
        self._event_thread = None
        # Vider la queue
        try:
            while True:
                self._event_queue.get_nowait()
        except queue.Empty:
            pass

    def _wait_for_event(self, event_method: str, timeout: float = 10.0) -> Optional[Dict[str, Any]]:
        """Attend un événement CDP spécifique depuis la queue."""
        deadline = time.perf_counter() + timeout
        while time.perf_counter() < deadline:
            try:
                raw = self._event_queue.get(timeout=0.3)
                evt = json.loads(raw)
                if evt.get("method") == event_method:
                    return evt
            except queue.Empty:
                continue
            except json.JSONDecodeError:
                continue
        return None

    # ------------------------------------------------------------------ navigation
    async def _ws_send_recv(self, ws, message: str, timeout: float = 10.0) -> str:
        await ws.send(message)
        return await asyncio.wait_for(ws.recv(), timeout=timeout)

    def _next_id(self) -> int:
        self._msg_id += 1
        return self._msg_id

    def _generate_dynamic_method(self, domain: str, method: str) -> None:
        """
        Génère un wrapper Python dans dynamic_methods.py pour la méthode CDP
        qui a retourné -32601 (Method Not Found). Le wrapper appelle
        client.send(domain, method, params) et retourne le résultat brut.
        """
        dynamic_path = Path(__file__).resolve().parent / "dynamic_methods.py"
        func_name = f"{domain.lower()}_{method}"

        wrapper = f'''
def {func_name}(client, **params):
    """Wrapper auto-généré pour CDP {domain}.{method} (Méthode introuvable)."""
    return client.send("{domain}", "{method}", params)
'''

        mode = "a" if dynamic_path.exists() else "w"
        with open(dynamic_path, mode, encoding="utf-8") as f:
            if mode == "w":
                f.write("# -*- coding: utf-8 -*-\n")
                f.write("# Méthodes CDP auto-générées (auto-guérison Pilier 4)\n")
                f.write("# Générées dynamiquement suite à des erreurs -32601.\n\n")
            f.write(wrapper)

    def send(self, domain: str, method: str, params: Optional[Dict[str, Any]] = None) -> Any:
        # Routage par domaine : Page DOMAINS -> connexion Browser avec sessionId
        # (Target.attachToTarget flatten: true). Autres domaines -> connexion Browser directe.
        session_id = None
        if domain in self.PAGE_DOMAINS:
            session_id = self._ensure_page_connected(self._active_tab_id)
            if session_id is None:
                return {"error": {"code": -32603, "message": "Impossible d'attacher à la page"}}
        ws = self._ensure_connected()  # toujours la connexion Browser persistante
        loop = self._get_loop()
        msg_id = self._next_id()
        final_params = dict(params or {})
        if session_id:
            final_params["sessionId"] = session_id
        message = json.dumps({
            "id": msg_id,
            "method": f"{domain}.{method}",
            "params": final_params,
        })

        def _do_send():
            return loop.run_until_complete(self._ws_send_recv(ws, message))

        try:
            response_str = _do_send()
        except websockets.ConnectionClosed:
            # Auto-reconnect : fermer la socket morte et en ouvrir une nouvelle
            try:
                loop.run_until_complete(ws.close())
            except Exception:
                pass
            if domain in self.PAGE_DOMAINS:
                self._page_ws = None
                ws = self._ensure_page_connected(self._active_tab_id)
            else:
                self._ws = None
                ws = self._ensure_connected()
            response_str = _do_send()
        except asyncio.TimeoutError:
            # Chromium n'a pas répondu dans le délai : retour d'erreur structurée
            return {
                "id": msg_id,
                "error": {"code": -32800, "message": "CDP response timeout"},
            }

        response = json.loads(response_str)

        # Auto-guérison Pilier 4 : catch -32601 (Method Not Found)
        if isinstance(response, dict) and response.get("error", {}).get("code") == -32601:
            self._generate_dynamic_method(domain, method)
            # Recharger le module dynamique si présent
            dyn_path = Path(__file__).resolve().parent / "dynamic_methods.py"
            if str(dyn_path.parent) not in sys.path:
                sys.path.insert(0, str(dyn_path.parent))
            try:
                import dynamic_methods as _dm
                importlib.reload(_dm)
            except Exception:
                pass
            # Ré-exécuter la commande (retournera l'erreur de Chromium ou le résultat)
            response_str = _do_send()
            response = json.loads(response_str)

        return response

    def close_ws(self) -> None:
        """Ferme explicitement les WebSockets persistants (Browser + Page)."""
        if self._ws is not None:
            try:
                loop = self._get_loop()
                loop.run_until_complete(self._ws.close())
            except Exception:
                pass
            self._ws = None
            self._ws_url = None
        if self._page_ws is not None:
            try:
                loop = self._get_loop()
                loop.run_until_complete(self._page_ws.close())
            except Exception:
                pass
            self._page_ws = None
            self._page_ws_url = None
            self._page_tab_id = None
        self._stop_event_listener()

    async def disconnect_async(self) -> None:
        self.close_ws()
        self._client = None

    def disconnect(self) -> None:
        try:
            self.close_ws()
        except Exception:
            pass
        self._client = None

    # ------------------------------------------------------------------- tabs
    def _http(self, method: str, path: str, data: Optional[dict] = None) -> Any:
        url = f"http://{self.host}:{self.port}{path}"
        if method == "GET":
            with urllib.request.urlopen(url, timeout=5) as r:
                return json.loads(r.read().decode())
        elif method == "PUT":
            body = json.dumps(data or {}).encode()
            req = urllib.request.Request(url, data=body, method="PUT")
            with urllib.request.urlopen(req, timeout=5) as r:
                return json.loads(r.read().decode())
        elif method == "DELETE":
            req = urllib.request.Request(url, method="DELETE")
            try:
                with urllib.request.urlopen(req, timeout=5) as r:
                    body = r.read().decode()
                if body.strip():
                    try:
                        return json.loads(body)
                    except json.JSONDecodeError:
                        return {"status": "ok", "raw": body[:200]}
                return {"status": "ok"}
            except urllib.error.HTTPError as e:
                return {"status": "error", "code": e.code, "msg": e.read().decode(errors="ignore")}
        raise ValueError(f"Methode HTTP non supportee : {method}")

    def open_tab(self, url: str = "about:blank") -> Dict[str, Any]:
        encoded = urllib.parse.quote(url)
        result = self._http("PUT", f"/json/new?url={encoded}")
        target_id = result.get("id")
        self._active_tab_id = target_id
        if result.get("webSocketDebuggerUrl"):
            self._tab_ws_urls[target_id] = result["webSocketDebuggerUrl"]
        return {
            "targetId": target_id,
            "title": result.get("title"),
            "url": result.get("url"),
            "type": result.get("type"),
            "webSocketDebuggerUrl": result.get("webSocketDebuggerUrl"),
        }

    def close_tab(self, target_id: str) -> Dict[str, Any]:
        result = self._http("DELETE", f"/json/close/{target_id}")
        if self._active_tab_id == target_id:
            self._active_tab_id = None
        return result

    def list_tabs(self) -> List[Dict[str, Any]]:
        data = self._http("GET", "/json/list")
        return [
            {
                "id": t.get("id"),
                "title": t.get("title"),
                "url": t.get("url"),
                "type": t.get("type"),
            }
            for t in data
        ]

    def switch_tab(self, target_id: str) -> Dict[str, Any]:
        return self.send("Target", "activateTarget", {"targetId": target_id})

    # ------------------------------------------------------------- navigation
    def navigate(self, url: str) -> Any:
        """
        Navigation event-driven : envoie Page.navigate puis attend l'événement
        Page.loadEventFired (événement CDP natif) avant de retourner.
        Retourne un dict avec le statut et le temps mesuré.
        """
        tab_id = self._active_tab_id
        if tab_id is None:
            raise RuntimeError("Aucun onglet actif. Appelez open_tab() avant navigate().")

        # 1. Démarrer le listener d'événements CDP pour cet onglet
        self._start_event_listener(tab_id)

        # 2. Envoyer Page.navigate
        nav_result = self.send("Page", "navigate", {"url": url})

        # 3. Attendre Page.loadEventFired (événement natif, pas de sleep)
        load_event = self._wait_for_event("Page.loadEventFired", timeout=15.0)

        # 4. Arrêter le listener une fois la page chargée
        self._stop_event_listener()

        return {
            "navigate_response": nav_result,
            "load_event": load_event,
            "loaded": load_event is not None,
        }

    def go_back(self) -> Any:
        return self.send("Page", "goBack")

    def go_forward(self) -> Any:
        return self.send("Page", "goForward")

    def reload(self) -> Any:
        return self.send("Page", "reload")

    def stop_loading(self) -> Any:
        return self.send("Page", "stopLoading")

    # ------------------------------------------------------------- interaction
    def read_dom(self, selector: str) -> Any:
        return self.send("Runtime", "evaluate", {
            "expression": (
                "(function(){"
                f"const el=document.querySelector('{selector}');"
                "if(!el)return null;"
                "return el.textContent;"
                "})()"
            ),
            "returnByValue": True,
        })

    def click(self, selector: str) -> Any:
        return self.send("Input", "dispatchMouseEvent", {
            "type": "mousePressed",
            "x": 0, "y": 0, "button": "left", "clickCount": 1,
        })

    def type(self, selector: str, text: str) -> Any:
        return self.send("Input", "insertText", {"text": text})

    def evaluate_js(self, script: str) -> Any:
        return self.send("Runtime", "evaluate", {
            "expression": script,
            "returnByValue": True,
        })

    def screenshot(self) -> str:
        return self.send("Page", "captureScreenshot", {})

    # ------------------------------------------------------------- donnees
    def get_bookmarks(self) -> Dict[str, Any]:
        if not os.path.exists(BOOKMARKS_FILE):
            return {"status": "absent", "bookmarks": []}
        with open(BOOKMARKS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        roots = data.get("roots", {})
        bookmarks = []

        def walk(node):
            if isinstance(node, dict):
                if node.get("type") == "url":
                    bookmarks.append({
                        "name": node.get("name"),
                        "url": node.get("url"),
                        "date_added": node.get("date_added"),
                    })
                for child in node.get("children", []):
                    walk(child)

        for root in roots.values():
            if isinstance(root, dict):
                walk(root)
        return {"status": "ok", "count": len(bookmarks), "bookmarks": bookmarks}

    def get_history(self) -> Dict[str, Any]:
        if not os.path.exists(HISTORY_FILE):
            return {"status": "absent", "history": []}
        uri = f"file:{HISTORY_FILE}?mode=ro"
        try:
            conn = sqlite3.connect(uri, uri=True)
            cur = conn.cursor()
            cur.execute(
                "SELECT url, title, visit_count, last_visit_time FROM urls "
                "ORDER BY last_visit_time DESC LIMIT 50"
            )
            rows = cur.fetchall()
            conn.close()
            return {
                "status": "ok",
                "count": len(rows),
                "history": [
                    {"url": r[0], "title": r[1], "visit_count": r[2], "last_visit_time": r[3]}
                    for r in rows
                ],
            }
        except Exception as e:
            return {"status": "error", "error": str(e), "history": []}

    def scan_extensions(self) -> Dict[str, Any]:
        if not os.path.isdir(EXTENSIONS_DIR):
            return {"status": "absent", "extensions": []}
        ids = []
        for entry in os.listdir(EXTENSIONS_DIR):
            sub = os.path.join(EXTENSIONS_DIR, entry)
            if os.path.isdir(sub):
                versions = [v for v in os.listdir(sub) if os.path.isdir(os.path.join(sub, v))]
                manifest_path = None
                for v in versions:
                    mp = os.path.join(sub, v, "manifest.json")
                    if os.path.exists(mp):
                        manifest_path = mp
                        break
                name = None
                if manifest_path:
                    try:
                        with open(manifest_path, "r", encoding="utf-8") as f:
                            mf = json.load(f)
                            name = mf.get("name")
                    except Exception:
                        pass
                ids.append({"id": entry, "name": name, "versions": versions})
        return {"status": "ok", "count": len(ids), "extensions": ids}


if __name__ == "__main__":
    client = ChromiumCDPClient()
    print("Statut :", client.get_status())
