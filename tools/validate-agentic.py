#!/usr/bin/env python3
"""Validate agentic skills frontmatter and structure (v2)."""

import json
import os
import re
import sys

SKILLS_DIR = os.path.join(os.path.dirname(__file__), '..', 'perplexity', 'skills')
MANIFEST_PATH = os.path.join(os.path.dirname(__file__), '..', 'MANIFEST.json')

REQUIRED_FIELDS = ['name', 'version', 'description', 'layer', 'nexusTags', 'slotWeight', 'status']
AGENTIC_REQUIRED_FIELDS = ['triggers', 'prerequisites', 'changelog']
VALID_STATUSES = ['active', 'deprecated', 'archived', 'pending']
VALID_LAYERS = ['L0_GOVERNANCE', 'L1_CAUSALITY', 'L2_PRODUCTION', 'L2_COMPOSITION',
                'L2_RESILIENCE', 'L3_EMERGENCE', 'L4_ORCHESTRATION', 'L5_META',
                'L0_UNKNOWN']


def validate_agentic_skill(skill_path):
    """Validate an agentic skill has all required fields."""
    errors = []
    with open(skill_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        errors.append(f"Missing YAML frontmatter")
        return errors

    import yaml
    try:
        frontmatter = yaml.safe_load(match.group(1))
    except yaml.YAMLError as e:
        errors.append(f"Invalid YAML: {e}")
        return errors

    if not isinstance(frontmatter, dict):
        errors.append("Frontmatter is not a YAML mapping")
        return errors

    # Check required fields
    for field in REQUIRED_FIELDS + AGENTIC_REQUIRED_FIELDS:
        if field not in frontmatter:
            errors.append(f"Missing required field: {field}")

    # Check status
    if frontmatter.get('status') not in VALID_STATUSES:
        errors.append(f"Invalid status: {frontmatter.get('status')}")

    # Check layer
    if frontmatter.get('layer') not in VALID_LAYERS:
        errors.append(f"Invalid layer: {frontmatter.get('layer')}")

    # Check triggers (must have at least 3 for agentic skills)
    triggers = frontmatter.get('triggers', [])
    if isinstance(triggers, list) and len(triggers) < 3:
        errors.append(f"Agentic skill should have at least 3 triggers (found {len(triggers)})")

    # Check version format (semver)
    version = frontmatter.get('version', '')
    if not re.match(r'^\d+\.\d+\.\d+$', str(version)):
        errors.append(f"Invalid version format: {version} (expected semver)")

    # Check changelog
    changelog = frontmatter.get('changelog', [])
    if not isinstance(changelog, list) or len(changelog) == 0:
        errors.append("Changelog must be a non-empty list")

    return errors


def validate_v2_specific(skill_path, skill_name):
    """Validate v2-specific patterns: Draft, Gap Analyzer, Delegation, Rewriter."""
    errors = []
    with open(skill_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # v2 skills should have version 2.x.x
    import yaml
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if match:
        frontmatter = yaml.safe_load(match.group(1))
        version = frontmatter.get('version', '1.0.0')
        if not version.startswith('2.'):
            errors.append(f"v2 skill should have version 2.x.x (found {version})")

    # Check for v2-specific sections
    if skill_name == 'skills-coverage':
        if 'Draft Agent' not in content and 'draft' not in content.lower():
            errors.append("v2 coverage skill missing 'Draft Agent' section")
        if 'Gap Analyzer' not in content and 'gap analyzer' not in content.lower():
            errors.append("v2 coverage skill missing 'Gap Analyzer' section")
        if 'feedback ciblé' not in content.lower() and 'targeted feedback' not in content.lower():
            errors.append("v2 coverage skill missing 'feedback ciblé' / 'targeted feedback' section")

    if skill_name == 'skills-agentic':
        if 'DELEGATOR' not in content and 'delegator' not in content.lower():
            errors.append("v2 agentic skill missing 'DELEGATOR' section")
        if 'REWRITER' not in content and 'rewriter' not in content.lower():
            errors.append("v2 agentic skill missing 'REWRITER' section")
        if 'niveau' not in content.lower() and 'level' not in content.lower():
            errors.append("v2 agentic skill missing delegation levels (niveau 1/2/3)")

    if skill_name == 'skills-rewriter':
        if 'sous-quête' not in content.lower() and 'sub_query' not in content.lower() and 'sub-query' not in content.lower():
            errors.append("rewriter skill missing 'sous-quêtes' / 'sub-queries' section")
        if 'reformul' not in content.lower():
            errors.append("rewriter skill missing 'reformulation' section")

    if skill_name == 'skills-agentic-test':
        if 'v2' not in content.lower() and 'F1' not in content:
            errors.append("v2 test skill missing v2 test queries (Category F/G/H)")
        if 'délégation' not in content.lower() and 'delegation' not in content.lower():
            errors.append("v2 test skill missing delegation tests")
        if 'brouillon' not in content.lower() and 'draft' not in content.lower():
            errors.append("v2 test skill missing draft tests")

    return errors


def main():
    errors = []

    # Load manifest
    with open(MANIFEST_PATH, 'r', encoding='utf-8') as f:
        manifest = json.load(f)

    # Find agentic skills in manifest
    agentic_skills = [s for s in manifest.get('skills', [])
                      if 'SKILLS_AGENTIC' in str(s.get('nexusTags', []))]

    print(f"Found {len(agentic_skills)} agentic skills in manifest")

    for skill in agentic_skills:
        skill_name = skill['name']
        skill_path = os.path.join(SKILLS_DIR, f"{skill_name}.md")

        if not os.path.exists(skill_path):
            errors.append(f"Agentic skill '{skill_name}' in manifest but file not found: {skill_path}")
            continue

        # v1 validation
        skill_errors = validate_agentic_skill(skill_path)
        if skill_errors:
            errors.append(f"Agentic skill '{skill_name}' (v1 validation):")
            for err in skill_errors:
                errors.append(f"  - {err}")

        # v2 validation
        v2_errors = validate_v2_specific(skill_path, skill_name)
        if v2_errors:
            errors.append(f"Agentic skill '{skill_name}' (v2 validation):")
            for err in v2_errors:
                errors.append(f"  - {err}")

    if errors:
        print("VALIDATION FAILED:")
        for err in errors:
            print(f"  ❌ {err}")
        sys.exit(1)
    else:
        print("✅ All agentic skills validated successfully (v1 + v2)")
        sys.exit(0)


if __name__ == '__main__':
    main()
