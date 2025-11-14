#!/bin/bash
################################################################################
# Schedule Health Check - Linux/macOS Cron Setup
# Author: Joshua
# Description: Sets up automated health monitoring with cron
################################################################################

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
PYTHON_SCRIPT="$PROJECT_ROOT/scripts/python/system_health_checker_v2.py"
LOG_DIR="$PROJECT_ROOT/logs"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=================================="
echo "Health Check Scheduler Setup"
echo "=================================="

# Check if Python script exists
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo -e "${RED}Error: Health checker script not found at $PYTHON_SCRIPT${NC}"
    exit 1
fi

# Create logs directory
mkdir -p "$LOG_DIR"
echo -e "${GREEN}✓${NC} Created logs directory: $LOG_DIR"

# Create wrapper script for cron
WRAPPER_SCRIPT="$SCRIPT_DIR/run_health_check.sh"
cat > "$WRAPPER_SCRIPT" << 'EOF'
#!/bin/bash
# Auto-generated wrapper script for cron execution

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

# Activate virtual environment if it exists
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

# Run the health checker
python3 "$PROJECT_ROOT/scripts/python/system_health_checker_v2.py" --config "$PROJECT_ROOT/scripts/python/config.json"

# Exit with the same code as the health checker
exit $?
EOF

chmod +x "$WRAPPER_SCRIPT"
echo -e "${GREEN}✓${NC} Created wrapper script: $WRAPPER_SCRIPT"

# Generate cron entries
echo ""
echo "Add one of these lines to your crontab (run 'crontab -e'):"
echo ""
echo -e "${YELLOW}# Run health check every 5 minutes${NC}"
echo "*/5 * * * * $WRAPPER_SCRIPT >> $LOG_DIR/health_check.log 2>&1"
echo ""
echo -e "${YELLOW}# Run health check every 15 minutes${NC}"
echo "*/15 * * * * $WRAPPER_SCRIPT >> $LOG_DIR/health_check.log 2>&1"
echo ""
echo -e "${YELLOW}# Run health check every hour${NC}"
echo "0 * * * * $WRAPPER_SCRIPT >> $LOG_DIR/health_check.log 2>&1"
echo ""
echo -e "${YELLOW}# Run health check daily at 6 AM${NC}"
echo "0 6 * * * $WRAPPER_SCRIPT >> $LOG_DIR/health_check.log 2>&1"
echo ""

# Ask if user wants to add to crontab
read -p "Would you like to add a cron job now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Select frequency:"
    echo "1) Every 5 minutes"
    echo "2) Every 15 minutes"
    echo "3) Every hour"
    echo "4) Daily at 6 AM"
    read -p "Enter choice (1-4): " choice

    case $choice in
        1)
            CRON_ENTRY="*/5 * * * * $WRAPPER_SCRIPT >> $LOG_DIR/health_check.log 2>&1"
            ;;
        2)
            CRON_ENTRY="*/15 * * * * $WRAPPER_SCRIPT >> $LOG_DIR/health_check.log 2>&1"
            ;;
        3)
            CRON_ENTRY="0 * * * * $WRAPPER_SCRIPT >> $LOG_DIR/health_check.log 2>&1"
            ;;
        4)
            CRON_ENTRY="0 6 * * * $WRAPPER_SCRIPT >> $LOG_DIR/health_check.log 2>&1"
            ;;
        *)
            echo -e "${RED}Invalid choice${NC}"
            exit 1
            ;;
    esac

    # Add to crontab
    (crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -
    echo -e "${GREEN}✓${NC} Cron job added successfully!"
    echo ""
    echo "View your cron jobs with: crontab -l"
    echo "Remove this job with: crontab -e"
fi

echo ""
echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo "Logs will be saved to: $LOG_DIR/health_check.log"
echo "View logs with: tail -f $LOG_DIR/health_check.log"
