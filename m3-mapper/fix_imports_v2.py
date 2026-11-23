#!/usr/bin/env python3
"""
Corrige les problèmes d'imports dans les fichiers de test JEVX :
1. Ajoute 'import sys' avant toute utilisation de sys.path.insert
2. Remplace WindowsPath( par Path( (car Path est déjà importé)
3. S'assure que 'from m3_mapper import m3_synapse' est présent
"""

import re
from pathlib import Path

TESTS_DIR = Path(r"D:\DO\WEB\TOOLS\L4-TOOLS\JEVX\tests")

def fix_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    original = content
    
    # 1. Remplacer WindowsPath( par Path( (Path est déjà importé dans la plupart des fichiers)
    content = content.replace("WindowsPath(", "Path(")
    
    # 2. Ajouter 'import sys' avant la première utilisation de sys.path.insert
    #    si 'import sys' n'est pas déjà présent avant
    lines = content.split('\n')
    new_lines = []
    sys_imported = False
    sys_path_insert_seen = False
    
    for line in lines:
        new_lines.append(line)
        
        # Détecter si 'import sys' est déjà présent
        if re.match(r'^import sys\s*$', line):
            sys_imported = True
        
        # Détecter la première utilisation de sys.path.insert
        if 'sys.path.insert' in line and not sys_imported:
            # Insérer 'import sys' avant cette ligne
            new_lines.insert(len(new_lines) - 1, 'import sys')
            sys_imported = True
    
    content = '\n'.join(new_lines)
    
    # 3. S'assurer que 'from m3_mapper import m3_synapse' est présent
    if 'from m3_mapper import m3_synapse' not in content:
        # Insérer après les autres imports
        lines = content.split('\n')
        insert_idx = 0
        for i, line in enumerate(lines):
            if line.startswith('import ') or line.startswith('from '):
                insert_idx = i + 1
        lines.insert(insert_idx, 'from m3_mapper import m3_synapse')
        content = '\n'.join(lines)
    
    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  [FIX] {filepath.name}")
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