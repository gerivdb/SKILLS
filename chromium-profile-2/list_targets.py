import sys, time
sys.path.insert(0, r"D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\chromium-profile-2")
from chromium_cdp_client import ChromiumCDPClient
client = ChromiumCDPClient()
client.connect()
# Lister les cibles
resp = client.send("Target.getTargets", {})
targets = resp.get("result", {}).get("targetInfos", [])
print(f"{len(targets)} CIBLES")
for t in targets:
    print(f"  ID: {t['targetId']} | Type: {t['type']} | Title: {t.get('title','')} | URL: {t.get('url','')}")
client.close()