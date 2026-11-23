import urllib.request, json

try:
    req = urllib.request.Request('http://127.0.0.1:9222/json/list', method='GET')
    with urllib.request.urlopen(req, timeout=5) as resp:
        data = json.loads(resp.read())
        print(f'Onglets trouves : {len(data)}')
        for t in data:
            tid = t.get('id', '')[:8]
            ttype = t.get('type', '')
            url = t.get('url', 'N/A')[:100]
            title = t.get('title', 'N/A')[:60]
            print(f'  ID: {tid} | Type: {ttype} | URL: {url} | Titre: {title}')
except Exception as e:
    print(f'Erreur: {e}')