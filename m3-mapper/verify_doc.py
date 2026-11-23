from pathlib import Path

p = Path(r"D:\DO\WEB\TOOLS\L0-CANON\ENV3-repo\TOPOLOGY_M3_CHROMIUM.md")
print("Taille:", p.stat().st_size, "octets")
print("Existe:", p.exists())

with open(p, "r", encoding="utf-8") as f:
    content = f.read()
print("Longueur du contenu:", len(content))
print("Premiers 200 chars:", repr(content[:200]))
print("Derniers 200 chars:", repr(content[-200:]))

trees_to_check = ["T-EXT", "T-ID", "T-JEVX", "T-JEVX-IMPASSES", "T-CTULU", "T-KIVA-CLI", "T-ECOS-CLI", "T-GATEWAY-MANAGER", "T-NEXUS", "T-WAZAA", "T-FLUENCE", "T-MIMIR", "T-VDB", "T-BRAIN", "T-TOPOS", "T-ROOTX", "T-PITCH-1"]
for tree in trees_to_check:
    found = tree in content
    print("  %s: %s" % (tree, "TROUVE" if found else "ABSENT"))

idx = content.find("# 🧭 Rapport de Navigation M3")
if idx >= 0:
    print("\n=== RAPPORT DE NAVIGATION (premiers 2000 chars) ===")
    print(content[idx:idx+2000])
else:
    print("Rapport de Navigation: NON TROUVE")