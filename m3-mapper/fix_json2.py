import json

path = r"D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\m3-mapper\topology.json"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Supprimer la dernière ligne si elle est juste une accolade fermante en trop
if lines[-1].strip() == "}":
    lines = lines[:-1]

with open(path, "w", encoding="utf-8") as f:
    f.writelines(lines)

print("Dernière accolade supprimée. Vérification JSON...")
with open(path, "r", encoding="utf-8") as f:
    topo = json.load(f)
print("JSON valide !")
print(f"Trees : {list(topo['trees'].keys())}")
print(f"Métadonnées : {topo['metadata']}")