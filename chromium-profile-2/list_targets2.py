import asyncio
import json
import websockets

CDP_URL = "ws://127.0.0.1:9222/devtools/browser/77311bc9-4ae7-434d-ab14-abe7204e2b73"

async def main():
    async with websockets.connect(CDP_URL) as ws:
        # Lister les cibles
        await ws.send(json.dumps({"id": 1, "method": "Target.getTargets", "params": {}}))
        resp = json.loads(await ws.recv())
        targets = resp.get("result", {}).get("targetInfos", [])
        print(f"{len(targets)} CIBLES")
        for t in targets:
            print(f"  ID: {t['targetId']} | Type: {t['type']} | Title: {t.get('title','')} | URL: {t.get('url','')}")

asyncio.run(main())