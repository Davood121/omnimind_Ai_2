@echo off
echo ========================================
echo Starting OmniMind Web Interface
echo ========================================
echo.
echo Prerequisites:
echo 1. Ollama must be running (ollama run phi3:medium)
echo 2. Dependencies installed (pip install -r requirements.txt)
echo.
echo Starting Flask server on http://127.0.0.1:5055
echo Press Ctrl+C to stop the server
echo.
python server.py
pause
