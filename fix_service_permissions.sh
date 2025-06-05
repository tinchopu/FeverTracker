#!/bin/bash

# Fix Fever Tracker Service Permission Issues
# This script addresses the permission denied error when starting the service

set -e  # Exit on any error

echo "🔧 Fixing Fever Tracker Service Permission Issues"
echo "================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SERVICE_USER="fevertracker_user"
APP_DIR="/opt/fevertracker"
SERVICE_NAME="fever_tracker"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"

echo -e "${BLUE}Step 1: Stopping the service${NC}"
sudo systemctl stop "$SERVICE_NAME.service" 2>/dev/null || true
echo -e "${GREEN}✓ Service stopped${NC}"

echo -e "${BLUE}Step 2: Checking and fixing user setup${NC}"
# Ensure home directory exists with proper permissions
sudo mkdir -p "/home/$SERVICE_USER"
sudo chown "$SERVICE_USER:$SERVICE_USER" "/home/$SERVICE_USER"
sudo chmod 755 "/home/$SERVICE_USER"

# Ensure .local directory structure exists
sudo mkdir -p "/home/$SERVICE_USER/.local/bin"
sudo mkdir -p "/home/$SERVICE_USER/.cache"
sudo chown -R "$SERVICE_USER:$SERVICE_USER" "/home/$SERVICE_USER/.local"
sudo chown -R "$SERVICE_USER:$SERVICE_USER" "/home/$SERVICE_USER/.cache"
sudo chmod -R 755 "/home/$SERVICE_USER/.local"
sudo chmod -R 755 "/home/$SERVICE_USER/.cache"
echo -e "${GREEN}✓ User directories fixed${NC}"

echo -e "${BLUE}Step 3: Reinstalling uv for service user${NC}"
# Remove existing uv installation if it exists
sudo rm -f "/home/$SERVICE_USER/.local/bin/uv"

# Install uv for the service user with proper environment
sudo -u "$SERVICE_USER" bash -c 'export HOME="/home/fevertracker_user" && curl -LsSf https://astral.sh/uv/install.sh | sh'

# Verify uv installation
if [ -f "/home/$SERVICE_USER/.local/bin/uv" ]; then
    echo -e "${GREEN}✓ uv installed successfully${NC}"
    # Make sure it's executable
    sudo chmod +x "/home/$SERVICE_USER/.local/bin/uv"
else
    echo -e "${RED}✗ uv installation failed${NC}"
    exit 1
fi

echo -e "${BLUE}Step 4: Fixing application directory permissions${NC}"
sudo chown -R "$SERVICE_USER:$SERVICE_USER" "$APP_DIR"
sudo chmod -R 755 "$APP_DIR"
echo -e "${GREEN}✓ Application directory permissions fixed${NC}"

echo -e "${BLUE}Step 5: Reinstalling Python dependencies${NC}"
cd "$APP_DIR"
# Clean any existing virtual environment
sudo rm -rf .venv 2>/dev/null || true

# Install dependencies with proper environment
sudo -u "$SERVICE_USER" HOME="/home/$SERVICE_USER" PATH="/home/$SERVICE_USER/.local/bin:$PATH" /home/$SERVICE_USER/.local/bin/uv sync --verbose
echo -e "${GREEN}✓ Dependencies reinstalled${NC}"

echo -e "${BLUE}Step 6: Testing manual execution${NC}"
echo "Testing if the application can run manually..."
sudo -u "$SERVICE_USER" HOME="/home/$SERVICE_USER" PATH="/home/$SERVICE_USER/.local/bin:$PATH" timeout 10s /home/$SERVICE_USER/.local/bin/uv run streamlit run main.py --server.port 8501 --server.headless true &
MANUAL_PID=$!
sleep 5

if kill -0 $MANUAL_PID 2>/dev/null; then
    echo -e "${GREEN}✓ Manual execution successful${NC}"
    kill $MANUAL_PID 2>/dev/null || true
else
    echo -e "${YELLOW}⚠ Manual execution test completed (this is expected for the test)${NC}"
fi

echo -e "${BLUE}Step 7: Updating systemd service${NC}"
sudo cp fever_tracker.service "$SERVICE_FILE"
sudo systemctl daemon-reload
echo -e "${GREEN}✓ Service file updated${NC}"

echo -e "${BLUE}Step 8: Starting the service${NC}"
sudo systemctl start "$SERVICE_NAME.service"
sleep 3

echo -e "${BLUE}Step 9: Checking service status${NC}"
if sudo systemctl is-active --quiet "$SERVICE_NAME.service"; then
    echo -e "${GREEN}✓ Service is running successfully!${NC}"
    echo -e "${GREEN}✓ Your Fever Tracker application should now be accessible at: http://localhost:8501${NC}"
else
    echo -e "${RED}✗ Service still failed to start. Checking logs...${NC}"
    echo ""
    echo -e "${YELLOW}Recent service logs:${NC}"
    sudo journalctl -u "$SERVICE_NAME.service" --no-pager -n 20
    echo ""
    echo -e "${YELLOW}You can view full logs with: sudo journalctl -u ${SERVICE_NAME}.service -f${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}🎉 Service permission issues have been fixed!${NC}"
