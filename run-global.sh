#!/bin/bash

echo "╔═══════════════════════════════════════╗"
echo "║        🌍 OmniMind Global 🌍          ║"
echo "║     Docker + ngrok Deployment         ║"
echo "╚═══════════════════════════════════════╝"
echo

# Check if Docker is running
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed"
    echo "Please install Docker from https://docker.com"
    exit 1
fi

# Check if ngrok token is set
if grep -q "YOUR_NGROK_TOKEN_HERE" ngrok.yml; then
    echo "❌ Please set your ngrok token in ngrok.yml"
    echo "1. Go to https://ngrok.com and sign up"
    echo "2. Get your auth token from dashboard"
    echo "3. Replace YOUR_NGROK_TOKEN_HERE in ngrok.yml"
    exit 1
fi

echo "✅ Docker found"
echo "✅ ngrok configured"
echo

echo "🔨 Building OmniMind container..."
docker-compose build

echo "🚀 Starting global deployment..."
docker-compose up -d

echo
echo "⏳ Waiting for services to start..."
sleep 10

echo
echo "═══════════════════════════════════════"
echo "   🌍 OmniMind is now GLOBAL! 🌍"
echo "═══════════════════════════════════════"
echo
echo "📱 Local Access:     http://localhost:8000"
echo "🌐 Global Access:    Check ngrok dashboard"
echo "📊 ngrok Dashboard:  http://localhost:4040"
echo
echo "🔗 Your global URLs will be shown at:"
echo "   http://localhost:4040"
echo

# Try to open ngrok dashboard (macOS/Linux)
if command -v open &> /dev/null; then
    open http://localhost:4040
elif command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:4040
fi

echo "Press Enter to view logs or Ctrl+C to stop..."
read

echo
echo "📋 Live logs (Ctrl+C to stop):"
docker-compose logs -f