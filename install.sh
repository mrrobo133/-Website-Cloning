#!/data/data/com.termux/files/usr/bin/bash

# ANSI Color Codes for Terminal UI
RED='\033[1;31m'
GREEN='\033[1;32m'
CYAN='\033[1;36m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

clear
echo -e "${CYAN}[*] Initializing Website Cloning Tool Installation...${NC}"
sleep 1

# Step 1: Updating packages and installing Python, Pip & Git
echo -e "${GREEN}[+] Updating Termux packages and installing dependencies...${NC}"
pkg update -y && pkg upgrade -y
pkg install python python-pip git curl -y

# Step 2: Installing required Python packages (requests, colorama, etc. if needed)
echo -e "${GREEN}[+] Installing required Python libraries...${NC}"
pip install --upgrade pip
pip install requests urllib3 colorama 2>/dev/null

# Step 3: Verifying Python installation
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[!] Python3 installation failed. Please install it manually.${NC}"
    exit 1
fi

# Step 4: Setting up execution permissions for main file
echo -e "${GREEN}[+] Configuring file permissions for tool.py...${NC}"
chmod +x tool.py 2>/dev/null

# Step 5: Finalizing
echo -e "\n${CYAN}====================================================${NC}"
echo -e "${GREEN} Installation Completed Successfully!${NC}"
echo -e "${CYAN}====================================================${NC}"
echo -e " To run the tool, type: ${YELLOW}python3 tool.py${NC}\n"
