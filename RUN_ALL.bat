@echo off
title OmniMind OS
cls
echo ========================================
echo         OMNIMIND OS LAUNCHER
echo ========================================
echo.

:: Kill any existing processes on port 8000
echo Cleaning up old processes...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000') do taskkill /f /pid %%a >nul 2>&1

:: Start Backend
echo Starting Backend on port 8000...
start "OmniMind Backend" cmd /k "python hologram_backend.py"

:: Wait for backend to start
timeout /t 3 /nobreak >nul

:: Start Frontend
echo Starting Frontend on port 5173...
cd frontend
start "OmniMind Frontend" cmd /k "npm run dev"
cd ..

:: Wait and open browser
timeout /t 5 /nobreak >nul
start http://localhost:5173

echo.
echo ========================================
echo    OmniMind OS Running!
echo ========================================
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo Close the terminal windows to stop.
echo.
pause