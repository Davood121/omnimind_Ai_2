# 🚀 Quick Reference Guide

## 📋 System Requirements
- Python 3.8+
- Node.js 18+
- Ollama with phi3:medium
- Windows (for WiFi monitoring)

## ⚡ Quick Start
```bash
# Double-click this file:
START_HERE.bat

# Or manually:
# Terminal 1
python api_server.py

# Terminal 2
cd frontend
npm run dev
```

## 🎮 Chat Commands

### Music
```
play jazz music
play relaxing songs
play workout music
```

### Web
```
open youtube.com
open github.com
search latest AI news
search Python tutorials
```

### Applications
```
open calculator
launch notepad
start paint
open chrome
```

### System Info
```
what's the time
show my username
what's my IP address
show computer name
```

## 📊 System Metrics

### What's Monitored
- CPU: Usage % and frequency (GHz)
- Memory: Used/Total (GB) and %
- Disk: Free space (GB) and %
- Network: Sent/Received (MB)
- WiFi: Signal strength (%)
- Battery: Level % and status
- Temperature: System temp (°C)
- Processes: Top 3 by CPU

### Update Frequency
- Every 2 seconds automatically
- No manual refresh needed

## 🎨 UI Components

### Desktop Layout
```
┌─────────────┬──────────────┬─────────────┬──────────────┐
│   System    │    Skills    │ Holographic │     Chat     │
│   Status    │    Panel     │    Logo     │  Interface   │
│   (Left)    │   (Left)     │  (Center)   │   (Right)    │
└─────────────┴──────────────┴─────────────┴──────────────┘
```

### Mobile Layout
```
┌──────────────────────────────┐
│         Header               │
├──────────────────────────────┤
│                              │
│      Holographic Logo        │
│         (Center)             │
│                              │
├──────────────────────────────┤
│  [📊] [⚡] [💬]  (Toggles)   │
└──────────────────────────────┘
```

## 🎯 Skills Panel

### Available Skills
1. **Play Music** 🎵 - YouTube search
2. **Open Website** 🌐 - Browser launch
3. **Search Web** 🔍 - Google search
4. **Open Application** 💻 - System apps
5. **System Commands** ⚙️ - Info commands
6. **File Operations** 📁 - File management

### Quick Actions
- Play Music
- Search Web
- Calculator
- Notepad

## 🔧 API Endpoints

### System
```
GET  /api/status          - System metrics
GET  /api/profile         - User profile
GET  /api/conversations   - Chat history
```

### Skills
```
GET  /api/skills          - Available skills
POST /api/execute-skill   - Execute skill
```

### Chat
```
POST /api/chat            - Send message
WS   /ws/voice            - Voice stream
```

## 📱 Mobile Controls

### Buttons
- 📊 = System Status
- ⚡ = AI Skills
- 💬 = Chat Interface
- ✖️ = Close Panel

### Gestures
- Tap button to open panel
- Tap X to close panel
- Swipe to scroll
- Tap skill to execute

## 🎨 Status Indicators

### Colors
- 🟢 Green = Idle/Good
- 🟠 Orange = Thinking/Warning
- 🔵 Blue = Speaking/Active
- 🔴 Red = Offline/Critical

### Meanings
- **Idle** - Ready for input
- **Thinking** - Processing request
- **Speaking** - Generating response
- **Offline** - Backend disconnected

## 🔒 Safety Features

### Skills
- Whitelisted commands only
- No destructive operations
- User confirmation required
- Timeout protection

### System
- Read-only monitoring
- No elevated privileges
- Safe command filtering
- Error boundaries

## 🐛 Troubleshooting

### Backend Offline
```bash
cd OmniMind
python api_server.py
```

### Frontend Won't Load
```bash
cd OmniMind/frontend
npm install
npm run dev
```

### No System Stats
```bash
pip install psutil
```

### Skills Not Working
- Check backend is running
- Verify port 8000 is open
- Check browser console (F12)

## 📊 Performance Tips

### For Best Performance
1. Close unused applications
2. Use Chrome or Edge
3. Clear browser cache
4. Update to latest versions

### If Slow
1. Reduce particle count
2. Disable animations
3. Use lighter AI model
4. Close other tabs

## 🎯 Keyboard Shortcuts

### Browser
- F12 = Developer Tools
- Ctrl+Shift+M = Device Toolbar
- Ctrl+F5 = Hard Refresh
- Ctrl+Shift+Delete = Clear Cache

### Chat
- Enter = Send message
- Shift+Enter = New line
- Esc = Clear input

## 📚 Documentation Files

- **README.md** - Overview
- **QUICK_START.md** - Fast setup
- **COMPLETE_SETUP.md** - Detailed setup
- **NEW_FEATURES.md** - Feature list
- **TROUBLESHOOTING.md** - Problem solving
- **IMPLEMENTATION_SUMMARY.md** - Technical details
- **QUICK_REFERENCE.md** - This file

## 🔗 Useful Links

- Frontend: http://localhost:5173
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Ollama: https://ollama.ai

## 💡 Pro Tips

1. **Use natural language** - Just type what you want
2. **Try quick actions** - Fastest way to execute skills
3. **Watch the logo** - It shows AI activity
4. **Check system panel** - Monitor your PC health
5. **Use mobile mode** - Toggle panels as needed

---

**Need help? Check TROUBLESHOOTING.md** 📖