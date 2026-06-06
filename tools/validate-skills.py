#!/usr/bin/env python3
"""Validate all skills frontmatter format."""

import os
import re
import sys
import yaml

SKILLS_DIR = os.path.join(os.path.dirname(__file__), '..', 'perplexity', 'skills')

REQUIRED_FIELDS = ['name', 'version', 'description', 'layer', 'nexusTags', 'slotWeight', 'status']
VALID_STATUSES = ['active', 'deprecated', 'archived', 'pending']


def validate_skill(skill_path):
    """Validate a single skill file."""
    errors = []
    with open(skill_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check frontmatter exists
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        errors.append("Missing YAML frontmatter")
        return errors

    # Parse YAML
    try:
        frontmatter = yaml.safe_load(match.group(1))
    except yaml.YAMLError as e:
        errors.append(f"Invalid YAML: {e}")
        return errors

    if not isinstance(frontmatter, dict):
        errors.append("Frontmatter is not a YAML mapping")
        return errors

    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in frontmatter:
            errors.append(f"Missing required field: {field}")

    # Check status
    if frontmatter.get('status') not in VALID_STATUSES:
        errors.append(f"Invalid status: {frontmatter.get('status')}")

    # Check version format
    version = frontmatter.get('version', '')
    if not re.match(r'^\d+\.\d+\.\d+$', str(version)):
        errors.append(f"Invalid version format: {version}")

    return errors


def main():
    errors = []
    skill_count = 0

    for filename in os.listdir(SKILLS_DIR):
        if not filename.endswith('.md'):
            continue
        skill_path = os.path.join(SKILLS_DIR, filename)
        skill_count += 1

        skill_errors = validate_skill(skill_path)
        if skill_errors:
            errors.append(f"{filename}:")
            for err in skill_errors:
                errors.append(f"  - {err}")

    print(f"Validated {skill_count} skills")

    if errors:
        print("VALIDATION FAILED:")
        for err in errors:
            print(f"  ❌ {err}")
        sys.exit(1)
    else:
        print("✅ All skills validated successfully")
        sys.exit(0)


if __name__ == '__main__':
    main()
