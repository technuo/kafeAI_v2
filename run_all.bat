@echo off
TITLE kafeAI v2 - Full Stack Starter
SETLOCAL

:: --- 1. 配置路径 ---
SET BASE_DIR=%~dp0
SET FRONTEND_DIR=%BASE_DIR%kafeAI\frontend
SET BACKEND_DIR=%BASE_DIR%kafeAI
SET VENV_PYTHON=%BASE_DIR%.venv\Scripts\python.exe

echo ==================================================
echo         🚀 KafeAI v2: Full Stack Booting...
echo ==================================================

:: --- 2. 检查环境变量 ---
if not exist "%BACKEND_DIR%\.env" (
    echo [ERROR] .env file not found in %BACKEND_DIR%
    pause
    exit /b
)

:: --- 3. 启动后台: WhatsApp Twilio Bot (Port 5000) ---
echo [1/3] Starting WhatsApp Twilio Bot...
start /min "kafeAI_Twilio" cmd /c "cd /d \"%BACKEND_DIR%\" && \"%VENV_PYTHON%\" whatsapp_twilio.py"

:: --- 4. 启动前端: Streamlit Dashboard (Port 8502) ---
echo [2/3] Starting Streamlit Dashboard (Port 8502)...
start /min "kafeAI_Frontend" cmd /c "cd /d \"%FRONTEND_DIR%\" && \"%VENV_PYTHON%\" -m streamlit run app.py --server.port 8502"

:: --- 5. 启动隧道: ngrok (Port 5000) ---
echo [3/3] Starting ngrok Tunnel...
:: 尝试杀掉旧进程确保成功
taskkill /F /IM ngrok.exe >nul 2>&1
start "kafeAI_ngrok" cmd /c "ngrok http 5000"

echo.
echo --------------------------------------------------
echo ✅ ALL SYSTEMS GO!
echo.
echo 🖥️  Frontend: http://localhost:8502
echo 📱 WhatsApp: Twilio is listening on Port 5000
echo 🌐 Tunnel: Check the ngrok window for your public URL
echo --------------------------------------------------
echo Press any key to stop all services (optional/manual)...
pause
