@echo off
title OmniMind OS Launcher
color 0B

echo.
echo     ╔═══════════════════════════════════════╗
echo     ║           🌌 OmniMind OS 🌌           ║
echo     ║      Your Personal AI Assistant       ║
echo     ╚═══════════════════════════════════════╝
echo.

:: Check if already installed
if not exist "frontend\node_modules" (
    echo ⚠️  OmniMind is not installed yet.
    echo.
    echo Please run INSTALL.bat first to complete setup.
    echo.
    pause
    exit /b 1
)

:: Start both backend and frontend with single command
echo 🚀 Launching OmniMind OS (Backend + Frontend)...
echo.
python run_omnimind.py

echo.
echo 🌟 OmniMind OS stopped.
echo.
echo Press any key to exit...
pause >nul