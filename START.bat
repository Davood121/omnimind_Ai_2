@echo off
title OmniMind OS
cls
echo ========================================
echo         OMNIMIND OS LAUNCHER
echo ========================================
echo.
echo Starting Frontend...
echo.

cd frontend
start "OmniMind Frontend" cmd /k "npm run dev"

echo.
echo ========================================
echo    OmniMind OS Started!
echo ========================================
echo.
echo Frontend: http://localhost:5173
echo Backend: Already running on port 8000
echo.
echo Open your browser to: http://localhost:5173
echo.
pause