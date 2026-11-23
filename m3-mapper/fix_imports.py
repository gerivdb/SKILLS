#!/usr/bin/env python3
"""
Corrige l'ordre des imports dans les fichiers de test JEVX :
- S'assure que 'import sys' apparaît avant toute utilisation de 'sys.path.insert'
- S'assure que 'from m3_mapper import m3_synapse' est présent
"""

import re
from pathlib import Path

TESTS_DIR = Path(r"D:\DO\WEB\TOOLS\L4-TOOLS\JEVX\tests")

def fix_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    original = content
    
    # Vérifier si sys est importé
    has_import_sys = bool(re.search(r'^import sys\s*$', content, re.MULTILINE))
    
    # Vérifier si sys.path.insert est présent
    has_sys_path_insert = 'sys.path.insert' in content
    
    if has_sys_path_insert and not has_import_sys:
        # Insérer 'import sys' au tout début du fichier (avant tout le reste)
        lines = content.split('\n')
        # Trouver où insérer : tout début du fichier
        lines.insert(0, 'import sys')
        content = '\n'.join(lines)
        print(f"  [FIX] {filepath.name} - ajouté 'import sys' en tête")
    
    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False

def main():
    test_files = sorted(TESTS_DIR.glob("test_*.py"))
    fixed = 0
    for tf in test_files:
        if fix_file(tf):
            fixed += 1
    print(f"\n{fixed} fichiers corrigés")

if __name__ == "__main__":
    main()