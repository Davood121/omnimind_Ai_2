# 🚀 Quick Start Guide

## Option 1: Double-Click to Start (Easiest!)

Simply double-click `START_HERE.bat` and everything will launch automatically!

## Option 2: Manual Start

### Step 1: Start the Backend API
Open PowerShell in the OmniMind folder and run:
```powershell
python api_server.py
```

### Step 2: Start the Frontend UI
Open another PowerShell in the OmniMind/frontend folder and run:
```powershell
npm run dev
```

### Step 3: Open Your Browser
Navigate to: **http://localhost:5173**

## 🎮 What You'll See

### 1. **Holographic Core** (Center)
   - Animated rotating rings
   - Pulsating energy sphere
   - Orbiting particles
   - Scanning laser effects

### 2. **System Panel** (Left)
   - Neural load monitoring
   - Processing speed
   - Memory usage
   - Connection status
   - Activity logs

### 3. **Chat Interface** (Right)
   - Type messages to OmniMind
   - Get AI responses
   - View conversation history

### 4. **Voice Activation** (Bottom Center)
   - Click "ACTIVATE VOICE" button
   - See real-time voice waveforms
   - Voice recognition coming soon!

## 🎨 Features to Try

1. **Send a message** in the chat interface
2. **Click the voice button** to see animations
3. **Watch the holographic core** respond to activity
4. **Observe the particle field** in the background
5. **Check system metrics** in the left panel

## 🔧 Troubleshooting

### API Server Won't Start
- Make sure Ollama is running with phi3:medium model
- Check if port 8000 is available
- Install dependencies: `pip install -r requirements.txt`

### Frontend Won't Start
- Check if port 5173 is available
- Install dependencies: `cd frontend && npm install`
- Make sure Node.js 18+ is installed

### Chat Not Working
- Ensure both API server and frontend are running
- Check browser console for errors
- Verify Ollama is running: `ollama list`

## 📱 Browser Compatibility

Works best on:
- ✅ Chrome/Edge (Recommended)
- ✅ Firefox
- ✅ Safari
- ⚠️ Mobile browsers (limited)

## 🎯 Next Steps

1. Customize colors in `frontend/src/index.css`
2. Add more AI skills in `skills/` folder
3. Modify the holographic effects in components
4. Train the AI with your preferences

---

**Enjoy your JARVIS-like AI experience! 🌌**