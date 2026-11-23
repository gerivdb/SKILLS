import re
from pathlib import Path

path = Path(r"D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\m3-mapper\m3_mapper.py")
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Trouver les lignes de début et fin du bloc du décorateur
start_line = None
end_line = None

for i, line in enumerate(lines):
    if line.strip() == "def decorator(func: Callable[..., Any]) -> Callable[..., Any]:":
        start_line = i
    if start_line is not None and line.strip() == "return decorator":
        end_line = i
        break

if start_line is None:
    print("ERREUR: start_line non trouvé")
    exit(1)

if end_line is None:
    print("ERREUR: end_line non trouvé")
    exit(1)

print(f"Remplacement des lignes {start_line+1} à {end_line+1}")

# Le nouveau bloc de décorateur
new_block = '''    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        import asyncio

        if asyncio.iscoroutinefunction(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                branch_id = branch_name.lower().replace(" ", "_").replace("-", "_")
                synapse_id = synapse_name.lower().replace(" ", "_").replace("-", "_")
                print(f"🔬 Exploration: {branch_name} → {synapse_name}")

                topo = load_topology()
                topo["domain"] = domain
                start_ts = datetime.now(timezone.utc)

                try:
                    result = await func(*args, **kwargs)

                    # Succès
                    syn = _ensure_synapse(
                        topo, tree_id, branch_id, synapse_id, synapse_name
                    )
                    syn.update({
                        "status": expected_outcome,
                        "error_class": None,
                        "evidence": str(result)[:200] if result else "Fonction exécutée sans erreur",
                        "evidence_full": str(result),
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "script": script,
                        "conclusion": f"Synapse validée : {func.__name__} a retourné avec succès.",
                    })
                    save_topology(topo)
                    print(f"   ✅ VALIDATED_PATH : {synapse_name}")
                    return result

                except TimeoutError as e:
                    syn = _ensure_synapse(
                        topo, tree_id, branch_id, synapse_id, synapse_name
                    )
                    syn.update({
                        "status": "BLOCKED",
                        "error_class": "TimeoutError",
                        "evidence": str(e)[:200],
                        "evidence_full": str(e),
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "script": script,
                        "conclusion": f"Blocage système : {func.__name__} a expiré ({e}).",
                    })
                    save_topology(topo)
                    print(f"   🛑 BLOCKED : {synapse_name} ({e})")
                    raise

                except M3SynapseError as e:
                    syn = _ensure_synapse(
                        topo, tree_id, branch_id, synapse_id, synapse_name
                    )
                    syn.update({
                        "status": "DEAD_END",
                        "error_class": type(e).__name__,
                        "evidence": str(e)[:200],
                        "evidence_full": str(e),
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "script": script,
                        "conclusion": f"Impasse architecturale : {func.__name__} ({e}).",
                    })
                    save_topology(topo)
                    print(f"   ❌ DEAD_END : {synapse_name} ({e})")
                    raise

                except Exception as e:
                    # Toute autre exception est traitée comme une impasse
                    syn = _ensure_synapse(
                        topo, tree_id, branch_id, synapse_id, synapse_name
                    )
                    syn.update({
                        "status": "DEAD_END",
                        "error_class": type(e).__name__,
                        "evidence": str(e)[:200],
                        "evidence_full": str(e),
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "script": script,
                        "conclusion": f"Échec inattendu : {func.__name__} ({e}).",
                    })
                    save_topology(topo)
                    print(f"   ❌ DEAD_END : {synapse_name} ({e})")
                    raise

            return wrapper
        else:
            @wraps(func)
            def wrapper(*args, **kwargs):
                branch_id = branch_name.lower().replace(" ", "_").replace("-", "_")
                synapse_id = synapse_name.lower().replace(" ", "_").replace("-", "_")
                print(f"🔬 Exploration: {branch_name} → {synapse_name}")

                topo = load_topology()
                topo["domain"] = domain
                start_ts = datetime.now(timezone.utc)

                try:
                    result = func(*args, **kwargs)

                    # Succès
                    syn = _ensure_synapse(
                        topo, tree_id, branch_id, synapse_id, synapse_name
                    )
                    syn.update({
                        "status": expected_outcome,
                        "error_class": None,
                        "evidence": str(result)[:200] if result else "Fonction exécutée sans erreur",
                        "evidence_full": str(result),
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "script": script,
                        "conclusion": f"Synapse validée : {func.__name__} a retourné avec succès.",
                    })
                    save_topology(topo)
                    print(f"   ✅ VALIDATED_PATH : {synapse_name}")
                    return result

                except TimeoutError as e:
                    syn = _ensure_synapse(
                        topo, tree_id, branch_id, synapse_id, synapse_name
                    )
                    syn.update({
                        "status": "BLOCKED",
                        "error_class": "TimeoutError",
                        "evidence": str(e)[:200],
                        "evidence_full": str(e),
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "script": script,
                        "conclusion": f"Blocage système : {func.__name__} a expiré ({e}).",
                    })
                    save_topology(topo)
                    print(f"   🛑 BLOCKED : {synapse_name} ({e})")
                    raise

                except M3SynapseError as e:
                    syn = _ensure_synapse(
                        topo, tree_id, branch_id, synapse_id, synapse_name
                    )
                    syn.update({
                        "status": "DEAD_END",
                        "error_class": type(e).__name__,
                        "evidence": str(e)[:200],
                        "evidence_full": str(e),
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "script": script,
                        "conclusion": f"Impasse architecturale : {func.__name__} ({e}).",
                    })
                    save_topology(topo)
                    print(f"   ❌ DEAD_END : {synapse_name} ({e})")
                    raise

                except Exception as e:
                    # Toute autre exception est traitée comme une impasse
                    syn = _ensure_synapse(
                        topo, tree_id, branch_id, synapse_id, synapse_name
                    )
                    syn.update({
                        "status": "DEAD_END",
                        "error_class": type(e).__name__,
                        "evidence": str(e)[:200],
                        "evidence_full": str(e),
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "script": script,
                        "conclusion": f"Échec inattendu : {func.__name__} ({e}).",
                    })
                    save_topology(topo)
                    print(f"   ❌ DEAD_END : {synapse_name} ({e})")
                    raise

            return wrapper
    return decorator'''

# Remplacer les lignes
new_lines = lines[:start_line] + [new_block + "\n"] + lines[end_line + 1:]

with open(path, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("m3_mapper.py modifié avec succès - support async ajouté")
print(f"Lignes {start_line+1} à {end_line+1} remplacées")