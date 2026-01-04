#!/bin/bash
################################################################################
# Environment Reset Script - Phase 5
# Resets main branch to clean state before re-attack phase
################################################################################

set -e  # Exit on error

echo "================================================================================"
echo "ENVIRONMENT RESET - PHASE 5"
echo "================================================================================"
echo "This script will reset the main branch to a clean state for re-attack testing"
echo "Start time: $(date)"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
MAIN_BRANCH="main"
HARDENED_BRANCH="hardened"
BACKUP_BRANCH="main-pre-reset-$(date +%Y%m%d-%H%M%S)"

################################################################################
# Step 1: Safety checks
################################################################################

echo "--------------------------------------------------------------------------------"
echo "STEP 1: SAFETY CHECKS"
echo "--------------------------------------------------------------------------------"

# Check if git repo
if [ ! -d .git ]; then
    echo -e "${RED}[ERROR] Not a git repository!${NC}"
    exit 1
fi

# Check current branch
CURRENT_BRANCH=$(git branch --show-current)
echo "[*] Current branch: $CURRENT_BRANCH"

# Check if hardened branch exists
if ! git rev-parse --verify "$HARDENED_BRANCH" >/dev/null 2>&1; then
    echo -e "${RED}[ERROR] Hardened branch '$HARDENED_BRANCH' not found!${NC}"
    echo "Cannot reset without a clean reference branch."
    exit 1
fi

echo -e "${GREEN}[OK] Safety checks passed${NC}"

################################################################################
# Step 2: Create backup
################################################################################

echo ""
echo "--------------------------------------------------------------------------------"
echo "STEP 2: CREATE BACKUP"
echo "--------------------------------------------------------------------------------"

echo "[*] Creating backup branch: $BACKUP_BRANCH"
git branch "$BACKUP_BRANCH" "$MAIN_BRANCH"

if git rev-parse --verify "$BACKUP_BRANCH" >/dev/null 2>&1; then
    echo -e "${GREEN}[OK] Backup created successfully${NC}"
    echo "You can restore with: git checkout main && git reset --hard $BACKUP_BRANCH"
else
    echo -e "${RED}[ERROR] Failed to create backup branch${NC}"
    exit 1
fi

################################################################################
# Step 3: Switch to main branch
################################################################################

echo ""
echo "--------------------------------------------------------------------------------"
echo "STEP 3: SWITCH TO MAIN BRANCH"
echo "--------------------------------------------------------------------------------"

if [ "$CURRENT_BRANCH" != "$MAIN_BRANCH" ]; then
    echo "[*] Switching to $MAIN_BRANCH..."
    git checkout "$MAIN_BRANCH"
else
    echo "[*] Already on $MAIN_BRANCH"
fi

echo -e "${GREEN}[OK] On main branch${NC}"

################################################################################
# Step 4: Reset main to hardened state
################################################################################

echo ""
echo "--------------------------------------------------------------------------------"
echo "STEP 4: RESET MAIN TO CLEAN STATE"
echo "--------------------------------------------------------------------------------"

echo "[*] Copying clean code from hardened branch..."

# Get list of files that differ between main and hardened
echo "[*] Identifying files to reset..."

# Reset specific directories that contain vulnerable code
DIRS_TO_RESET=(
    "sample-apps/frontend/src"
    "sample-apps/backend-api/src"
    "docker"
    ".github/workflows"
)

for dir in "${DIRS_TO_RESET[@]}"; do
    if [ -d "$dir" ]; then
        echo "  [*] Resetting: $dir"
        git checkout "$HARDENED_BRANCH" -- "$dir" 2>/dev/null || true
    fi
done

# Remove any attack-specific files
echo "[*] Removing attack artifacts..."
rm -f sample-apps/backend-api/src/*-attack-*.js 2>/dev/null || true
rm -f sample-apps/frontend/src/*-attack-*.tsx 2>/dev/null || true
rm -f docker/*-vulnerable.* 2>/dev/null || true

echo -e "${GREEN}[OK] Files reset to clean state${NC}"

################################################################################
# Step 5: Commit the reset
################################################################################

echo ""
echo "--------------------------------------------------------------------------------"
echo "STEP 5: COMMIT RESET"
echo "--------------------------------------------------------------------------------"

# Check if there are changes to commit
if git diff --quiet && git diff --cached --quiet; then
    echo -e "${YELLOW}[WARN] No changes to commit - already clean${NC}"
else
    echo "[*] Committing reset..."

    git add -A

    cat > /tmp/reset-commit-msg << 'EOF'
Reset environment for re-attack phase

This commit resets the main branch to a clean state by copying
clean code from the hardened branch. This prepares for Phase 6
(re-attack with ML detection active).

Changes:
- Removed all intentional vulnerabilities
- Reset to hardened branch code
- Removed attack artifacts

Phase: 5 - Environment Reset
Research: Masters Thesis - Approach B

Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
EOF

    git commit -F /tmp/reset-commit-msg
    rm /tmp/reset-commit-msg

    echo -e "${GREEN}[OK] Reset committed${NC}"
fi

################################################################################
# Step 6: Verify clean state
################################################################################

echo ""
echo "--------------------------------------------------------------------------------"
echo "STEP 6: VERIFY CLEAN STATE"
echo "--------------------------------------------------------------------------------"

echo "[*] Running verification checks..."

# Check git status
echo "[*] Git status:"
git status --short

# Wait for user confirmation to push
echo ""
echo -e "${YELLOW}[WARN] Ready to push reset to remote${NC}"
read -p "Push changes to remote? (y/n): " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "[*] Pushing to remote..."
    git push origin "$MAIN_BRANCH"
    echo -e "${GREEN}[OK] Changes pushed to remote${NC}"
else
    echo -e "${YELLOW}[SKIP] Push skipped - run manually: git push origin main${NC}"
fi

################################################################################
# Step 7: Trigger security scan
################################################################################

echo ""
echo "--------------------------------------------------------------------------------"
echo "STEP 7: TRIGGER VERIFICATION SCAN"
echo "--------------------------------------------------------------------------------"

echo "[*] Waiting for next scheduled security scan (2 AM UTC)..."
echo "Or manually trigger workflow in GitHub Actions UI"

################################################################################
# Step 8: Verify ML shows normal
################################################################################

echo ""
echo "--------------------------------------------------------------------------------"
echo "STEP 8: NEXT STEPS"
echo "--------------------------------------------------------------------------------"

echo ""
echo "Environment reset complete! Next steps:"
echo ""
echo "1. Wait for security scan to run (next scheduled: 2 AM UTC)"
echo "2. Verify scan shows clean (no vulnerabilities)"
echo "3. Wait for ML detection to run (2:30 AM UTC)"
echo "4. Verify ML predicts 'NORMAL' (no anomalies)"
echo "5. Once verified clean, proceed to Phase 6 (re-attack)"
echo ""
echo "Backup branch created: $BACKUP_BRANCH"
echo "To restore if needed: git reset --hard $BACKUP_BRANCH"
echo ""

echo "================================================================================"
echo "RESET COMPLETE"
echo "================================================================================"
echo "End time: $(date)"
echo ""
