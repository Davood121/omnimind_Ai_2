@echo off
echo ========================================
echo    OmniMind OS - Complete Installation
echo ========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

:: Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org
    pause
    exit /b 1
)

:: Check if Ollama is installed
ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Ollama is not installed
    echo Please install Ollama from https://ollama.ai
    pause
    exit /b 1
)

echo ✓ Python found
echo ✓ Node.js found  
echo ✓ Ollama found
echo.

:: Install Python dependencies
echo Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install Python dependencies
    pause
    exit /b 1
)

:: Install Node.js dependencies
echo Installing Node.js dependencies...
cd frontend
npm install
if %errorlevel% neq 0 (
    echo ERROR: Failed to install Node.js dependencies
    pause
    exit /b 1
)
cd ..

:: Pull Ollama model
echo Installing AI model...
ollama pull qwen2.5:3b
if %errorlevel% neq 0 (
    echo WARNING: Failed to install qwen2.5:3b, will use available models
)

:: Create desktop shortcut
echo Creating desktop shortcut...
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\OmniMind OS.lnk'); $Shortcut.TargetPath = '%CD%\START_HERE.bat'; $Shortcut.WorkingDirectory = '%CD%'; $Shortcut.IconLocation = '%CD%\web\favicon.ico'; $Shortcut.Save()"

echo.
echo ========================================
echo    Installation Complete!
echo ========================================
echo.
echo Desktop shortcut created: "OmniMind OS"
echo.
echo To start OmniMind:
echo 1. Double-click "OmniMind OS" on desktop
echo 2. Or run: START_HERE.bat
echo.
pause