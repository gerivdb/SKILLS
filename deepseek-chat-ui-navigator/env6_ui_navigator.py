# env6_ui_navigator.py — Contrôle UI de la colonne de gauche (ENV6)
# Permet de lister les conversations, en changer, ou en créer une nouvelle.
import json, urllib.request, websocket, time, sys

CDP = "http://127.0.0.1:9222"

def find_tab():
    tabs = json.loads(urllib.request.urlopen(CDP + "/json/list").read())
    return next((t for t in tabs if t.get("type") == "page" and "chat.deepseek.com" in t.get("url", "")), None)

def cdp_eval(expr, await_promise=False):
    tab = find_tab()
    if not tab: return {"error": "no_tab"}
    ws = websocket.create_connection(tab["webSocketDebuggerUrl"], suppress_origin=True, timeout=10)
    try:
        ws.send(json.dumps({"id": 1, "method": "Runtime.evaluate",
            "params": {"expression": expr, "returnByValue": True, "awaitPromise": await_promise}}))
        while True:
            r = json.loads(ws.recv())
            if r.get("id") == 1:
                return r.get("result", {}).get("result", {}).get("value")
    finally:
        ws.close()

def list_conversations():
    """Extrait la liste des conversations depuis la col_gauche."""
    js = """
    (() => {
      // DeepSeek utilise souvent des liens <a> ou des <div> avec role="button" dans l'historique
      const items = Array.from(document.querySelectorAll('a[href*="/a/chat/s/"], [class*="history"] a, [class*="chat-item"]'));
      return items.map(el => ({
        title: el.innerText.trim().split('\\n')[0], // Premier ligne du texte
        href: el.getAttribute('href') || 'unknown',
        id: (el.getAttribute('href') || '').split('/s/')[1] || 'unknown'
      })).filter(c => c.title.length > 0 && c.title !== "Nouvelle conversation");
    })()
    """
    return cdp_eval(js)

def switch_conversation(conv_id):
    """Clique sur une conversation spécifique."""
    js = f"""
    (() => {{
      const items = Array.from(document.querySelectorAll('a'));
      const target = items.find(el => el.getAttribute('href') && el.getAttribute('href').includes('{conv_id}'));
      if (target) {{
        target.click();
        return {{status: 'clicked', id: '{conv_id}'}};
      }}
      return {{status: 'not_found', id: '{conv_id}'}};
    }})()
    """
    return cdp_eval(js)

def create_new_conversation():
    """Clique sur le bouton Nouvelle conversation."""
    js = """
    (() => {
      // Cherche le bouton avec le texte "Nouvelle conversation" ou l'icône +
      const btns = Array.from(document.querySelectorAll('button, [role="button"], div'));
      const target = btns.find(el => el.innerText && el.innerText.includes('Nouvelle conversation'));
      if (target) {
        target.click();
        return {status: 'clicked_new'};
      }
      return {status: 'not_found'};
    })()
    """
    return cdp_eval(js)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python env6_ui_navigator.py [list|switch <id>|new]")
        sys.exit(1)
        
    cmd = sys.argv[1]
    if cmd == "list":
        convs = list_conversations()
        print(json.dumps(convs, indent=2, ensure_ascii=False))
    elif cmd == "switch" and len(sys.argv) > 2:
        res = switch_conversation(sys.argv[2])
        print(res)
    elif cmd == "new":
        res = create_new_conversation()
        print(res)