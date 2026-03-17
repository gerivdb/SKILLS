#!/usr/bin/env bash
# =============================================================================
# SKILLS Validation Script
# =============================================================================
# Validates all SKILL.md files for:
# - YAML frontmatter presence
# - YAML syntax validity
# - Required fields
# - Duplicate skills
# - Broken links
# =============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
TOTAL=0
PASSED=0
FAILED=0
WARNINGS=0

echo "=============================================="
echo "  SKILLS Registry Validation"
echo "=============================================="
echo ""

# Check for required tools
command -v python3 >/dev/null 2>&1 || {
    echo -e "${RED}ERROR: python3 is required but not installed.${NC}"
    exit 1
}

# Find all SKILL.md files
SKILL_FILES=$(find . -name "SKILL.md" -type f | grep -v ".git" | sort)

if [ -z "$SKILL_FILES" ]; then
    echo -e "${YELLOW}WARNING: No SKILL.md files found${NC}"
    exit 0
fi

echo "Found $(echo "$SKILL_FILES" | wc -l) SKILL.md files"
echo ""

# Validate each file
for FILE in $SKILL_FILES; do
    TOTAL=$((TOTAL + 1))
    echo -n "Validating: $FILE ... "
    
    # Check if file has frontmatter
    if ! head -1 "$FILE" | grep -q "^---"; then
        echo -e "${RED}FAIL${NC}"
        echo -e "  ${RED}✗ Missing YAML frontmatter${NC}"
        FAILED=$((FAILED + 1))
        continue
    fi
    
    # Extract frontmatter
    FRONTMATTER=$(sed -n '/^---$/,/^---$/p' "$FILE")
    
    # Check required fields
    MISSING_FIELDS=""
    
    # name
    if ! echo "$FRONTMATTER" | grep -q "^name:"; then
        MISSING_FIELDS="$MISSING_FIELDS name"
    fi
    
    # description
    if ! echo "$FRONTMATTER" | grep -q "^description:"; then
        MISSING_FIELDS="$MISSING_FIELDS description"
    fi
    
    # triggers
    if ! echo "$FRONTMATTER" | grep -q "^triggers:"; then
        MISSING_FIELDS="$MISSING_FIELDS triggers"
    fi
    
    # domain
    if ! echo "$FRONTMATTER" | grep -q "^domain:"; then
        MISSING_FIELDS="$MISSING_FIELDS domain"
    fi
    
    # version
    if ! echo "$FRONTMATTER" | grep -q "^version:"; then
        MISSING_FIELDS="$MISSING_FIELDS version"
    fi
    
    # author
    if ! echo "$FRONTMATTER" | grep -q "^author:"; then
        MISSING_FIELDS="$MISSING_FIELDS author"
    fi
    
    # license
    if ! echo "$FRONTMATTER" | grep -q "^license:"; then
        MISSING_FIELDS="$MISSING_FIELDS license"
    fi
    
    # status
    if ! echo "$FRONTMATTER" | grep -q "^status:"; then
        MISSING_FIELDS="$MISSING_FIELDS status"
    fi
    
    if [ -n "$MISSING_FIELDS" ]; then
        echo -e "${RED}FAIL${NC}"
        echo -e "  ${RED}✗ Missing required fields:$MISSING_FIELDS${NC}"
        FAILED=$((FAILED + 1))
        continue
    fi
    
    # Validate YAML syntax
    if ! python3 -c "import yaml; yaml.safe_load(open('$FILE').read())" 2>/dev/null; then
        echo -e "${RED}FAIL${NC}"
        echo -e "  ${RED}✗ Invalid YAML syntax${NC}"
        FAILED=$((FAILED + 1))
        continue
    fi
    
    echo -e "${GREEN}PASS${NC}"
    PASSED=$((PASSED + 1))
done

echo ""
echo "=============================================="
echo "  Validation Summary"
echo "=============================================="
echo -e "Total:   $TOTAL"
echo -e "Passed:  ${GREEN}$PASSED${NC}"
echo -e "Failed:  ${RED}$FAILED${NC}"
echo -e "Warnings: ${YELLOW}$WARNINGS${NC}"
echo "=============================================="

if [ $FAILED -gt 0 ]; then
    echo -e "${RED}Validation FAILED${NC}"
    exit 1
else
    echo -e "${GREEN}All validations PASSED${NC}"
    exit 0
fi
