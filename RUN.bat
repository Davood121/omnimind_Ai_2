@echo off
title OmniMind OS
echo ========================================
echo    Starting OmniMind OS
echo ========================================
echo.

:: Kill any existing processes on ports 8002 and 5173
echo Checking for existing processes...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8002') do taskkill /f /pid %%a >nul 2>&1
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5173') do taskkill /f /pid %%a >nul 2>&1

:: Start backend on port 8002
echo Starting Backend API Server on port 8002...
start "OmniMind Backend" cmd /k "python api_server_8002.py"

:: Wait for backend to start
timeout /t 3 /nobreak >nul

:: Start frontend
echo Starting Frontend UI...
cd frontend
start "OmniMind Frontend" cmd /k "npm run dev"
cd ..

echo.
echo ========================================
echo    OmniMind OS Started!
echo ========================================
echo.
echo Backend API: http://localhost:8002
echo Frontend UI: http://localhost:5173
echo API Docs: http://localhost:8002/docs
echo.
echo Close the terminal windows to stop the servers.
echo.
pause