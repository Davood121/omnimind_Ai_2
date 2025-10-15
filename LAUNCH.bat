@echo off
title OmniMind OS Launcher
echo ========================================
echo    OmniMind OS - Starting System
echo ========================================
echo.

:: Start Backend
echo Starting Backend on port 7000...
start "OmniMind Backend" cmd /k "python backend.py"

:: Wait 3 seconds
timeout /t 3 /nobreak >nul

:: Start Frontend
echo Starting Frontend on port 5173...
cd frontend
start "OmniMind Frontend" cmd /k "npm run dev"
cd ..

:: Open Web Interface
echo Opening Web Interface...
timeout /t 2 /nobreak >nul
start "" "web\index.html"

echo.
echo ========================================
echo    OmniMind OS Started Successfully!
echo ========================================
echo.
echo Backend API: http://localhost:7000
echo React Frontend: http://localhost:5173  
echo Web Interface: web\index.html (opened)
echo.
echo Close the terminal windows to stop servers.
pause