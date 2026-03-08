# 强制清理并重启全部服务
taskkill /F /IM python.exe; taskkill /F /IM ngrok.exe;
start-job { cd "d:\2026\kafeAI v2\kafeAI\frontend"; & "d:\2026\kafeAI v2\.venv\Scripts\python.exe" -m streamlit run app.py --server.port 8502 };
start-job { cd "d:\2026\kafeAI v2\kafeAI"; & "d:\2026\kafeAI v2\.venv\Scripts\python.exe" whatsapp_twilio.py };
start-job { ngrok http 5000 };
