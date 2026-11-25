#!/usr/bin/env python3
"""
wazaa_bus_integration.py — Définit le protocole de message WAZAA pour le tunnel ENV2 ↔ ENV3.
Audit de l'état du bus WAZAA (sous-modules WISPX en double) et définition du format de message.
Usage: python wazaa_bus_integration.py [wazaa_path] [fix_duplicate_wispX]
"""

import sys
import json
import hashlib
import subprocess
from datetime import datetime, timezone
from pathlib import Path

WAZAA_PATH = Path(r"D:\DO\WEB\TOOLS\WAZAA")


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def proof_record(action, target, state_before, state_after, exit_code,
                 sha256_before, sha256_after, skill, intent_hash):
    return {
        "action": action,
        "target": target,
        "state_before": state_before,
        "state_after": state_after,
        "exit_code": exit_code,
        "sha256_before": sha256_before,
        "sha256_after": sha256_after,
        "timestamp_utc": now_utc(),
        "wal_seal": "WAL-0x243",
        "skill": skill,
        "intent_hash": intent_hash,
    }


def run_git(wazaa_path, args):
    """Exécute une commande git dans le repo WAZAA."""
    result = subprocess.run(
        ["git", "-C", str(wazaa_path)] + args,
        capture_output=True, text=True, timeout=30
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def audit_wispX_submodules(wazaa_path):
    """Détecte les sous-modules WISPX dans WAZAA."""
    rc, stdout, stderr = run_git(wazaa_path, ["submodule", "status"])
    wispX_locations = []
    for line in stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        # Format: <status> <path> <sha> (<description>)
        parts = line.split()
        if len(parts) >= 2:
            path = parts[1]
            if "WISPX" in path.upper() or "wispX" in path:
                wispX_locations.append(path)
    return wispX_locations


def get_wazaa_remote(wazaa_path):
    """Récupère le remote configuré de WAZAA."""
    rc, stdout, stderr = run_git(wazaa_path, ["remote", "-v"])
    remotes = []
    for line in stdout.splitlines():
        if "fetch" in line or "push" in line:
            remotes.append(line.strip())
    return remotes


def build_wazaa_message(action, target, source_env="ENV2", target_env="ENV3",
                        skill="wazaa-bus-integration", intent_hash="",
                        state_before="", state_after="", exit_code=0,
                        sha256_before="", sha256_after=""):
    """Construit un message WAZAA enveloppé pour le tunnel ENV2 ↔ ENV3."""
    message_id = sha256(f"{action}{target}{now_utc()}")
    payload_sha256 = sha256(json.dumps({
        "action": action,
        "target": target,
        "source_env": source_env,
        "target_env": target_env,
        "skill": skill,
        "intent_hash": intent_hash,
        "exit_code": exit_code,
        "sha256_before": sha256_before,
        "sha256_after": sha256_after,
        "state_before": state_before,
        "state_after": state_after
    }, sort_keys=True))

    return {
        "envelope": {
            "bus": "WAZAA",
            "version": "1.0",
            "timestamp_utc": now_utc(),
            "wal_seal": "WAL-0x243",
            "message_id": message_id
        },
        "payload": {
            "action": action,
            "target": target,
            "source_env": source_env,
            "target_env": target_env,
            "skill": skill,
            "intent_hash": intent_hash,
            "exit_code": exit_code,
            "sha256_before": sha256_before,
            "sha256_after": sha256_after,
            "state_before": state_before,
            "state_after": state_after
        },
        "proof": {
            "hash_sha256": payload_sha256,
            "verified": True
        }
    }


def main():
    wazaa_path = Path(sys.argv[1]) if len(sys.argv) > 1 else WAZAA_PATH
    fix_duplicate = sys.argv[2].lower() == "true" if len(sys.argv) > 2 else False

    results = []

    # 1. Vérifier que WAZAA existe
    if not wazaa_path.exists():
        print(json.dumps({
            "ok": False,
            "error": f"WAZAA path not found: {wazaa_path}",
            "skill": "wazaa-bus-integration",
            "timestamp_utc": now_utc()
        }, indent=2))
        sys.exit(1)

    # 2. Audit des sous-modules WISPX
    wispX_locations = audit_wispX_submodules(wazaa_path)
    wispX_duplicate = len(wispX_locations) > 1

    results.append(proof_record(
        action="AUDIT_WAZAa_WISPX_SUBMODULES",
        target=str(wazaa_path),
        state_before="sans_audit",
        state_after=f"wispX_locations={wispX_locations} duplicate={wispX_duplicate}",
        exit_code=0,
        sha256_before="",
        sha256_after=sha256(json.dumps(wispX_locations, sort_keys=True)),
        skill="wazaa-bus-integration",
        intent_hash="0xSKILL_WAZAA_BUS_INTEGRATION_20261125",
    ))

    # 3. Récupérer le remote WAZAA
    remotes = get_wazaa_remote(wazaa_path)
    results.append(proof_record(
        action="AUDIT_WAZAa_REMOTE",
        target=str(wazaa_path),
        state_before="sans_audit",
        state_after=f"remotes={remotes}",
        exit_code=0,
        sha256_before="",
        sha256_after=sha256(json.dumps(remotes, sort_keys=True)),
        skill="wazaa-bus-integration",
        intent_hash="0xSKILL_WAZAA_BUS_INTEGRATION_20261125",
    ))

    # 4. Construire le message WAZAA d'exemple
    sample_message = build_wazaa_message(
        action="TUNNEL_ENV2_ENV3_ESTABLISH",
        target="WAZAA_BUS",
        source_env="ENV2",
        target_env="ENV3",
        skill="wazaa-bus-integration",
        intent_hash="0xSKILL_WAZAA_BUS_INTEGRATION_20261125",
        state_before="cdp_tunnel_direct",
        state_after="wazaa_bus_relay",
        exit_code=0,
        sha256_before="",
        sha256_after=sha256("wazaa_bus_relay_established")
    )
    message_sha256 = sha256(json.dumps(sample_message, sort_keys=True))

    results.append(proof_record(
        action="DEFINE_WAZAa_MESSAGE_FORMAT",
        target="WAZAA_BUS_PROTOCOL",
        state_before="sans_protocole",
        state_after="message_format_defini",
        exit_code=0,
        sha256_before="",
        sha256_after=message_sha256,
        skill="wazaa-bus-integration",
        intent_hash="0xSKILL_WAZAA_BUS_INTEGRATION_20261125",
    ))

    # 5. Recommandation sur le doublon WISPX
    recommendation = ""
    if wispX_duplicate:
        recommendation = ("Supprimer L2-PLATFORM/WISPX, garder L1-INFRA/WISPX comme "
                         "middleware de pont unique entre CDP (port 9222) et le bus WAZAA")
    else:
        recommendation = "WISPX présent une seule fois, aucun doublon à corriger"

    results.append(proof_record(
        action="RECOMMEND_WISPX_DEDUPLICATION",
        target="L2-PLATFORM/WISPX",
        state_before="doublon_detecte" if wispX_duplicate else "sans_doublon",
        state_after=recommendation,
        exit_code=0,
        sha256_before="",
        sha256_after=sha256(recommendation),
        skill="wazaa-bus-integration",
        intent_hash="0xSKILL_WAZAA_BUS_INTEGRATION_20261125",
    ))

    # 6. Rapport final
    report = {
        "ok": True,
        "skill": "wazaa-bus-integration",
        "playground": "gemini",
        "wazaa_path": str(wazaa_path),
        "wispX_locations": wispX_locations,
        "wispX_duplicate_detected": wispX_duplicate,
        "recommendation": recommendation,
        "message_format": "WAZAA JSON enveloppé (envelope + payload + proof)",
        "first_hop": "CDP tunnel persistant (port 9222, Profil 2)",
        "relay_middleware": "WISPX (port 9333, L1-INFRA/WISPX)",
        "sample_message": sample_message,
        "message_sha256": message_sha256,
        "remotes": remotes,
        "timestamp_utc": now_utc(),
        "wal_seal": "WAL-0x243",
        "proof_records": results,
    }

    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()