from m3_mapper import m3_synapse, load_topology, save_topology, recompute_metadata
import json

class APIError(Exception):
    pass

@m3_synapse(branch_name="Test_Branch", synapse_name="test_synapse_ok", tree_id="T-TEST", tree_name="Arbre Test")
def test_ok():
    return {"result": "ok", "value": 42}

@m3_synapse(branch_name="Test_Branch", synapse_name="test_synapse_fail", tree_id="T-TEST", tree_name="Arbre Test")
def test_fail():
    raise APIError("Test d'impasse simulée")

try:
    test_ok()
except Exception as e:
    print(f"Erreur test_ok : {e}")

try:
    test_fail()
except Exception as e:
    print(f"Erreur test_fail (attendue) : {e}")

topo = load_topology()
topo = recompute_metadata(topo)
save_topology(topo)

print()
print("=== État du graphe après test ===")
print(json.dumps(topo["metadata"], indent=2, ensure_ascii=False))
print()
for tid, tree in topo["trees"].items():
    if tid == "T-TEST":
        for bid, branch in tree["branches"].items():
            for sid, syn in branch["synapses"].items():
                print(f"  {syn['name']}: {syn['status']} ({syn.get('error_class','-')})")
