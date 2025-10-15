#!/usr/bin/env python3
"""
OmniMind OS - Single Command Launcher
Starts both backend and frontend with one command
"""

import subprocess
import sys
import os
import time
import threading
from pathlib import Path

def run_backend():
    """Run the FastAPI backend server"""
    print("Starting Backend API Server...")
    try:
        subprocess.run([sys.executable, "api_server.py"], cwd=Path(__file__).parent)
    except KeyboardInterrupt:
        print("Backend stopped")

def run_frontend():
    """Run the React frontend development server"""
    print("Starting Frontend UI...")
    try:
        subprocess.run(["npm", "run", "dev"], cwd=Path(__file__).parent / "frontend")
    except KeyboardInterrupt:
        print("Frontend stopped")

def main():
    print("OmniMind OS - Single Command Launcher")
    print("=" * 50)
    
    # Check if frontend dependencies are installed
    if not (Path(__file__).parent / "frontend" / "node_modules").exists():
        print("ERROR: Frontend not installed. Run INSTALL.bat first.")
        return
    
    print("Starting both Backend and Frontend...")
    print("Backend API: http://localhost:8001")
    print("Frontend UI: http://localhost:5173")
    print("=" * 50)
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()
    
    # Wait a moment for backend to start
    time.sleep(2)
    
    # Start frontend in main thread (so Ctrl+C works)
    try:
        run_frontend()
    except KeyboardInterrupt:
        print("\nShutting down OmniMind OS...")
        print("Both servers stopped")

if __name__ == "__main__":
    main()