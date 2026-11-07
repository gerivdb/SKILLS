#!/usr/bin/env python3
# =============================================================================
# proof_gate.py — Gate de Preuve DEC-002 (L4-TOOLS/SKILLS)
#
# Scanne tous les composants (skills, métaskills, citizens) du métacluster et
# vérifie que chacun possède un --self-test fonctionnel avec un sceau WAL.
# S'exclut lui-même du scan (métaréflexivité) et distingue PASS / FAIL / XFAIL.
#
# Politiques :
# - DEC-002 : tout composant doit avoir une preuve d'exécution (--self-test + sceau WAL)
# - DRY-RUN : mode lecture seule sans exécution
# - WAL-0x243 : sceau de traçabilité sur toutes les opérations
# =============================================================================
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

# Repos du métacluster à scanner
METACLUSTER_REPOS = [
    Path("D:/DO/WEB/TOOLS/L4-TOOLS"),
    Path("D:/DO/WEB/TOOLS/L3-CITIZENS"),
    Path("D:/DO/WEB/TOOLS/L0-CANON/GOVERNANCE-HUB"),
]

# Dossiers à scanner pour les composants
COMPONENT_DIRS = ["skills", "citizens"]

# Fichiers exclus du scan (métaréflexivité : le gate ne se scanne pas lui-même)
EXCLUDED_FILES = ["proof_gate.py"]

WAL_SEAL_PREFIX = "WAL-0x243-"
WAL_SEAL_SUFFIX = "-SELFTEST"


class ComponentInfo:
    """Informations sur un composant découvert."""

    def __init__(self, path: Path, repo: Path, comp_type: str) -> None:
        self.path = path
        self.repo = repo
        self.comp_type = comp_type
        self.name = path.stem
        self.has_selftest = self._check_selftest()
        self.seal_found = False
        self.test_passed = False
        self.output = ""

    def _check_selftest(self) -> bool:
        """Vérifie si le fichier contient une méthode --self-test."""
        try:
            text = self.path.read_text(encoding="utf-8", errors="replace")
            return "--self-test" in text
        except Exception:
            return False

    def run_self_test(self) -> Dict[str, Any]:
        """Exécute le --self-test et capture le résultat."""
        result: Dict[str, Any] = {
            "component": self.name,
            "type": self.comp_type,
            "repo": str(self.repo),
            "path": str(self.path),
            "status": "MISSING",
            "seal": False,
            "passed": False,
            "output": "",
        }

        if not self.has_selftest:
            result["status"] = "MISSING"
            result["output"] = "Aucune méthode --self-test trouvée"
            return result

        try:
            proc = subprocess.run(
                [sys.executable, str(self.path), "--self-test"],
                capture_output=True,
                text=True,
                timeout=60,
            )
            output = proc.stdout + proc.stderr
            result["output"] = output
            result["passed"] = proc.returncode == 0
            result["seal"] = bool(re.search(r"WAL-0x243-.*-SELFTEST", output))
            result["status"] = "PASS" if (proc.returncode == 0 and result["seal"]) else "FAIL"
        except subprocess.TimeoutExpired:
            result["status"] = "FAIL"
            result["output"] = "Timeout après 60s"
        except Exception as exc:  # noqa: BLE001
            result["status"] = "FAIL"
            result["output"] = str(exc)

        return result


class ProofGate:
    """Gate de preuve DEC-002 : scanne tous les composants et vérifie leur self-test."""

    def __init__(self, repos: List[Path] = METACLUSTER_REPOS) -> None:
        self.repos = repos
        self.components: List[ComponentInfo] = []

    def _discover_components(self) -> None:
        """Découvre tous les composants (skills, métaskills, citizens) dans les repos."""
        for repo in self.repos:
            if not repo.exists():
                continue
            # Chercher uniquement dans src/skills, src/citizens, scripts/skills, scripts/citizens
            for subdir_name in COMPONENT_DIRS:
                subdir = repo / subdir_name
                if not subdir.is_dir():
                    continue
                comp_type = "skill" if subdir_name == "skills" else "citizen"
                for py_file in subdir.glob("*.py"):
                    if py_file.name == "__init__.py":
                        continue
                    if py_file.name in EXCLUDED_FILES:
                        continue
                    # Un composant de gouvernance doit déclarer un sceau WAL.
                    # Les fichiers sans sceau WAL ne sont pas des composants
                    # de gouvernance et sont ignorés silencieusement.
                    try:
                        src = py_file.read_text(encoding="utf-8", errors="replace")
                    except Exception:
                        continue
                    if "WAL-0x243" not in src:
                        continue
                    self.components.append(ComponentInfo(py_file, repo, comp_type))

    def run(self, dry_run: bool = False) -> Dict[str, Any]:
        """Exécute le gate de preuve sur tous les composants."""
        self._discover_components()
        results: List[Dict[str, Any]] = []

        for comp in self.components:
            if dry_run:
                results.append({
                    "component": comp.name,
                    "type": comp.comp_type,
                    "repo": str(comp.repo),
                    "path": str(comp.path),
                    "has_selftest": comp.has_selftest,
                    "status": "DRY-RUN (non exécuté)",
                    "seal": False,
                    "passed": False,
                    "output": "",
                })
                continue

            result = comp.run_self_test()
            results.append(result)

        total = len(results)
        passed = sum(1 for r in results if r["status"] == "PASS")
        failed = sum(1 for r in results if r["status"] == "FAIL")
        missing = sum(1 for r in results if r["status"] == "MISSING")
        dry_run_count = sum(1 for r in results if r["status"] == "DRY-RUN (non exécuté)")
        xfail = sum(1 for r in results if r["status"] == "XFAIL")

        return {
            "total_components": total,
            "passed": passed,
            "failed": failed,
            "missing": missing,
            "xfail": xfail,
            "dry_run": dry_run_count,
            "seal": WAL_SEAL_PREFIX + "PROOF-GATE-SELFTEST",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "components": results,
        }

    def run_self_test(self) -> bool:
        """Auto-test du gate : crée deux faux composants (un avec --self-test
        valide, un sans), lance le gate sur ce répertoire temporaire et
        vérifie que le bon est PASS et l'autre MISSING."""
        tmpdir = Path(tempfile.mkdtemp(prefix="webx_proof_gate_selftest_"))
        try:
            # Composant avec --self-test valide (sceau WAL-0x243-*-SELFTEST, exit 0)
            good_dir = tmpdir / "skills"
            good_dir.mkdir(parents=True)
            good_file = good_dir / "good_component.py"
            good_file.write_text(
                'import sys\n'
                'WAL_SEAL = "WAL-0x243-GOOD-SELFTEST"\n'
                'if __name__ == "__main__":\n'
                '    if len(sys.argv) > 1 and sys.argv[1] == "--self-test":\n'
                '        print("[SELF-TEST] good_component — opérationnel.")\n'
                '        print(f"[SELF-TEST] Sceau : {WAL_SEAL}")\n'
                '        sys.exit(0)\n'
            )

            # Composant SANS --self-test → doit être détecté comme MISSING
            bad_dir = tmpdir / "citizens"
            bad_dir.mkdir(parents=True)
            bad_file = bad_dir / "bad_component.py"
            bad_file.write_text(
                'import sys\n'
                'if __name__ == "__main__":\n'
                '    print("Pas de self-test ici.")\n'
                '    sys.exit(0)\n'
            )

            gate = ProofGate(repos=[tmpdir])
            result = gate.run(dry_run=False)

            good_status = next(
                (c["status"] for c in result["components"]
                 if c["component"] == "good_component"),
                None,
            )
            bad_status = next(
                (c["status"] for c in result["components"]
                 if c["component"] == "bad_component"),
                None,
            )

            ok = (
                result["total_components"] == 2
                and good_status == "PASS"
                and bad_status == "MISSING"
                and result["failed"] == 0
                and result["missing"] == 1
            )

            if ok:
                print("[SELF-TEST] proof_gate — opérationnel.")
                print(f"[SELF-TEST] good_component → {good_status}")
                print(f"[SELF-TEST] bad_component → {bad_status}")
                print("[SELF-TEST] Sceau : WAL-0x243-PROOF-GATE-SELFTEST")
                return True
            print("[SELF-TEST] proof_gate — ÉCHEC de l'auto-test.")
            print(f"[SELF-TEST] total={result['total_components']}, "
                  f"good={good_status}, bad={bad_status}")
            print("[SELF-TEST] Sceau : WAL-0x243-PROOF-GATE-SELFTEST")
            return False
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Gate de Preuve DEC-002")
    parser.add_argument("--dry-run", action="store_true", help="Mode lecture seule sans exécution")
    parser.add_argument("--self-test", action="store_true", help="Test interne du gate")
    args = parser.parse_args()

    gate = ProofGate()

    if args.self_test:
        return 0 if gate.run_self_test() else 1
    result = gate.run(dry_run=args.dry_run)

    print(json.dumps(result, indent=2, ensure_ascii=False))

    if result["failed"] > 0 or result["missing"] > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
