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

Pilier 1 (Session Pooling) : WebSocket persistante (self._ws) réutilisée entre les commandes.
Pilier 1 (Event-driven) : navigate() attend Page.loadEventFired au lieu d'un sleep().
Pilier 4 (Auto-guérison) : catch -32601 → génération dynamique d'un wrapper dans dynamic_methods.py.
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

# Import MA3 algorithmes deterministes (REF-182)
MA3_PATH = Path(__file__).resolve().parent.parent / "ma3_algorithms"
if str(MA3_PATH) not in sys.path:
    sys.path.insert(0, str(MA3_PATH))
from sliding_window import SlidingWindow  # noqa: E402

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
        # Session Pooling : WebSocket persistante (endpoint Browser)
        self._ws = None
        self._ws_url: Optional[str] = None
        # WebSocket dédiée Page (pour domaines Runtime/DOM/Page/Input)
        self._page_ws = None
        self._page_ws_url: Optional[str] = None
        self._page_tab_id: Optional[str] = None
        self._client: Optional[CDPClient] = None
        self._active_tab_id: Optional[str] = None
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._tab_ws_urls: Dict[str, str] = {}
        self._msg_id = 0                     # Compteur d'ID JSON-RPC
        self._session_ids: Dict[str, str] = {}  # tab_id -> sessionId (Target.attachToTarget)
        # Event-driven navigation
        self._event_queue: "queue.Queue[str]" = queue.Queue()
        self._event_thread: Optional[threading.Thread] = None
        self._event_listener_running = False

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

    # ------------------------------------------------------------------ session pooling (WebSocket Browser)
    def _ensure_connected(self):
        """Ouvre (ou réutilise) un WebSocket persistant vers Chromium CDP (endpoint Browser)."""
        if self._ws is not None:
            try:
                loop = self._get_loop()
                loop.run_until_complete(self._ws.ping())
                return self._ws
            except Exception:
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

    # ------------------------------------------------------------------ session pooling (WebSocket Page)
    def _ensure_page_connected(self, tab_id: Optional[str] = None) -> Any:
        """
        Ouvre (ou réutilise) un WebSocket persistant vers l'endpoint Page de l'onglet cible.
        Nécessaire pour les domaines Runtime/DOM/Page/Input qui ne sont pas sur l'endpoint Browser.
        Vérifie la fraîcheur de la socket (ping) avant de la réutiliser.
        """
        target_id = tab_id or self._active_tab_id
        if not target_id:
            return None

        # Réutiliser si déjà connecté et vivant
        if self._page_ws is not None and self._page_tab_id == target_id:
            try:
                loop = self._get_loop()
                loop.run_until_complete(self._page_ws.ping())
                return self._page_ws
            except Exception:
                try:
                    loop.run_until_complete(self._page_ws.close())
                except Exception:
                    pass
                self._page_ws = None
                self._page_ws_url = None
                self._page_tab_id = None

        # Toujours rafraîchir l'URL de debug via /json/list (le cache self._tab_ws_urls
        # devient obsolète après une Page.navigate qui change le contexte d'exécution)
        page_url = None
        tabs = self.list_tabs()
        for t in tabs:
            if t["id"] == target_id and t.get("webSocketDebuggerUrl"):
                page_url = t["webSocketDebuggerUrl"]
                break
        # Fallback sur le cache _tab_ws_urls (rempli par open_tab / attach_to_tab)
        if not page_url and target_id in self._tab_ws_urls:
            page_url = self._tab_ws_urls[target_id]
        if not page_url:
            return None

        loop = self._get_loop()
        self._page_ws = loop.run_until_complete(websockets.connect(page_url))
        self._page_ws_url = page_url
        self._page_tab_id = target_id
        return self._page_ws

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

    # ------------------------------------------------------------------ navigation (event-driven)
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

        # 5. Invalider le cache WebSocket Page : le contexte d'exécution a changé
        #    après la navigation, l'ancienne socket pointe vers about:blank.
        self._page_ws = None
        self._page_ws_url = None
        self._page_tab_id = None

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

    # ------------------------------------------------------------------ envoi CDP (WebSocket persistante)
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
        # Routage par domaine : Page DOMAINS -> WebSocket Page dédiée
        # Autre domaine -> WebSocket Browser persistante
        if domain in self.PAGE_DOMAINS:
            ws = self._ensure_page_connected(self._active_tab_id)
            if ws is None:
                return {"error": {"code": -32603, "message": "Impossible d'attacher à la page"}}
        else:
            ws = self._ensure_connected()
        loop = self._get_loop()
        msg_id = self._next_id()
        message = json.dumps({
            "id": msg_id,
            "method": f"{domain}.{method}",
            "params": params or {},
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
                "webSocketDebuggerUrl": t.get("webSocketDebuggerUrl"),
            }
            for t in data
        ]

    def switch_tab(self, target_id: str) -> Dict[str, Any]:
        return self.send("Target", "activateTarget", {"targetId": target_id})

    # ------------------------------------------------------------- navigation helpers
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

    def _extract_eval_value(self, response: Any) -> str:
        """Extrait la valeur d'une reponse CDP Runtime.evaluate (double nesting result.result.value)."""
        if isinstance(response, dict):
            result = response.get("result", {})
            if isinstance(result, dict):
                inner = result.get("result", {})
                if isinstance(inner, dict):
                    val = inner.get("value", "")
                    return str(val) if val is not None else ""
                return str(result.get("value", ""))
        return ""

    def _strip_html_tags(self, html: str) -> str:
        """Supprime les balises HTML d'une chaine (fallback extraction texte)."""
        import re
        text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def read_dom_sliding(self, selector: str, window_size: int = 4096,
                          min_chars: int = 256) -> Dict[str, Any]:
        """Extraction de densite DOM via SlidingWindow (remplace DENSITY_JS bugge).

        Recupere le textContent de l element selectionne, puis en cas de texte
        vide (Shadow DOM, iframes) bascule sur innerHTML + nettoyage Python.
        Applique ensuite une fenetre glissante pour isoler les chunks
        semantiques denses.
        """
        raw = self.read_dom(selector)
        text = self._extract_eval_value(raw)

        # Fallback : si textContent vide, utiliser innerHTML + nettoyage Python
        if not text:
            html_raw = self.evaluate_js(
                f"(function(){{const el=document.querySelector('{selector}');"
                "return el ? el.innerHTML : '';}})()"
            )
            html_text = self._extract_eval_value(html_raw)
            text = self._strip_html_tags(html_text)

        chunks = SlidingWindow.dom_density(text, window_size, min_chars)
        total_chars = sum(len(c) for _, _, c in chunks)
        return {
            "selector": selector,
            "total_chars": total_chars,
            "chunk_count": len(chunks),
            "chunks": chunks,
        }

    def read_bridge_state(self) -> Dict[str, Any]:
        """Lit l'état du pont DOM (document.documentElement.dataset.bridgeState)
        maintenu par l'extension Sensor. Accessible depuis main world via CDP."""
        import json
        response = self.send("Runtime", "evaluate", {
            "expression": (
                "(function(){"
                "const ds = document.documentElement.dataset.bridgeState;"
                "return ds ? JSON.parse(ds) : { generating: true, lastResponse: '', cycle: 0, ready: false };"
                "})()"
            ),
            "returnByValue": True,
        })
        val = self._extract_eval_value(response)
        try:
            return json.loads(val) if val else {}
        except json.JSONDecodeError:
            return {}

    def wait_for_response_complete(self, timeout: float = 30.0) -> str:
        """Attend que la réponse Gemini soit complète (pas de génération en cours).

        Lit document.documentElement.dataset.bridgeState maintenu par l'extension
        Sensor (Chemin B). Si le capteur n'apparaît pas après sensor_timeout,
        bascule sur read_dom_sliding (innerHTML, Chemin A).
        Retourne lastResponse dès que ready=True et generating=False.
        """
        import json

        sensor_timeout = 5.0  # attendre max 5s que le capteur soit injecté
        state = {}
        sensor_seen = False
        sensor_deadline = time.perf_counter() + sensor_timeout
        deadline = time.perf_counter() + timeout

        while time.perf_counter() < deadline:
            state = self.read_bridge_state()
            if state:
                sensor_seen = True
                if state.get("ready") and not state.get("generating"):
                    return str(state.get("lastResponse", ""))
            elif time.perf_counter() >= sensor_deadline and not sensor_seen:
                # Capteur jamais apparu : bascule sur le fallback innerHTML
                break
            time.sleep(0.2)

        # Fallback Chemin A : innerHTML + SlidingWindow
        sliding = self.read_dom_sliding("body", window_size=4096, min_chars=256)
        if sliding["total_chars"] > 0:
            return "".join(c for _, _, c in sliding["chunks"])

        raise TimeoutError(
            f"Réponse Gemini non complète après {timeout}s (état dernier: {state})"
        )

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
