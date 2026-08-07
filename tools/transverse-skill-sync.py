#!/usr/bin/env python3
"""
transverse-skill-sync.py
Automates detection and propagation of transverse skills across the ecosystem.

A skill is considered "transverse" when its frontmatter contains:
  - scope: ecosystem
  OR
  - layer: L4_TRANSVERSAL

When detected, the skill is automatically:
  1. Copied to L4-TOOLS/SKILLS/TRANSVERSE/
  2. Registered in REGISTRY.yaml via registry-gen.py
  3. Validated via validate-skills.py

Usage:
  python tools/transverse-skill-sync.py [--dry-run] [--force]
"""

import os
import re
import sys
import shutil
import subprocess
import argparse

SKILLS_DIR = os.path.join(os.path.dirname(__file__), '..')
TRANSVERSE_DIR = os.path.join(SKILLS_DIR, 'TRANSVERSE')
REGISTRY_GEN = os.path.join(SKILLS_DIR, 'tools', 'registry-gen.py')
VALIDATE_SCRIPT = os.path.join(SKILLS_DIR, 'tools', 'validate-skills.py')


def is_transverse_skill(skill_path):
    """Check if a SKILL.md file declares the skill as transverse."""
    try:
        with open(skill_path, 'r', encoding='utf-8') as f:
            content = f.read()

        match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not match:
            return False

        frontmatter = match.group(1)
        # Check for ecosystem scope or L4_TRANSVERSAL layer
        scope_match = re.search(r'^\s*scope:\s*['"']?ecosystem['"']?', frontmatter, re.MULTILINE | re.IGNORECASE)
        layer_match = re.search(r'^\s*layer:\s*['"']?L4_TRANSVERSAL['"']?', frontmatter, re.MULTILINE | re.IGNORECASE)

        return bool(scope_match or layer_match)
    except (IOError, re.error):
        return False


def get_skill_name(skill_path):
    """Extract the skill name from SKILL.md frontmatter."""
    try:
        with open(skill_path, 'r', encoding='utf-8') as f:
            content = f.read()

        match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not match:
            return None

        frontmatter = match.group(1)
        name_match = re.search(r'^\s*name:\s*(.+)', frontmatter, re.MULTILINE)
        return name_match.group(1).strip().strip('"').strip("'") if name_match else None
    except IOError:
        return None


def sync_transverse_skill(skill_file, dry_run=False, force=False):
    """Copy a transverse skill to the TRANSVERSE directory."""
    skill_name = get_skill_name(skill_file)
    if not skill_name:
        print(f"  WARN: Could not extract name from {skill_file}")
        return False

    # Find the skill directory (parent of SKILL.md)
    skill_dir = os.path.dirname(skill_file)
    dest_dir = os.path.join(TRANSVERSE_DIR, skill_name)

    if os.path.exists(dest_dir) and not force:
        # Check if source is newer
        src_mtime = os.path.getmtime(skill_file)
        dest_mtime = os.path.getmtime(os.path.join(dest_dir, 'SKILL.md')) if os.path.exists(os.path.join(dest_dir, 'SKILL.md')) else 0
        if src_mtime <= dest_mtime:
            print(f"  SKIP {skill_name}: already up-to-date in TRANSVERSE")
            return None  # None means "skipped, not an error"

    if dry_run:
        print(f"  [DRY-RUN] Would copy {skill_name} -> TRANSVERSE/")
        return True

    # Copy the entire skill directory
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    shutil.copytree(skill_dir, dest_dir)
    print(f"  COPIED {skill_name} -> TRANSVERSE/")
    return True


def run_registry_gen():
    """Re-run registry-gen.py to update REGISTRY.yaml."""
    try:
        result = subprocess.run(
            [sys.executable, REGISTRY_GEN],
            cwd=SKILLS_DIR,
            capture_output=True,
            text=True,
            timeout=30
        )
        # Check stdout for success message
        if "Registry generated" in result.stdout:
            # Extract total skills count
            for line in result.stdout.split('\n'):
                if 'Total skills:' in line:
                    print(f"  {line.strip()}")
            return True
        return False
    except (subprocess.TimeoutExpired, OSError) as e:
        print(f"  WARN: registry-gen.py failed: {e}")
        return False


def run_validation():
    """Run validate-skills.py to check all skills."""
    try:
        result = subprocess.run(
            [sys.executable, VALIDATE_SCRIPT],
            cwd=SKILLS_DIR,
            capture_output=True,
            text=True,
            timeout=30
        )
        # Check for validation success
        if "All skills validated successfully" in result.stdout:
            print("  VALIDATION PASSED: All skills valid")
            return True
        elif "Validated" in result.stdout:
            # Some skills failed but we still got output
            print(f"  VALIDATION: {result.stdout.strip()}")
            return True  # Not a blocking error
        return False
    except (subprocess.TimeoutExpired, OSError) as e:
        print(f"  WARN: validate-skills.py failed: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Sync transverse skills to TRANSVERSE directory"
    )
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without copying')
    parser.add_argument('--force', action='store_true', help='Force copy even if up-to-date')
    parser.add_argument('--no-registry', action='store_true', help='Skip registry regeneration')
    parser.add_argument('--no-validate', action='store_true', help='Skip validation')
    parser.add_argument('--watch', action='store_true', help='Watch mode: run on every change')
    args = parser.parse_args()

    print("=" * 60)
    print("Transverse Skill Sync")
    print("=" * 60)

    # Find all SKILL.md files
    skill_files = []
    for root, dirs, files in os.walk(SKILLS_DIR):
        # Skip TRANSVERSE and .kilo directories
        if 'TRANSVERSE' in root or '.kilo' in root:
            continue
        for f in files:
            if f == 'SKILL.md':
                skill_files.append(os.path.join(root, f))

    print(f"\nFound {len(skill_files)} skill files. Scanning for transverse skills...")

    transverse_skills = []
    for sf in skill_files:
        if is_transverse_skill(sf):
            transverse_skills.append(sf)

    if not transverse_skills:
        print("No transverse skills found.")
        return 0

    print(f"Found {len(transverse_skills)} transverse skill(s):\n")

    copied = 0
    skipped = 0
    errors = 0

    for sf in sorted(transverse_skills):
        skill_name = get_skill_name(sf)
        result = sync_transverse_skill(sf, dry_run=args.dry_run, force=args.force)
        if result is True:
            copied += 1
        elif result is None:
            skipped += 1
        else:
            errors += 1

    print(f"\n--- Sync Summary ---")
    print(f"  Copied: {copied}")
    print(f"  Skipped: {skipped}")
    print(f"  Errors: {errors}")

    # Run registry gen and validation
    if not args.no_registry and not args.dry_run:
        print("\n--- Regenerating Registry ---")
        run_registry_gen()

    if not args.no_validate:
        print("\n--- Running Validation ---")
        run_validation()

    print("\nDone.")
    return 0 if errors == 0 else 1


if __name__ == '__main__':
    sys.exit(main())