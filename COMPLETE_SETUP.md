# 🚀 Complete Setup & Usage Guide

## 📋 Prerequisites

### Required Software
1. **Python 3.8+** - [Download](https://www.python.org/downloads/)
2. **Node.js 18+** - [Download](https://nodejs.org/)
3. **Ollama** - [Download](https://ollama.ai/)

### Verify Installation
```powershell
python --version    # Should show 3.8 or higher
node --version      # Should show 18.0 or higher
npm --version       # Should show 9.0 or higher
ollama --version    # Should show ollama version
```

---

## 🎯 Step-by-Step Setup

### Step 1: Install Ollama Model
```powershell
# Pull the AI model (this may take a few minutes)
ollama pull phi3:medium

# Verify it's installed
ollama list
```

### Step 2: Install Backend Dependencies
```powershell
cd OmniMind
pip install -r requirements.txt
```

### Step 3: Install Frontend Dependencies
```powershell
cd frontend
npm install
```

### Step 4: Start the System

#### Option A: Automatic (Easiest)
Double-click `START_HERE.bat`

#### Option B: Manual
```powershell
# Terminal 1 - Start API Server
cd OmniMind
python api_server.py

# Terminal 2 - Start Frontend
cd OmniMind/frontend
npm run dev
```

### Step 5: Open in Browser
Navigate to: **http://localhost:5173**

---

## 🎮 Using OmniMind OS

### Main Interface Components

#### 1. **Holographic Core** (Center)
- The animated sphere is the heart of OmniMind
- Pulses and glows when AI is active
- Responds to voice activation

#### 2. **System Panel** (Left)
- Shows real-time system metrics
- Neural load, processing speed, memory
- Activity log of recent events
- **Mobile**: Tap hamburger menu to toggle

#### 3. **Chat Interface** (Right)
- Type messages to interact with AI
- View conversation history
- Get intelligent responses
- **Mobile**: Tap chat icon to toggle

#### 4. **Voice Activation** (Bottom)
- Click "ACTIVATE VOICE" button
- See real-time voice waveform
- Future: Full voice recognition

### Status Indicators

| Color | Status | Meaning |
|-------|--------|---------|
| 🟢 Green | Idle | Ready for input |
| 🟠 Orange | Thinking | Processing your request |
| 🔵 Blue | Speaking | Generating response |
| 🔴 Red | Offline | Backend disconnected |

---

## 💬 Interacting with OmniMind

### Chat Commands

#### General Conversation
```
You: Hello OmniMind
AI: Hello! I'm OmniMind, your personal AI assistant. How can I help you today?
```

#### Ask Questions
```
You: What's the weather like?
AI: I don't have real-time weather data, but I can help you with other tasks!
```

#### Get Help
```
You: What can you do?
AI: I can chat with you, answer questions, and help with various tasks...
```

### Voice Mode (Coming Soon)
1. Click "ACTIVATE VOICE"
2. Speak your command
3. See waveform visualization
4. Get voice response

---

## 📱 Mobile Usage

### Accessing on Mobile

1. **Find your computer's IP address**
   ```powershell
   ipconfig
   # Look for "IPv4 Address" (e.g., 192.168.1.100)
   ```

2. **Update API server** (if needed)
   Edit `api_server.py`:
   ```python
   allow_origins=["http://localhost:5173", "http://YOUR_IP:5173"]
   ```

3. **Access from phone**
   ```
   http://YOUR_IP:5173
   ```

### Mobile Controls

- **System Panel**: Tap left hamburger menu
- **Chat Panel**: Tap right hamburger menu
- **Close Panel**: Tap X button
- **Send Message**: Type and tap send icon

---

## ⚙️ Configuration

### Change AI Model

Edit `api_server.py`:
```python
ollama = OllamaInterface(model="phi3:mini")  # Faster
# or
ollama = OllamaInterface(model="llama2")     # Alternative
```

### Customize Colors

Edit `frontend/src/index.css`:
```css
:root {
  --cyber-blue: #00d9ff;      /* Change to your color */
  --cyber-purple: #b537f2;    /* Change to your color */
  --cyber-pink: #ff006e;      /* Change to your color */
  --cyber-green: #00ff88;     /* Change to your color */
}
```

### Adjust Performance

Edit `frontend/src/components/ParticleField.tsx`:
```typescript
// Reduce particles for better performance
const particleCount = window.innerWidth < 768 ? 25 : 50
```

---

## 🔧 Advanced Features

### API Endpoints

Access these directly in browser:

- **Status**: http://localhost:8000/api/status
- **Profile**: http://localhost:8000/api/profile
- **Conversations**: http://localhost:8000/api/conversations
- **API Docs**: http://localhost:8000/docs

### WebSocket (Future)

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/voice')
ws.onmessage = (event) => {
  console.log('Voice data:', event.data)
}
```

### Memory System

OmniMind stores data in:
- `memory/user_profile.json` - Your preferences
- `memory/conversations.json` - Chat history

Edit these files to customize your profile!

---

## 🎨 Customization Ideas

### 1. Change Fonts
Edit `frontend/src/index.css`:
```css
@import url('https://fonts.googleapis.com/css2?family=YourFont&display=swap');

:root {
  --font-orbitron: 'YourFont', sans-serif;
}
```

### 2. Add More Particles
Edit `ParticleField.tsx`:
```typescript
const particleCount = 200 // More particles!
```

### 3. Change Animation Speed
Edit `HolographicCore.tsx`:
```typescript
rotate: { duration: 10 } // Faster rotation
```

### 4. Custom System Metrics
Edit `SystemPanel.tsx` to add your own metrics!

---

## 📊 Performance Tips

### For Best Performance

1. **Close unused applications**
2. **Use Chrome or Edge browser**
3. **Reduce particle count on older devices**
4. **Use phi3:mini model for faster responses**
5. **Clear browser cache regularly**

### Optimization Settings

```typescript
// In ParticleField.tsx
const particleCount = 50  // Reduced from 100

// In HolographicCore.tsx
const size = Math.min(256, minDimension * 0.5)  // Smaller core
```

---

## 🔒 Privacy & Security

### Data Storage
- All data stored locally on your device
- No cloud services or external APIs
- Conversations saved in `memory/` folder

### Network Security
- API runs on localhost only
- CORS restricted to your domains
- No data leaves your computer

### Clearing Data
```powershell
# Delete conversation history
rm OmniMind/memory/conversations.json

# Reset user profile
rm OmniMind/memory/user_profile.json
```

---

## 🆘 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Backend offline | Run `python api_server.py` |
| Frontend won't load | Run `npm run dev` in frontend folder |
| No AI responses | Check Ollama is running: `ollama list` |
| Port in use | Kill process or change port |
| Slow performance | Reduce particles, use lighter model |

See **TROUBLESHOOTING.md** for detailed solutions.

---

## 🎯 What's Next?

### Planned Features
- [ ] Real voice recognition
- [ ] 3D holographic effects with Three.js
- [ ] Custom AI model training
- [ ] Plugin system for extensions
- [ ] Mobile app version
- [ ] Multi-language support
- [ ] AR/VR integration

### Contributing
Want to add features? Edit the code and share your improvements!

---

## 📚 Additional Resources

- **README.md** - Overview and quick start
- **FEATURES.md** - Detailed feature list
- **RESPONSIVE_GUIDE.md** - Mobile optimization
- **TROUBLESHOOTING.md** - Problem solving
- **QUICK_START.md** - Fast setup guide

---

**Enjoy your JARVIS-like AI experience! 🌌**

*OmniMind OS - The Future of AI Interaction*