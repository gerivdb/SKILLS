import sys
sys.path.insert(0, r'D:\DO\WEB\TOOLS\L2-PLATFORM\WEBX\src')
from webx.registry import DriverRegistry

r = DriverRegistry(sot_drivers_path=r'D:\DO\WEB\TOOLS\L2-PLATFORM\WEBX\SOT\drivers')
drivers = r.list_drivers()
print(f'Drivers trouves : {len(drivers)}')
for d in drivers:
    name = d.get("name", "unknown")
    engine = d.get("engine", "N/A")
    launchable = d.get("launchable", False)
    headless = d.get("headless", False)
    sovereign = d.get("sovereign", False)
    cdp_port = d.get("cdp_port", "N/A")
    print(f"  - {name} | engine={engine} | launchable={launchable} | headless={headless} | sovereign={sovereign} | cdp_port={cdp_port}")