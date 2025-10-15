@echo off
title OmniMind Global Deployment
color 0B

echo.
echo     ╔═══════════════════════════════════════╗
echo     ║        🌍 OmniMind Global 🌍          ║
echo     ║     Docker + ngrok Deployment         ║
echo     ╚═══════════════════════════════════════╝
echo.

:: Check if Docker is running
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed or not running
    echo Please install Docker Desktop from https://docker.com
    pause
    exit /b 1
)

:: Check if ngrok token is set
findstr "YOUR_NGROK_TOKEN_HERE" ngrok.yml >nul
if %errorlevel% equ 0 (
    echo ❌ Please set your ngrok token in ngrok.yml
    echo 1. Go to https://ngrok.com and sign up
    echo 2. Get your auth token from dashboard
    echo 3. Replace YOUR_NGROK_TOKEN_HERE in ngrok.yml
    pause
    exit /b 1
)

echo ✅ Docker found
echo ✅ ngrok configured
echo.

echo 🔨 Building OmniMind container...
docker-compose build

echo 🚀 Starting global deployment...
docker-compose up -d

echo.
echo ⏳ Waiting for services to start...
timeout /t 10 /nobreak >nul

echo.
echo ═══════════════════════════════════════
echo    🌍 OmniMind is now GLOBAL! 🌍
echo ═══════════════════════════════════════
echo.
echo 📱 Local Access:     http://localhost:8000
echo 🌐 Global Access:    Check ngrok dashboard
echo 📊 ngrok Dashboard:  http://localhost:4040
echo.
echo 🔗 Your global URLs will be shown at:
echo    http://localhost:4040
echo.

:: Try to open ngrok dashboard
start http://localhost:4040

echo Press any key to view logs or Ctrl+C to stop...
pause >nul

echo.
echo 📋 Live logs (Ctrl+C to stop):
docker-compose logs -f