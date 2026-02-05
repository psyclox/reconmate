#!/bin/bash

# AutoRecon Installer for Kali Linux
# Usage: sudo ./setup.sh

GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${GREEN}[*] Starting AutoRecon Setup...${NC}"

# Check for root
if [ "$EUID" -ne 0 ]; then 
  echo "Please run as root (sudo ./setup.sh)"
  exit
fi

echo -e "${GREEN}[*] Updating package lists...${NC}"
apt-get update

echo -e "${GREEN}[*] Installing system dependencies (nmap, whois)...${NC}"
apt-get install -y nmap whois python3-pip python3-venv

echo -e "${GREEN}[*] Setting up Python Virtual Environment...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

echo -e "${GREEN}[*] Activating venv and installing Python libraries...${NC}"
source venv/bin/activate
pip install -r requirements.txt

echo -e "${GREEN}[*] Setup Complete!${NC}"
echo -e "To run the tool:"
echo -e "  source venv/bin/activate"
echo -e "  python main.py -d example.com"
