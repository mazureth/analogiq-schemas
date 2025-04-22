#!/bin/bash
# Install Git hooks for this repository

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Get the repository root directory
REPO_ROOT=$(git rev-parse --show-toplevel)

# Check if we're in a Git repository
if [ ! -d "$REPO_ROOT/.git" ]; then
    echo -e "${RED}Error: Not in a Git repository${NC}"
    exit 1
fi

HOOKS_DIR="$REPO_ROOT/.git/hooks"
SOURCE_DIR="$REPO_ROOT/hooks"

# Install pre-commit hook
echo -e "${YELLOW}Installing pre-commit hook...${NC}"

# Check if file already exists
if [ -f "$HOOKS_DIR/pre-commit" ]; then
    echo -e "${YELLOW}A pre-commit hook already exists.${NC}"
    read -p "Do you want to overwrite it? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Hook installation cancelled.${NC}"
        exit 0
    fi
fi

# Copy the pre-commit hook
cp "$SOURCE_DIR/pre-commit" "$HOOKS_DIR/pre-commit"
chmod +x "$HOOKS_DIR/pre-commit"

echo -e "${GREEN}Pre-commit hook installed successfully!${NC}"
echo -e "${YELLOW}The hook will validate unit files before each commit.${NC}"
echo -e "${YELLOW}If validation fails, the commit will be aborted.${NC}"

exit 0 