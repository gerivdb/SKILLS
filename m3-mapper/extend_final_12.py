#!/usr/bin/env python3
"""
Étend M3 Mapper aux 9 derniers dépôts restants.
Version simplifiée qui lit le graphe actuel pour éviter les doublons.
"""

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from m3_mapper import load_topology, save_topology, update_tree, update_branch, mark_synapse

TOPO_PATH = Path(__file__).resolve().parent / "topology.json"
DISCOVERED_PATH = Path(__file__).resolve().parent / "discovered_repos.json"


def load_discovered_repos():
    return json.loads(DISCOVERED_PATH.read_text())


def run_test(repo_path, test_file):
    test_path = Path(repo_path) / "tests" / test_file
    if not test_path.exists():
        return {
            "status": "DEAD_END",
            "error_class": "FileNotFound",
            "evidence": f"Fichier de test non trouvé: {test_path}",
            "script": str(test_path),
            "conclusion": "Fichier de test absent du dépôt",
        }

    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", str(test_path), "-v", "--tb=line"],
            capture_output=True,
            text=True,
            timeout=10,
            cwd=repo_path,
        )

        output = result.stdout + result.stderr

        if result.returncode == 0:
            return {
                "status": "VALIDATED_PATH",
                "error_class": None,
                "evidence": "Test passé",
                "evidence_full": output[:500],
                "script": str(test_path),
                "conclusion": "Test pytest passé avec succès",
            }
        else:
            if "ModuleNotFoundError" in output or "ImportError" in output:
                return {
                    "status": "DEAD_END",
                    "error_class": "ImportError",
                    "evidence": "Erreur d'import - module manquant",
                    "evidence_full": output[:500],
                    "script": str(test_path),
                    "conclusion": "Module manquant, test non exécutable",
                }
            elif "ConnectionError" in output or "ConnectionRefusedError" in output:
                return {
                    "status": "BLOCKED",
                    "error_class": "Service_Unavailable",
                    "evidence": "Service externe non disponible",
                    "evidence_full": output[:500],
                    "script": str(test_path),
                    "conclusion": "Dépendance externe non disponible",
                }
            else:
                return {
                    "status": "DEAD_END",
                    "error_class": "TestFailure",
                    "evidence": "Test échoué - assertion ou erreur runtime",
                    "evidence_full": output[:500],
                    "script": str(test_path),
                    "conclusion": "Test échoué",
                }
    except subprocess.TimeoutExpired:
        return {
            "status": "BLOCKED",
            "error_class": "Timeout",
            "evidence": "Timeout (10s) - test trop long ou bloqué",
            "evidence_full": "Timeout après 10 secondes",
            "script": str(test_path),
            "conclusion": "Test trop long ou bloqué",
        }
    except Exception as e:
        return {
            "status": "DEAD_END",
            "error_class": type(e).__name__,
            "evidence": f"Erreur d'exécution: {str(e)}",
            "evidence_full": str(e)[:500],
            "script": str(test_path),
            "conclusion": "Erreur inattendue",
        }


def extend_mapper():
    repos = load_discovered_repos()
    topo = load_topology(TOPO_PATH)

    # Identifier les arbres déjà dans le graphe
    existing_trees = {t.replace("T-", "").upper() for t in topo.get("trees", {})}
    new_repos = {k: v for k, v in repos.items() if k.upper() not in existing_trees}

    print(f"Extension M3 Mapper à {len(new_repos)} nouveaux dépôts...\n")

    count = 0
    for repo_name, repo_info in sorted(new_repos.items(), key=lambda x: x[1]['test_count'], reverse=True):
        tree_id = f"T-{repo_name.upper()}"
        branch_name = "Integration-Tests"

        print(f"  {repo_info['stratum']}/{repo_name} ({repo_info['test_count']} tests)...", end=" ")

        update_tree(topo, tree_id, f"{repo_name} — Tests d'intégration ({repo_info['stratum']})")
        update_branch(topo, tree_id, branch_name, f"Tests pytest {repo_name}")

        test_file = repo_info['test_files'][0] if repo_info['test_files'] else None
        if test_file:
            synapse_name = test_file.replace("test_", "").replace(".py", "")
            result = run_test(repo_info['path'], test_file)

            mark_synapse(
                topo,
                tree_id,
                branch_name,
                synapse_name,
                result['status'],
                synapse_name=synapse_name,
                evidence=result.get('evidence', ''),
                evidence_full=result.get('evidence_full', ''),
                error_class=result.get('error_class'),
                script=result.get('script', ''),
                conclusion=result.get('conclusion', ''),
            )

            print(result['status'])
        else:
            print("Aucun test")

        count += 1
        if count % 10 == 0:
            save_topology(topo, TOPO_PATH)
            print(f"  [Sauvegarde intermédiaire: {count} dépôts traités]")

    save_topology(topo, TOPO_PATH)
    print(f"\n✅ Extension terminée: {len(new_repos)} dépôts traités")


if __name__ == "__main__":
    extend_mapper()
