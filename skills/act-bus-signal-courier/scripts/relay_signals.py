# =============================================================================
# relay_signals.py - Skill: act-bus-signal-courier
# Valide la structure atomique des signaux (eNN-completed.json)
# Pontage avec bus WAZAA en L4 + fallback WAL 0x243
# =============================================================================

import json
import os
import sys
import shutil
from datetime import datetime

KILO_BUS = r"D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\.kilo\bus"
WAZAA_BUS = r"D:\DO\WEB\TOOLS\L4-TOOLS\WAZAA"
WAL_FALLBACK = r"D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\wal\0x243"
SIGNAL_PATTERN = "eNN-completed.json"


def validate_signal_structure(signal_path):
    """Valide qu un signal respecte la structure atomique eNN-completed.json."""
    try:
        with open(signal_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        return False, f"JSON invalide: {e}"
    required = ["signal_id", "status", "timestamp", "worktree"]
    missing = [k for k in required if k not in data]
    if missing:
        return False, f"Champs manquants: {missing}"
    if data["status"] != "completed":
        return False, f"Statut inattendu: {data.get('status')}"
    return True, "Structure valide"


def bridge_to_wazaa(signal_path):
    """Copie le signal vers le bus WAZAA en L4."""
    os.makedirs(WAZAA_BUS, exist_ok=True)
    dest = os.path.join(WAZAA_BUS, os.path.basename(signal_path))
    shutil.copy2(signal_path, dest)
    return dest


def wal_fallback(signal_path, reason):
    """Ecrit le signal dans le WAL de fallback 0x243."""
    os.makedirs(WAL_FALLBACK, exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    wal_path = os.path.join(WAL_FALLBACK, f"signal_{ts}.json")
    shutil.copy2(signal_path, wal_path)
    with open(wal_path, "a", encoding="utf-8") as f:
        f.write(f"\n# Fallback reason: {reason}\n# WAL: 0x243\n")
    return wal_path


def main():
    print("[BUS-COURIER] Debut relay signaux GeriCode", flush=True)

    # Chercher les signaux eNN-completed.json sur le bus Kilo
    signals = []
    if os.path.exists(KILO_BUS):
        for f in os.listdir(KILO_BUS):
            if f.endswith("-completed.json"):
                signals.append(os.path.join(KILO_BUS, f))

    if not signals:
        print("[BUS-COURIER] Aucun signal a relayer sur le bus Kilo", flush=True)
        print("[BUS-COURIER] Relai termine - 0 signaux traites", flush=True)
        sys.exit(0)

    for signal_path in signals:
        valid, reason = validate_signal_structure(signal_path)
        if not valid:
            print(f"[BUS-COURIER] SIGNAL INVALIDE {os.path.basename(signal_path)}: {reason}", flush=True)
            continue
        print(f"[BUS-COURIER] Signal valide: {os.path.basename(signal_path)}", flush=True)

        # Pontage WAZAA
        try:
            dest = bridge_to_wazaa(signal_path)
            print(f"[BUS-COURIER] LIVRE vers WAZAA: {dest}", flush=True)
        except Exception as e:
            print(f"[BUS-COURIER] WAZAA indisponible ({e}), fallback WAL 0x243", flush=True)
            wal_path = wal_fallback(signal_path, str(e))
            print(f"[BUS-COURIER] FALLBACK WAL 0x243: {wal_path}", flush=True)

    print("[BUS-COURIER] Relai termine", flush=True)
    sys.exit(0)


if __name__ == "__main__":
    main()

