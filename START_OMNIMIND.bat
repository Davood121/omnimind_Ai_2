@echo off
cls
echo ========================================
echo    STARTING OMNIMIND OS
echo ========================================
echo.

cd /d "%~dp0"

echo [1/2] Starting Backend...
start "OmniMind Backend" cmd /k "python hologram_backend.py"
timeout /t 3 /nobreak >nul

echo [2/2] Starting Frontend...
cd frontend
start "OmniMind Frontend" cmd /k "npm run dev"
cd ..

timeout /t 5 /nobreak >nul
start http://localhost:5173

echo.
echo ========================================
echo    OMNIMIND OS RUNNING
echo ========================================
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo Keep both terminal windows open!
echo Press any key to exit this launcher...
pause >nul