import re
from pathlib import Path

path = Path(r"D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\m3-mapper\m3_mapper.py")
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Trouver et remplacer le bloc du décorateur
# Le bloc commence par "    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:"
# et se termine par "    return decorator\n\n# ---------------------------------------------------------------------------\n# API directe"

old_pattern = r'''    def decorator\(func: Callable\[\.\.\., Any\]\) -> Callable\[,\.\.\., Any\]:
        @wraps\(func\)
        def wrapper\(\*args, \*\*kwargs\):
            branch_id = branch_name\.lower\(\)\.replace\(" ", "_"\)\.replace\("-", "_"\)
            synapse_id = synapse_name\.lower\(\)\.replace\(" ", "_"\)\.replace\("-", "_"\)
            print\(f"🔬 Exploration: \{branch_name\} → \{synapse_name\}"\)

            topo = load_topology\(\)
            topo\["domain"\] = domain

            start_ts = datetime\.now\(timezone\.utc\)

            try:
                result = func\(\*args, \*\*kwargs\)

                # Succès
                syn = _ensure_synapse\(
                    topo, tree_id, branch_id, synapse_id, synapse_name
                \)
                syn\.update\(\{
                    "status": expected_outcome,
                    "error_class": None,
                    "evidence": str\(result\)\[:200\] if result else "Fonction exécutée sans erreur",
                    "evidence_full": str\(result\),
                    "timestamp": datetime\.now\(timezone\.utc\)\.isoformat\(\),
                    "script": script,
                    "conclusion": f"Synapse validée : \{func\.__name__\} a retourné avec succès\.",
                \}
                save_topology\(topo\)
                print\(f"   ✅ VALIDATED_PATH : \{synapse_name\}"\)
                return result

            except TimeoutError as e:
                syn = _ensure_synapse\(
                    topo, tree_id, branch_id, synapse_id, synapse_name
                \)
                syn\.update\(\{
                    "status": "BLOCKED",
                    "error_class": "TimeoutError",
                    "evidence": str\(e\)\[:200\],
                    "evidence_full": str\(e\),
                    "timestamp": datetime\.now\(timezone\.utc\)\.isoformat\(\),
                    "script": script,
                    "conclusion": f"Blocage système : \{func\.__name__\} a expiré \(\{e}\)\.",
                \}
                save_topology\(topo\)
                print\(f"   🛑 BLOCKED : \{synapse_name\} \({e}\)"\)
                raise

            except M3SynapseError as e:
                syn = _ensure_synapse\(
                    topo, tree_id, branch_id, synapse_id, synapse_name
                \)
                syn\.update\(\{
                    "status": "DEAD_END",
                    "error_class": type\(e\)\.__name__,
                    "evidence": str\(e\)\[:200\],
                    "evidence_full": str\(e\),
                    "timestamp": datetime\.now\(timezone\.utc\)\.isoformat\(\),
                    "script": script,
                    "conclusion": f"Impasse architecturale : \{func\.__name__\} \(\{e}\)\.",
                \}
                save_topology\(topo\)
                print\(f"   ❌ DEAD_END : \{synapse_name\} \({e}\)"\)
                raise

            except Exception as e:
                # Toute autre exception est traitée comme une impasse
                syn = _ensure_synapse\(
                    topo, tree_id, branch_id, synapse_id, synapse_name
                \)
                syn\.update\(\{
                    "status": "DEAD_END",
                    "error_class": type\(e\)\.__name__,
                    "evidence": str\(e\)\[:200\],
                    "evidence_full": str\(e\),
                    "timestamp": datetime\.now\(timezone\.utc\)\.isoformat\(\),
                    "script": script,
                    "conclusion": f"Échec inattendu : \{func\.__name__\} \({e}\)\.",
                \}
                save_topology\(topo\)
                print\(f"   ❌ DEAD_END : \{synapse_name\} \({e}\)"\)
                raise

        return wrapper
    return decorator'''

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

# On doit trouver l'ancien bloc et le remplacer
# L'ancien bloc commence par "    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:"
# et se termine par "    return decorator" juste avant "# ---------------------------------------------------------------------------\n# API directe"

start_marker = "    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:"
end_marker = "    return decorator\n\n# ---------------------------------------------------------------------------\n# API directe"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx == -1:
    print("ERREUR: start_marker non trouvé")
    exit(1)

if end_idx == -1:
    print("ERREUR: end_marker non trouvé")
    exit(1)

# Remplacer le bloc
new_content = content[:start_idx] + new_block + content[end_idx + len(end_marker):]

with open(path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("m3_mapper.py modifié avec succès - support async ajouté")
print(f"Lignes remplacées : {end_idx - start_idx}")