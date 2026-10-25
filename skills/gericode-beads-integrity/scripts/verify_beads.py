# =============================================================================
# verify_beads.py - Skill: gericode-beads-integrity
# Verifie l integrite de beads.json, detecte les verrous Windows, backup tournant
# Cible : L2-PLATFORM/GeriCode/beads.json (2.1 Mo)
# =============================================================================

import json
import os
import sys
import shutil
from datetime import datetime

BEADS_PATH = r"D:\DO\WEB\TOOLS\L2-PLATFORM\GeriCode\beads.json"
BACKUP_DIR = r"D:\DO\WEB\TOOLS\L2-PLATFORM\GeriCode\backups"
MAX_BACKUPS = 5


def is_file_locked(path):
    """Detecte si un fichier est verrouille par Windows."""
    try:
        fd = os.open(path, os.O_RDWR | os.O_CREAT, 0o666)
        os.close(fd)
        return False
    except OSError:
        return True


def verify_json(path):
    """Verifie que le fichier est un JSON valide."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def create_rotating_backup(path, backup_dir):
    """Cree un backup tournant avec horodatage."""
    os.makedirs(backup_dir, exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    backup_path = os.path.join(backup_dir, f"beads.{ts}.bak")
    shutil.copy2(path, backup_path)
    # Rotation : supprimer les plus anciens au-dela de MAX_BACKUPS
    backups = sorted(
        [os.path.join(backup_dir, f) for f in os.listdir(backup_dir) if f.endswith(".bak")],
        key=os.path.getmtime
    )
    while len(backups) > MAX_BACKUPS:
        os.remove(backups.pop(0))
    return backup_path


def main():
    print("[BEADS-INTEGRITY] Debut verification", flush=True)
    print(f"[BEADS-INTEGRITY] Cible : {BEADS_PATH}", flush=True)

    if not os.path.exists(BEADS_PATH):
        print(f"[BEADS-INTEGRITY] BLOQUE: beads.json introuvable", flush=True)
        sys.exit(1)

    # Verrou Windows
    locked = is_file_locked(BEADS_PATH)
    if locked:
        print("[BEADS-INTEGRITY] BLOQUE: beads.json est verrouille par Windows", flush=True)
        sys.exit(1)
    print("[BEADS-INTEGRITY] OK: aucun verrou Windows detecte", flush=True)

    # JSON valide
    try:
        data = verify_json(BEADS_PATH)
        print(f"[BEADS-INTEGRITY] OK: JSON valide ({len(data)} racine(s))", flush=True)
    except Exception as e:
        print(f"[BEADS-INTEGRITY] BLOQUE: JSON invalide - {e}", flush=True)
        sys.exit(1)

    # Backup tournant
    backup_path = create_rotating_backup(BEADS_PATH, BACKUP_DIR)
    print(f"[BEADS-INTEGRITY] Backup cree : {backup_path}", flush=True)

    print("[BEADS-INTEGRITY] Verification terminee avec succes", flush=True)
    sys.exit(0)


if __name__ == "__main__":
    main()

