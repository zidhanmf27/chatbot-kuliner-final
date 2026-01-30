@echo off
REM Batch file untuk menjalankan API Chatbot Kuliner
REM Otomatis restart jika crash

:start
echo [%date% %time%] Starting Chatbot Kuliner API...
cd /d "C:\Users\Zidhan Maula Fatih\Kuliah\chatbot-kuliner-final"

REM Jalankan API
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000

REM Jika API crash/stop, tunggu 5 detik lalu restart
echo [%date% %time%] API stopped. Restarting in 5 seconds...
timeout /t 5 /nobreak
goto start
