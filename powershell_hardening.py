#!/usr/bin/env python3
# =============================================================================
# powershell_hardening.py — Métaskill de durcissement PowerShell (GOVERNANCE-HUB)
#
# Détecte les appels subprocess invoquant powershell/pwsh sans les gardes
# obligatoires (WindowStyle Hidden, wrapper CMD) et corrige automatiquement le
# fichier en remplaçant la ligne entière.
#
# WAL-0x243-POWERSHELL-HARDENING-SELFTEST
# =============================================================================
from __future__ import annotations

import re
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List

POWERSHELL_CMD_RE = re.compile(r"\b(powershell|pwsh)\b")
WINDOWS_STYLE_HIDDEN_RE = re.compile(r"-WindowStyle\s+Hidden")
WRAPPER_CMD_RE = re.compile(r'"cmd".*?"/c"')
SUBPROCESS_CALL_RE = re.compile(r"subprocess\.(run|check_output|Popen|call|check_call)\s*\(")

WAL_SEAL = "WAL-0x243-POWERSHELL-HARDENING-SELFTEST"


class PowerShellHardening:
    """Métaskill de durcissement PowerShell : détection + correction automatique."""

    def analyze_file(self, path: Path) -> List[str]:
        """Retourne la liste des violations dans le fichier."""
        violations: List[str] = []
        text = path.read_text(encoding="utf-8", errors="replace")
        lines = text.split("\n")

        for i, line in enumerate(lines, start=1):
            if not SUBPROCESS_CALL_RE.search(line):
                continue
            if not POWERSHELL_CMD_RE.search(line):
                continue
            if not WINDOWS_STYLE_HIDDEN_RE.search(line):
                violations.append(f"{path}:{i} — appel PowerShell sans -WindowStyle Hidden")
            if not WRAPPER_CMD_RE.search(line):
                violations.append(f"{path}:{i} — appel PowerShell sans wrapper CMD")

        return violations

    def fix_file(self, path: Path) -> int:
        """Corrige automatiquement un fichier en remplaçant les lignes non conformes."""
        violations = self.analyze_file(path)
        if not violations:
            return 0

        text = path.read_text(encoding="utf-8", errors="replace")
        lines = text.split("\n")
        fixed_count = 0

        new_lines: List[str] = []
        for line in lines:
            if SUBPROCESS_CALL_RE.search(line) and POWERSHELL_CMD_RE.search(line):
                if not (WINDOWS_STYLE_HIDDEN_RE.search(line) or WRAPPER_CMD_RE.search(line)):
                    import re as _re
                    # Capture : subprocess.run(["...", ...], ...)
                    m = _re.search(r'(subprocess\.\w+\(\s*\[)([^\]]*)(\].*)', line)
                    if m:
                        prefix = m.group(1)
                        inner = m.group(2)
                        suffix = m.group(3)
                        # Supprimer le premier élément s'il est powershell/pwsh
                        inner_stripped = _re.sub(
                            r'^"\b(powershell|pwsh)\b"\s*,\s*', '', inner
                        )
                        new_inner = (
                            '"cmd", "/c", "powershell", "-WindowStyle Hidden", '
                            '"-ExecutionPolicy Bypass", ' + inner_stripped
                        )
                        new_line = prefix + new_inner + suffix
                    else:
                        new_line = line
                    new_lines.append(new_line)
                    fixed_count += 1
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)

        path.write_text("\n".join(new_lines), encoding="utf-8")
        return fixed_count

    def harden_file(self, path: Path) -> Dict[str, Any]:
        """Analyse et corrige un fichier."""
        violations_before = self.analyze_file(path)
        fixed_count = self.fix_file(path)
        violations_after = self.analyze_file(path)
        return {
            "file": str(path),
            "violations_before": len(violations_before),
            "fixed": fixed_count,
            "violations_after": len(violations_after),
        }


def self_test() -> bool:
    """Test auto : crée un fichier piégé, le scanne, le corrige, vérifie."""
    print("[SELF-TEST] powershell_hardening — création d'un fichier piégé...")
    tmpdir = Path(tempfile.mkdtemp(prefix="webx_powershell_harden_"))
    bad_file = tmpdir / "bad_powershell.py"
    bad_file.write_text(
        'import subprocess\n'
        'result = subprocess.run(["powershell", "-NoProfile", "-Command", "Get-Process"], capture_output=True, text=True)\n'
    )
    try:
        hardener = PowerShellHardening()
        violations_before = hardener.analyze_file(bad_file)
        print(f"[SELF-TEST] {len(violations_before)} violation(s) détectée(s) avant correction.")

        fixed_count = hardener.fix_file(bad_file)
        print(f"[SELF-TEST] {fixed_count} violation(s) corrigée(s).")

        violations_after = hardener.analyze_file(bad_file)
        print(f"[SELF-TEST] {len(violations_after)} violation(s) restante(s) après correction.")

        if (
            len(violations_before) > 0
            and fixed_count > 0
            and len(violations_after) == 0
        ):
            print("[SELF-TEST] PASS — powershell_hardening opérationnel.")
            print(f"[SELF-TEST] Sceau : {WAL_SEAL}")
            return True
        print("[SELF-TEST] FAIL — Des violations subsistent après correction.")
        print(f"[SELF-TEST] Sceau : {WAL_SEAL}")
        return False
    except Exception as exc:  # noqa: BLE001
        print(f"[SELF-TEST] FAIL — {exc}")
        print(f"[SELF-TEST] Sceau : {WAL_SEAL}")
        return False
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "--self-test":
        return 0 if self_test() else 1
    print("Usage: python powershell_hardening.py --self-test")
    return 1


if __name__ == "__main__":
    sys.exit(main())
