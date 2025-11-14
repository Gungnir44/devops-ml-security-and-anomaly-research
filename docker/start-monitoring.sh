#!/bin/bash
################################################################################
# Start Monitoring Stack - Helper Script
# Author: Joshua
# Description: Easy startup for Docker monitoring stack
################################################################################

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  DevOps Monitoring Stack - Startup    ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${YELLOW}Error: Docker is not running${NC}"
    echo "Please start Docker and try again"
    exit 1
fi

echo -e "${GREEN}✓${NC} Docker is running"

# Check if config.json exists
if [ ! -f "../scripts/python/config.json" ]; then
    echo -e "${YELLOW}⚠${NC} config.json not found, creating from example..."
    cp ../scripts/python/config.example.json ../scripts/python/config.json
    echo -e "${GREEN}✓${NC} Created config.json"
fi

# Stop existing containers (if any)
echo ""
echo "Stopping existing containers..."
docker-compose -f docker-compose-monitoring.yml down 2>/dev/null || true

# Start the stack
echo ""
echo "Starting monitoring stack..."
docker-compose -f docker-compose-monitoring.yml up -d

# Wait for services to be healthy
echo ""
echo "Waiting for services to start..."
sleep 5

# Check status
echo ""
echo -e "${BLUE}Container Status:${NC}"
docker-compose -f docker-compose-monitoring.yml ps

echo ""
echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║         Stack Started Successfully!     ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}Access your services:${NC}"
echo -e "  ${GREEN}Dashboard:${NC}   http://localhost:5000"
echo -e "  ${GREEN}Web Demo:${NC}    http://localhost:8080"
echo -e "  ${GREEN}API:${NC}         http://localhost:5000/api/latest"
echo ""
echo -e "${BLUE}Useful commands:${NC}"
echo -e "  View logs:       docker-compose -f docker-compose-monitoring.yml logs -f"
echo -e "  Stop stack:      docker-compose -f docker-compose-monitoring.yml down"
echo -e "  Restart:         docker-compose -f docker-compose-monitoring.yml restart"
echo -e "  Container stats: docker stats"
echo ""
echo -e "${YELLOW}Tip:${NC} The dashboard will update automatically as health checks run"
echo ""
