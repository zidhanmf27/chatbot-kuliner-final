@echo off
REM Batch file untuk menjalankan Scheduler
REM Otomatis restart jika crash

:start
echo [%date% %time%] Starting Chatbot Scheduler...
cd /d "C:\Users\Zidhan Maula Fatih\Kuliah\chatbot-kuliner-final"

REM Jalankan Scheduler
python scheduler/service.py

REM Jika Scheduler crash/stop, tunggu 5 detik lalu restart
echo [%date% %time%] Scheduler stopped. Restarting in 5 seconds...
timeout /t 5 /nobreak
goto start
