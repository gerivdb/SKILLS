import json

path = r"D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\m3-mapper\topology.json"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Ajouter une virgule après la fermeture de 'trees' avant 'metadata'
content = content.replace(
    "  },\n  \"metadata\": {",
    "  },\n  },\n  \"metadata\": {"
)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Fichier modifié. Vérification JSON...")
with open(path, "r", encoding="utf-8") as f:
    topo = json.load(f)
print("JSON valide !")
print(f"Trees : {list(topo['trees'].keys())}")
print(f"Métadonnées : {topo['metadata']}")