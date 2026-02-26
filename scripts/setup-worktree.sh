#!/bin/bash
# scripts/setup-worktree.sh
# [[scripts.setup-worktree]]
# https://github.com/Mjvolk3/Swanki/tree/main/scripts/setup-worktree.sh

# One-command setup for new git worktrees

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}Setting up worktree...${NC}"

# Get the main repo path dynamically (works across all devices)
# git rev-parse --git-common-dir returns the shared .git directory (always in main repo)
MAIN_REPO="$(cd "$(git rev-parse --git-common-dir)/.." && pwd)"
WORKTREE_DIR="$(pwd)"

echo -e "\n${BLUE}1. Setting up .env file (worktree-specific)...${NC}"

# Function to update env var paths
update_env_paths() {
    local env_file="$1"

    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS sed requires '' after -i
        sed -i '' "s|^ASSET_IMAGES_DIR=.*|ASSET_IMAGES_DIR=\"$WORKTREE_DIR/notes/assets/images\"|" "$env_file"
        sed -i '' "s|^WORKSPACE_DIR=.*|WORKSPACE_DIR=\"$WORKTREE_DIR\"|" "$env_file"
    else
        # Linux sed doesn't need '' after -i
        sed -i "s|^ASSET_IMAGES_DIR=.*|ASSET_IMAGES_DIR=\"$WORKTREE_DIR/notes/assets/images\"|" "$env_file"
        sed -i "s|^WORKSPACE_DIR=.*|WORKSPACE_DIR=\"$WORKTREE_DIR\"|" "$env_file"
    fi
}

if [ -f .env ] && [ ! -L .env ]; then
    echo "  ✓ .env file already exists (not a symlink)"
    echo "  → Updating worktree-specific paths..."
    update_env_paths ".env"
    echo "  ✓ Updated paths to point to worktree"
elif [ -L .env ]; then
    echo "  ! .env is a symlink - removing and creating worktree-specific copy"
    rm .env
    cp "$MAIN_REPO/.env" .env
    update_env_paths ".env"
    echo "  ✓ Created worktree-specific .env"
elif [ -f "$MAIN_REPO/.env" ]; then
    echo "  → Creating new .env from main repo template..."
    cp "$MAIN_REPO/.env" .env
    update_env_paths ".env"
    echo "  ✓ Created worktree-specific .env"
else
    echo "  ℹ No .env in main repo to copy (skipping)"
fi

echo "  → Worktree-specific paths configured:"
echo "    - ASSET_IMAGES_DIR → $WORKTREE_DIR/notes/assets/images"
echo "    - WORKSPACE_DIR → $WORKTREE_DIR"

echo -e "\n${BLUE}2. Verifying Python environment...${NC}"
if command -v conda &> /dev/null; then
    if conda env list | grep -q "^swanki "; then
        echo "  ✓ swanki conda environment exists"
        CONDA_PYTHON=$(conda run -n swanki which python 2>/dev/null || echo "")
        if [ -n "$CONDA_PYTHON" ]; then
            echo "  → Python: $CONDA_PYTHON"
            conda run -n swanki python --version
        fi
    else
        echo "  ℹ swanki conda environment not found"
        echo "  → Create it with: conda create -n swanki python=3.11 -y"
    fi
else
    echo "  ℹ conda not found in PATH"
fi

echo -e "\n${BLUE}3. Configuring VS Code for worktree...${NC}"
# Create .env.vscode for PYTHONPATH override (if not exists)
if [ ! -f .env.vscode ]; then
    echo "  Creating .env.vscode with PYTHONPATH..."
    echo "PYTHONPATH=$WORKTREE_DIR:\${PYTHONPATH}" > .env.vscode
    echo "  ✓ Created .env.vscode"
else
    echo "  ✓ .env.vscode already exists"
fi

echo -e "\n${BLUE}4. Sharing Claude Code auto memory with main repo...${NC}"
# Claude Code stores per-project auto memory at ~/.claude/projects/<encoded-path>/memory/
# The encoding replaces / and . with - in the absolute path.
# Worktrees get separate memory dirs by default, but we want to share the main repo's memory.
CLAUDE_PROJECTS_DIR="$HOME/.claude/projects"
MAIN_CLAUDE_DIR="$CLAUDE_PROJECTS_DIR/$(echo "$MAIN_REPO" | tr '/.' '-')"
WT_CLAUDE_DIR="$CLAUDE_PROJECTS_DIR/$(echo "$WORKTREE_DIR" | tr '/.' '-')"
MAIN_MEMORY="$MAIN_CLAUDE_DIR/memory"
WT_MEMORY="$WT_CLAUDE_DIR/memory"

# Ensure main repo memory dir exists
mkdir -p "$MAIN_MEMORY"

if [ -L "$WT_MEMORY" ]; then
    echo "  ✓ memory/ symlink already exists → $(readlink "$WT_MEMORY")"
elif [ -d "$WT_MEMORY" ]; then
    if [ -z "$(ls -A "$WT_MEMORY")" ]; then
        rmdir "$WT_MEMORY"
        ln -s "$MAIN_MEMORY" "$WT_MEMORY"
        echo "  ✓ Replaced empty memory/ dir with symlink → $MAIN_MEMORY"
    else
        echo -e "  ${YELLOW}Warning: memory/ directory has content (not replacing)${NC}"
        echo "    To share memory, merge contents then: rm -rf $WT_MEMORY && ln -s $MAIN_MEMORY $WT_MEMORY"
    fi
else
    mkdir -p "$WT_CLAUDE_DIR"
    ln -s "$MAIN_MEMORY" "$WT_MEMORY"
    echo "  ✓ Created symlink: memory/ → $MAIN_MEMORY"
fi

echo -e "\n${BLUE}5. Installing pre-commit hooks...${NC}"
if command -v pre-commit &> /dev/null; then
    pre-commit install
    echo "  ✓ pre-commit hooks installed"
else
    echo "  ✗ pre-commit not found — install with: pip install pre-commit"
fi

echo -e "\n${GREEN}✓ Worktree setup complete!${NC}"
echo -e "\n${BLUE}How this works:${NC}"
echo "  - .env is COPIED (not symlinked) from main repo with worktree-specific overrides"
echo "  - .env.vscode sets PYTHONPATH to prioritize this worktree's code"
echo "  - Claude Code auto memory symlinked to main repo (shared across worktrees)"
echo "  - Other worktrees and main repo are NOT affected"
echo -e "\n${BLUE}Verify worktree is active:${NC}"
echo "  python -c 'import swanki; print(swanki.__file__)'"
echo "  (should show path to this worktree, not main repo)"
