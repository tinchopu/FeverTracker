#!/bin/bash

# Fever Tracker Linux Service Deployment Script
# This script sets up the Fever Tracker application as a systemd service

set -e  # Exit on any error

echo "🌡️ Fever Tracker Service Deployment Script"
echo "=========================================="

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

echo -e "${BLUE}Step 1: Creating dedicated user '${SERVICE_USER}'${NC}"
if id "$SERVICE_USER" &>/dev/null; then
    echo -e "${YELLOW}User '${SERVICE_USER}' already exists, skipping creation${NC}"
else
    sudo useradd -r -s /bin/false "$SERVICE_USER"
    echo -e "${GREEN}✓ User '${SERVICE_USER}' created successfully${NC}"
fi

echo -e "${BLUE}Step 2: Creating application directory '${APP_DIR}'${NC}"
sudo mkdir -p "$APP_DIR"
echo -e "${GREEN}✓ Directory '${APP_DIR}' created${NC}"

echo -e "${BLUE}Step 3: Copying application files to '${APP_DIR}'${NC}"
# Copy all files from current directory to the app directory
sudo cp -r . "$APP_DIR/"
# Remove the deployment script from the destination to avoid confusion
sudo rm -f "$APP_DIR/deploy_as_service.sh"
echo -e "${GREEN}✓ Application files copied${NC}"

echo -e "${BLUE}Step 4: Setting ownership and permissions${NC}"
sudo chown -R "$SERVICE_USER:$SERVICE_USER" "$APP_DIR"
sudo chmod -R 755 "$APP_DIR"
echo -e "${GREEN}✓ Ownership and permissions set${NC}"

echo -e "${BLUE}Step 5: Installing uv (if not already installed)${NC}"
if command -v uv &> /dev/null; then
    echo -e "${YELLOW}uv is already installed, skipping installation${NC}"
else
    echo -e "${YELLOW}Installing uv...${NC}"
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.cargo/env
    echo -e "${GREEN}✓ uv installed successfully${NC}"
fi

echo -e "${BLUE}Step 6: Installing Python dependencies${NC}"
cd "$APP_DIR"
sudo -u "$SERVICE_USER" uv sync
echo -e "${GREEN}✓ Dependencies installed${NC}"

echo -e "${BLUE}Step 7: Installing systemd service${NC}"
sudo cp fever_tracker.service "$SERVICE_FILE"
echo -e "${GREEN}✓ Service file installed to ${SERVICE_FILE}${NC}"

echo -e "${BLUE}Step 8: Enabling and starting the service${NC}"
sudo systemctl daemon-reload
sudo systemctl enable "$SERVICE_NAME.service"
sudo systemctl start "$SERVICE_NAME.service"
echo -e "${GREEN}✓ Service enabled and started${NC}"

echo -e "${BLUE}Step 9: Checking service status${NC}"
sleep 3  # Give the service a moment to start
if sudo systemctl is-active --quiet "$SERVICE_NAME.service"; then
    echo -e "${GREEN}✓ Service is running successfully!${NC}"
    echo -e "${GREEN}✓ Your Fever Tracker application is now accessible at: http://your_server_ip:8501${NC}"
else
    echo -e "${RED}✗ Service failed to start. Check logs with: sudo journalctl -u ${SERVICE_NAME}.service${NC}"
    exit 1
fi

echo ""
echo -e "${BLUE}Useful service management commands:${NC}"
echo -e "  ${YELLOW}Check status:${NC}     sudo systemctl status ${SERVICE_NAME}.service"
echo -e "  ${YELLOW}View logs:${NC}        sudo journalctl -u ${SERVICE_NAME}.service -f"
echo -e "  ${YELLOW}Stop service:${NC}     sudo systemctl stop ${SERVICE_NAME}.service"
echo -e "  ${YELLOW}Start service:${NC}    sudo systemctl start ${SERVICE_NAME}.service"
echo -e "  ${YELLOW}Restart service:${NC}  sudo systemctl restart ${SERVICE_NAME}.service"
echo -e "  ${YELLOW}Disable service:${NC}  sudo systemctl disable ${SERVICE_NAME}.service"

echo ""
echo -e "${GREEN}🎉 Deployment completed successfully!${NC}"
