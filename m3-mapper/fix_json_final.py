import json

path = r"D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\m3-mapper\topology.json"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Trouver la position de '"metadata":' et tout réécrire à partir de là
idx = content.find('"metadata":')
if idx == -1:
    print("ERREUR: 'metadata' non trouvé")
else:
    # Garder tout jusqu'à la fin de trees (juste avant '"metadata"')
    prefix = content[:idx].rstrip()
    # S'assurer que prefix se termine par '}' (fermeture de trees)
    if not prefix.endswith("}"):
        prefix = prefix.rstrip() + "}"
    
    new_content = prefix + ',\n  "metadata": {\n    "total_trees": 5,\n    "total_branches": 11,\n    "total_synapses": 25,\n    "validated_paths": 10,\n    "dead_ends": 13,\n    "blocked": 1,\n    "last_updated_utc": "2026-11-21T01:15:00Z",\n    "generator": "m3_mapper_engine_v1"\n  }\n}'
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    
    print("Fichier réécrit. Vérification JSON...")
    with open(path, "r", encoding="utf-8") as f:
        topo = json.load(f)
    print("JSON valide !")
    print(f"Trees : {list(topo['trees'].keys())}")
    print(f"Métadonnées : {topo['metadata']}")