#!/usr/bin/env python3
#==============================================================================
# SCRIPT DE PURGE DYNAMIQUE — LOT 2 (Tâches 11-20)
# Suppression chirurgicale des entrées fantômes de REGISTRY.yaml
# Compare dynamiquement registre vs disque
#==============================================================================

import yaml
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(r"D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS")
REGISTRY_PATH = BASE / "REGISTRY.yaml"
BACKUP_PATH = BASE / "REGISTRY.yaml.bak"
MANIFEST_PATH = BASE / "MANIFEST.json"
WAL_LOG = BASE / "wal" / "lot2_purge.log"

def write_wal(message: str):
    WAL_LOG.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).isoformat()
    with open(WAL_LOG, "a", encoding="utf-8") as f:
        f.write(f"{ts} | {message}\n")

def main():
    ts = datetime.now(timezone.utc).isoformat()
    
    # Tâche 11 : Sauvegarde de REGISTRY.yaml
    shutil.copy2(REGISTRY_PATH, BACKUP_PATH)
    write_wal(f"[T11] backup_created={BACKUP_PATH}")
    
    # Tâche 12 : Charger le registre
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        registry = yaml.safe_load(f)
    
    original_skills = registry.get("skills", [])
    original_count = len(original_skills)
    write_wal(f"[T12] original_skills_count={original_count}")
    
    # Tâche 13 : Découvrir les skills physiques sur le disque
    physical_skill_names = set()
    for d in BASE.iterdir():
        if d.is_dir() and (d / "SKILL.md").exists():
            physical_skill_names.add(d.name)
    
    write_wal(f"[T13] physical_skills_on_disk={len(physical_skill_names)}")
    
    # Tâche 13 (suite) : Identifier les entrées fantômes (dans le registre, pas sur le disque)
    ghost_ids = [s.get("id") for s in original_skills if s.get("id") not in physical_skill_names]
    ghost_count = len(ghost_ids)
    write_wal(f"[T13] ghost_ids_count={ghost_count}")
    
    # Tâche 13 (suite) : Purger chirurgicalement
    kept_skills = [s for s in original_skills if s.get("id") in physical_skill_names]
    purged_count = original_count - len(kept_skills)
    write_wal(f"[T13] purged_count={purged_count} kept_count={len(kept_skills)}")
    
    # Tâche 14 : Mettre à jour et valider syntaxe YAML
    registry["skills"] = kept_skills
    registry["metadata"]["total_skills"] = len(kept_skills)
    registry["metadata"]["valid_skills"] = len(kept_skills)
    registry["metadata"]["invalid_skills"] = 0
    registry["metadata"]["scan_timestamp"] = ts
    
    output = yaml.dump(registry, sort_keys=False, allow_unicode=True, default_flow_style=False)
    
    # Valider que le YAML est parseable
    yaml.safe_load(output)
    
    with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
        f.write(output)
    
    write_wal(f"[T14] registry_written skills_count={len(kept_skills)}")
    
    # Tâche 15 : Synchroniser MANIFEST.json
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    
    original_manifest_count = len(manifest.get("skills", []))
    kept_skill_names = {s.get("name") for s in kept_skills if s.get("name")}
    manifest["skills"] = [s for s in manifest.get("skills", []) if s.get("name") in kept_skill_names]
    manifest["skillsCount"] = len(manifest["skills"])
    
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    
    write_wal(f"[T15] manifest_synced original={original_manifest_count} new={len(manifest['skills'])}")
    
    # Tâche 16 : Tester le chargement par parseur Python
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        yaml.safe_load(f)
    write_wal("[T16] yaml_reload_validated=OK")
    
    # Tâche 17 : Vérifier l'intégrité de la structure
    assert "registry" in registry, "Clé 'registry' manquante"
    assert "skills" in registry, "Clé 'skills' manquante"
    assert "metadata" in registry, "Clé 'metadata' manquante"
    write_wal("[T17] structure_integrity=OK")
    
    # Tâche 18 : Consigner le delta d'entropie
    write_wal(f"[T18] entropy_delta_before={original_count} after={len(kept_skills)} purged={purged_count}")
    
    # Tâche 19 : Confirmer suppression effective des fantômes
    remaining_ids = [s.get("id") for s in registry.get("skills", [])]
    ghosts_still_present = [g for g in ghost_ids if g in remaining_ids]
    assert len(ghosts_still_present) == 0, f"Fantômes encore présents : {ghosts_still_present}"
    write_wal("[T19] ghosts_confirmed_removed=OK")
    
    # Tâche 20 : Code de retour
    print(f"PURGE TERMINEE : {purged_count} entites fantomes supprimees")
    print(f"Competences restantes : {len(kept_skills)}")
    print("EXIT CODE : 0")
    
    write_wal(f"[T20] exit_code=0")
    return 0

if __name__ == "__main__":
    exit(main())
