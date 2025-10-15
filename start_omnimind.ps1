#!/usr/bin/env pwsh
# OmniMind OS Startup Script

Write-Host "🌌 Starting OmniMind OS..." -ForegroundColor Cyan
Write-Host ""

# Check Ollama installation
Write-Host "🔍 Checking Ollama installation..." -ForegroundColor Yellow
try {
    $ollamaVersion = ollama --version 2>$null
    Write-Host "✅ Ollama found: $ollamaVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Ollama not found. Please install from https://ollama.ai" -ForegroundColor Red
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

# Check for qwen2.5:3b model
Write-Host "🔍 Checking AI model..." -ForegroundColor Yellow
$models = ollama list 2>$null
if ($models -match "qwen2.5:3b") {
    Write-Host "✅ qwen2.5:3b model found" -ForegroundColor Green
} else {
    Write-Host "⚠️  qwen2.5:3b model not found. Installing..." -ForegroundColor Yellow
    ollama pull qwen2.5:3b
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ qwen2.5:3b model installed successfully" -ForegroundColor Green
    } else {
        Write-Host "❌ Failed to install qwen2.5:3b model" -ForegroundColor Red
    }
}

Write-Host ""

# Start API Server
Write-Host "🚀 Starting API Server..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot'; python api_server.py"

# Wait for API to start
Start-Sleep -Seconds 3

# Start Frontend
Write-Host "🎨 Starting Holographic UI..." -ForegroundColor Magenta
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\frontend'; npm run dev"

Write-Host ""
Write-Host "✨ OmniMind OS is starting up!" -ForegroundColor Cyan
Write-Host ""
Write-Host "📡 API Server: http://localhost:8000" -ForegroundColor Yellow
Write-Host "🌐 Frontend UI: http://localhost:5173" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C in each window to stop the servers" -ForegroundColor Gray