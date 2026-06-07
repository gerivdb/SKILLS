#!/usr/bin/env python3
"""
generate_coords.py — Génère TAXONOMY/coords.yaml depuis MANIFEST.json

Algorithme:
  1. Lire MANIFEST.json
  2. Pour chaque skill, extraire les coordonnées UAE depuis le frontmatter
     ou les déduire du nom/descriptions
  3. Calculer le score UAE = 1/sqrt(d) (distance au centre du plateau 5D)
  4. Attribuer la zone LADYBIRD/STANDARD/BASIC
  5. Ecrire TAXONOMY/coords.yaml

Usage:
  python scripts/generate_coords.py [--check]
"""

import json
import math
import os
import sys
import yaml

# Force UTF-8 output on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

MANIFEST_PATH = os.path.join(os.path.dirname(__file__), '..', 'MANIFEST.json')
COORDS_PATH = os.path.join(os.path.dirname(__file__), '..', 'TAXONOMY', 'coords.yaml')

# Mapping des strates numériques pour le calcul de distance
STRATE_MAP = {'L0': 0, 'L1': 1, 'L2': 2, 'L3': 3, 'L4': 4, 'L5': 5}
DOMAINE_MAP = {
    'governance': 0, 'sot': 1, 'cognition': 2, 'automation': 3,
    'git': 4, 'agentic': 5, 'domain': 6, 'external': 7
}
ENV_MAP = {'ENV1': 0, 'ENV2': 1, 'BOTH': 2}
PHASE_MAP = {'create': 0, 'audit': 1, 'fix': 2, 'close': 3, 'route': 4}
URGENCE_MAP = {'P0': 0, 'P1': 1, 'P2': 2, 'P3': 3}

# Centres multi-poles pour le scoring UAE
# Le score est la distance minimale a l'un des centres optimaux
CENTERS = [
    (0.0, 0.0, 1.0, 1.0, 1.0),  # L0 governance audit P1 (centre gouvernance)
    (4.0, 5.0, 1.0, 4.0, 0.0),  # L4 agentic route P0 (centre orchestration)
]


def compute_uae_score(strate, domaine, env, phase, urgence):
    """Calcule le score UAE = 100 * (1 - d_min/d_max) ou d_min est la distance au centre le plus proche."""
    s = STRATE_MAP.get(strate, 2.5)
    d = DOMAINE_MAP.get(domaine, 3.5)
    e = ENV_MAP.get(env, 1.0)
    p = PHASE_MAP.get(phase, 2.0)
    u = URGENCE_MAP.get(urgence, 1.5)

    point = (s, d, e, p, u)

    # Distance minimale a l'un des centres
    min_distance = float('inf')
    for center in CENTERS:
        dist = math.sqrt(sum((a - b) ** 2 for a, b in zip(point, center)))
        min_distance = min(min_distance, dist)

    # Distance max possible = sqrt(124) = 11.1
    max_distance = math.sqrt(124)
    score = 100.0 * (1.0 - min_distance / max_distance)
    return round(max(score, 0.0), 1)


def get_zone(uae_score):
    """Attribue la zone LADYBIRD/STANDARD/BASIC selon le score."""
    if uae_score >= 80:
        return "LADYBIRD"
    elif uae_score >= 60:
        return "STANDARD"
    else:
        return "BASIC"


def generate_coords():
    """Génère le coords.yaml depuis le MANIFEST.json."""
    with open(MANIFEST_PATH, 'r', encoding='utf-8') as f:
        manifest = json.load(f)

    coords = {'skills': {}}

    for skill in manifest['skills']:
        name = skill['name']
        layer = skill.get('layer', 'L0_UNKNOWN')
        description = skill.get('description', '')

        # Déduire les coordonnées UAE du layer et de la description
        strate = _infer_strate(layer)
        domaine = _infer_domaine(name, description)
        env = _infer_env(name, description)
        phase = _infer_phase(name, description)
        urgence = _infer_urgence(name, description, layer)

        uae_score = compute_uae_score(strate, domaine, env, phase, urgence)
        zone = get_zone(uae_score)

        coords['skills'][name] = {
            'strate': strate,
            'domaine': domaine,
            'env': env,
            'phase': phase,
            'urgence': urgence,
            'uae_score': uae_score,
            'zone': zone
        }

    return coords


def _infer_strate(layer):
    """Déduit la strate du layer MANIFEST."""
    if layer.startswith('L0'):
        return 'L0'
    elif layer.startswith('L1'):
        return 'L1'
    elif layer.startswith('L2'):
        return 'L2'
    elif layer.startswith('L3'):
        return 'L3'
    elif layer.startswith('L4'):
        return 'L4'
    elif layer.startswith('L5'):
        return 'L5'
    return 'L0'


def _infer_domaine(name, description):
    """Déduit le domaine du nom et de la description."""
    text = (name + ' ' + description).lower()
    if any(kw in text for kw in ['governance', 'adr', 'nexus', 'compliance', 'scaffold']):
        return 'governance'
    elif any(kw in text for kw in ['agentic', 'orchestrat', 'delegat', 'router', 'rewriter', 'coverage']):
        return 'agentic'
    elif any(kw in text for kw in ['cognit', 'triade', 'reposcope', 'reasoning', 'hitl']):
        return 'cognition'
    elif any(kw in text for kw in ['git', 'github', 'branch', 'commit', 'stash', 'merge', 'rebase']):
        return 'git'
    elif any(kw in text for kw in ['automat', 'workflow', 'pipeline', 'task', 'swarm', 'boinc', 'comet', 'devtools']):
        return 'automation'
    elif any(kw in text for kw in ['vdb', 'tql', 'vector', 'plix', 'base243', 'intent-bridge', 'data-vector']):
        return 'sot'
    elif any(kw in text for kw in ['diagram', 'prd', 'wiki', 'deepwiki', 'infographic', 'mermaid', 'uml', 'vega']):
        return 'domain'
    return 'external'


def _infer_env(name, description):
    """Déduit l'environnement du nom et de la description."""
    text = (name + ' ' + description).lower()
    if 'devtools' in text or 'dev' in text:
        return 'ENV2'
    elif any(kw in text for kw in ['prod', 'cloud', 'deploy']):
        return 'ENV2'
    return 'BOTH'


def _infer_phase(name, description):
    """Déduit la phase du nom et de la description."""
    text = (name + ' ' + description).lower()
    if any(kw in text for kw in ['audit', 'monitor', 'watch', 'scan', 'check', 'validat']):
        return 'audit'
    elif any(kw in text for kw in ['fix', 'repair', 'recover', 'debug', 'reform', 'prune']):
        return 'fix'
    elif any(kw in text for kw in ['close', 'finish', 'end', 'terminat']):
        return 'close'
    elif any(kw in text for kw in ['rout', 'orchestrat', 'delegat', 'syncer']):
        return 'route'
    return 'create'


def _infer_urgence(name, description, layer):
    """Déduit l'urgence du layer et de la description."""
    if layer in ('L4_ORCHESTRATION',):
        return 'P0'
    text = (name + ' ' + description).lower()
    if any(kw in text for kw in ['critical', 'emergency', 'p0']):
        return 'P0'
    elif any(kw in text for kw in ['audit', 'monitor', 'security', 'compliance', 'governance']):
        return 'P1'
    elif any(kw in text for kw in ['automat', 'workflow', 'pipeline', 'git']):
        return 'P2'
    return 'P3'


def write_coords(coords):
    """Écrit le fichier coords.yaml."""
    os.makedirs(os.path.dirname(COORDS_PATH), exist_ok=True)
    with open(COORDS_PATH, 'w', encoding='utf-8') as f:
        f.write('# TAXONOMY/coords.yaml\n')
        f.write('# Généré automatiquement par scripts/generate_coords.py\n')
        f.write('# Ne pas éditer manuellement — relancer le script\n\n')
        yaml.dump(coords, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    print(f"✅ coords.yaml généré: {len(coords['skills'])} skills")


def validate_coords(coords):
    """Valide le coords.yaml généré."""
    errors = []
    for name, coord in coords['skills'].items():
        for field in ['strate', 'domaine', 'env', 'phase', 'urgence']:
            if field not in coord:
                errors.append(f"{name}: champ manquant '{field}'")
        if 'uae_score' not in coord:
            errors.append(f"{name}: score UAE manquant")
        elif not (0 <= coord['uae_score'] <= 100):
            errors.append(f"{name}: score UAE hors limites ({coord['uae_score']})")
        if coord.get('zone') not in ('LADYBIRD', 'STANDARD', 'BASIC'):
            errors.append(f"{name}: zone invalide ({coord.get('zone')})")
    return errors


def check_idempotent():
    """Vérifie que le script est idempotent (2 exécutions = même résultat)."""
    coords1 = generate_coords()
    write_coords(coords1)
    with open(COORDS_PATH, 'r', encoding='utf-8') as f:
        content1 = f.read()
    coords2 = generate_coords()
    write_coords(coords2)
    with open(COORDS_PATH, 'r', encoding='utf-8') as f:
        content2 = f.read()
    if content1 == content2:
        print("✅ Idempotence vérifiée")
        return True
    else:
        print("❌ ERREUR: le script n'est pas idempotent")
        return False


def main():
    if '--check' in sys.argv:
        if not check_idempotent():
            sys.exit(1)
        return

    coords = generate_coords()
    errors = validate_coords(coords)

    if errors:
        print("❌ ERREURS DE VALIDATION:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)

    write_coords(coords)

    # Statistiques
    zones = {}
    strates = {}
    for coord in coords['skills'].values():
        zone = coord['zone']
        strate = coord['strate']
        zones[zone] = zones.get(zone, 0) + 1
        strates[strate] = strates.get(strate, 0) + 1

    print(f"\n📊 Statistiques:")
    print(f"  Total: {len(coords['skills'])} skills")
    for zone in ('LADYBIRD', 'STANDARD', 'BASIC'):
        count = zones.get(zone, 0)
        print(f"  {zone}: {count}")
    for strate in sorted(strates.keys()):
        print(f"  {strate}: {strates[strate]}")


if __name__ == '__main__':
    main()
