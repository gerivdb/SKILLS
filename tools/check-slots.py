#!/usr/bin/env python3
"""Check slot count against maximum."""

import argparse
import json
import os
import sys

MANIFEST_PATH = os.path.join(os.path.dirname(__file__), '..', 'MANIFEST.json')


def main():
    parser = argparse.ArgumentParser(description='Check skill slot count')
    parser.add_argument('--max', type=int, default=100, help='Maximum slot count')
    args = parser.parse_args()

    with open(MANIFEST_PATH, 'r', encoding='utf-8') as f:
        manifest = json.load(f)

    count = manifest.get('skillsCount', len(manifest.get('skills', [])))
    active_count = len([s for s in manifest.get('skills', [])
                        if s.get('status') == 'active'])

    print(f"Total skills in manifest: {count}")
    print(f"Active skills: {active_count}")
    print(f"Maximum allowed: {args.max}")
    print(f"Remaining slots: {args.max - active_count}")

    if active_count > args.max:
        print(f"❌ Slot count ({active_count}) exceeds maximum ({args.max})")
        sys.exit(1)
    else:
        print(f"✅ Slot count within limit ({active_count}/{args.max})")
        sys.exit(0)


if __name__ == '__main__':
    main()
