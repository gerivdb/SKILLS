import urllib.request, json
req = urllib.request.Request('http://127.0.0.1:9222/json')
with urllib.request.urlopen(req) as resp:
    targets = json.loads(resp.read().decode())
print(f'Nombre de cibles CDP: {len(targets)}')
for t in targets:
    print(f'  type={t.get("type")} url={t.get("url")} title={t.get("title")}')