#!/usr/bin/env python3
"""
validate_cognitive.py — Validates CognitivePattern YAML files in a given directory.
Usage: python validators/validate_cognitive.py SKILLS/cognitive
Expected output: OK: 6 CognitivePatterns valid
"""
import sys
import os
import yaml

REQUIRED_FIELDS = ["id", "label", "family", "rank", "trigger", "anti_pattern", "applicable_to", "ref"]
EXPECTED_COUNT = 6

def validate_cognitive(directory: str) -> int:
    if not os.path.isdir(directory):
        print(f"ERROR: Directory not found: {directory}", file=sys.stderr)
        return 1

    yaml_files = [f for f in os.listdir(directory) if f.endswith(".yaml") and f != "MANIFEST.yaml"]
    errors = []

    for filename in sorted(yaml_files):
        filepath = os.path.join(directory, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as fh:
                data = yaml.safe_load(fh)
        except yaml.YAMLError as e:
            errors.append(f"{filename}: YAML parse error — {e}")
            continue

        missing = [field for field in REQUIRED_FIELDS if field not in data]
        if missing:
            errors.append(f"{filename}: missing fields {missing}")
            continue

        if data.get("family") != "cognitive":
            errors.append(f"{filename}: family must be 'cognitive', got '{data.get('family')}'")
        if data.get("rank") != "C0":
            errors.append(f"{filename}: rank must be 'C0', got '{data.get('rank')}'")

    if errors:
        for err in errors:
            print(f"FAIL: {err}", file=sys.stderr)
        return 1

    count = len(yaml_files)
    if count != EXPECTED_COUNT:
        print(f"FAIL: expected {EXPECTED_COUNT} CognitivePatterns, found {count}", file=sys.stderr)
        return 1

    print(f"OK: {count} CognitivePatterns valid")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <cognitive_directory>", file=sys.stderr)
        sys.exit(1)
    sys.exit(validate_cognitive(sys.argv[1]))
