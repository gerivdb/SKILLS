#!/bin/sh
# install-hooks.sh — SKILLS
# Active les githooks du repo
# Usage: sh .githooks/install-hooks.sh

git config core.hooksPath .githooks
echo '[SKILLS] Hooks actives: .githooks/'
echo '  - pre-commit: frontmatter skills + REGISTRY.yaml sync + encoding'
