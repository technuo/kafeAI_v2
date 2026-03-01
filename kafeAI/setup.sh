#!/bin/bash

echo "=================================================="
echo "        🌟 Welcome to kafeAI Setup 🌟"
echo "=================================================="

# 1. Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "[!] Python3 is not installed."
    echo "[!] Please install Python 3.9+ (e.g., 'brew install python' on Mac or 'sudo apt install python3' on Linux)."
    exit 1
fi

# 2. Run the Python Setup Wizard
echo -e "\nLaunching Setup Wizard..."
python3 "$(dirname "$0")/setup/setup_wizard.py"

if [ $? -ne 0 ]; then
    echo -e "\n[!] Setup failed. Please check the error messages above."
    exit 1
fi

# 3. Launch the Application
echo -e "\n[!] Setup successful! Starting kafeAI...\n"

# Try to launch manageragent.py
python3 "$(dirname "$0")/manageragent.py"
