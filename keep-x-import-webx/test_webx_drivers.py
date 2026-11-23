import sys
sys.path.insert(0, r'D:\DO\WEB\TOOLS\L2-PLATFORM\WEBX\src')
from webx.cluster import WebCluster

c = WebCluster(sot_drivers_path=r'D:\DO\WEB\TOOLS\L2-PLATFORM\WEBX\SOT\drivers')
drivers = c.list_drivers()
for name, info in drivers.items():
    h = info["health"]
    print(f"{name}: {h['status']} (latency: {h['latency_ms']}ms, error: {h.get('error', 'none')})")
