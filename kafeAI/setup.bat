@echo off
setlocal
title kafeAI Setup Wizard

echo ==================================================
echo         🌟 Welcome to kafeAI Setup 🌟
echo ==================================================

:: 1. Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python is not installed or not in PATH.
    echo [!] Please download and install Python 3.9+ from https://www.python.org/downloads/
    echo [!] Ensure you check "Add Python to PATH" during installation.
    start https://www.python.org/downloads/
    pause
    exit /b 1
)

:: 2. Run the Python Setup Wizard
echo.
echo Launching Setup Wizard...
python "%~dp0setup\setup_wizard.py"

if %errorlevel% neq 0 (
    echo.
    echo [!] Setup failed. Please check the error messages above.
    pause
    exit /b 1
)

:: 3. Launch the Application
echo.
echo [!] Setup successful! Starting kafeAI...
echo.

:: Try to launch manageragent.py
python "%~dp0manageragent.py"

pause
