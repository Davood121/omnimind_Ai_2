# 🔧 Troubleshooting Guide

## Common Issues and Solutions

### 🔴 Backend Connection Failed

#### Symptoms
- Red dot in header showing "offline"
- Chat shows "Backend offline - Start api_server.py"
- Messages show connection error

#### Solutions

**1. Check if API server is running**
```powershell
# Look for a window titled "OmniMind API"
# Or check if port 8000 is in use
netstat -ano | findstr :8000
```

**2. Start the API server**
```powershell
cd OmniMind
python api_server.py
```

**3. Check Ollama is running**
```powershell
# Verify Ollama is installed and running
ollama list

# If not installed, download from https://ollama.ai
# Then pull the model:
ollama pull phi3:medium
```

**4. Verify Python dependencies**
```powershell
cd OmniMind
pip install -r requirements.txt
```

---

### 🌐 Frontend Won't Load

#### Symptoms
- Browser shows "Cannot connect"
- Blank white screen
- Console errors

#### Solutions

**1. Check if frontend is running**
```powershell
# Look for a window with "VITE" in the output
# Or check if port 5173 is in use
netstat -ano | findstr :5173
```

**2. Start the frontend**
```powershell
cd OmniMind/frontend
npm run dev
```

**3. Clear browser cache**
- Press Ctrl+Shift+Delete
- Clear cached images and files
- Reload page (Ctrl+F5)

**4. Reinstall dependencies**
```powershell
cd OmniMind/frontend
rm -r node_modules
npm install
npm run dev
```

---

### 💬 Chat Not Working

#### Symptoms
- Messages don't send
- No AI responses
- "Connection error" messages

#### Solutions

**1. Verify both servers are running**
- API server on port 8000
- Frontend on port 5173

**2. Check browser console**
- Press F12
- Look for errors in Console tab
- Check Network tab for failed requests

**3. Test API directly**
Open browser and visit:
```
http://localhost:8000/api/status
```
Should return JSON with system status

**4. Check CORS settings**
Ensure `api_server.py` allows localhost:5173

---

### 🎨 UI Looks Broken

#### Symptoms
- No colors or styling
- Components misaligned
- Missing animations

#### Solutions

**1. Check Tailwind CSS**
```powershell
cd OmniMind/frontend
# Verify tailwindcss is installed
npm list tailwindcss
```

**2. Rebuild the project**
```powershell
cd OmniMind/frontend
npm run build
npm run dev
```

**3. Clear Vite cache**
```powershell
cd OmniMind/frontend
rm -r node_modules/.vite
npm run dev
```

---

### 📱 Mobile Issues

#### Symptoms
- Layout broken on phone
- Panels don't toggle
- Performance issues

#### Solutions

**1. Use supported browser**
- ✅ Chrome/Edge (recommended)
- ✅ Safari
- ⚠️ Firefox (may have issues)

**2. Clear mobile browser cache**
- Settings → Privacy → Clear browsing data

**3. Check screen orientation**
- Portrait mode works best
- Landscape mode may need scrolling

**4. Reduce animations**
Edit `ParticleField.tsx` to use fewer particles:
```typescript
const particleCount = 25 // Reduced from 50
```

---

### 🎤 Voice Button Not Working

#### Symptoms
- Button doesn't respond
- No voice visualization
- No microphone access

#### Solutions

**1. Browser permissions**
- Allow microphone access when prompted
- Check browser settings → Privacy → Microphone

**2. Voice feature status**
Currently, voice button shows animations only.
Real voice recognition coming in future update.

**3. Use chat instead**
Type messages in the chat interface for full functionality.

---

### 🐌 Slow Performance

#### Symptoms
- Laggy animations
- Slow response times
- High CPU usage

#### Solutions

**1. Close other applications**
- Free up system resources
- Close unused browser tabs

**2. Reduce particle count**
Edit `ParticleField.tsx`:
```typescript
const particleCount = window.innerWidth < 768 ? 25 : 50
```

**3. Disable animations**
Add to `index.css`:
```css
* {
  animation: none !important;
  transition: none !important;
}
```

**4. Use lighter AI model**
Edit `api_server.py`:
```python
ollama = OllamaInterface(model="phi3:mini")  # Faster, less accurate
```

---

### 🔒 Port Already in Use

#### Symptoms
- Error: "Port 8000 is already in use"
- Error: "Port 5173 is already in use"

#### Solutions

**1. Kill existing processes**
```powershell
# Find process using port 8000
netstat -ano | findstr :8000
# Kill it (replace PID with actual number)
taskkill /PID <PID> /F

# Same for port 5173
netstat -ano | findstr :5173
taskkill /PID <PID> /F
```

**2. Use different ports**
Edit `vite.config.ts`:
```typescript
server: {
  port: 5174  // Changed from 5173
}
```

Edit `api_server.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8001)  # Changed from 8000
```

---

### 📦 Installation Issues

#### Symptoms
- npm install fails
- pip install fails
- Missing dependencies

#### Solutions

**1. Update Node.js**
- Download latest LTS from https://nodejs.org
- Minimum version: 18.x

**2. Update Python**
- Download from https://python.org
- Minimum version: 3.8

**3. Clear package caches**
```powershell
# Clear npm cache
npm cache clean --force

# Clear pip cache
pip cache purge
```

**4. Use administrator privileges**
- Right-click PowerShell
- "Run as Administrator"
- Retry installation

---

## 🆘 Still Having Issues?

### Diagnostic Checklist

- [ ] Python 3.8+ installed
- [ ] Node.js 18+ installed
- [ ] Ollama installed with phi3:medium
- [ ] All dependencies installed
- [ ] Both servers running
- [ ] Ports 8000 and 5173 available
- [ ] Browser cache cleared
- [ ] Firewall not blocking connections

### Get Help

1. **Check the logs**
   - API server window for Python errors
   - Frontend window for build errors
   - Browser console (F12) for runtime errors

2. **Restart everything**
   ```powershell
   # Close all terminal windows
   # Run START_HERE.bat again
   ```

3. **Fresh install**
   ```powershell
   cd OmniMind
   # Backend
   pip uninstall -r requirements.txt -y
   pip install -r requirements.txt
   
   # Frontend
   cd frontend
   rm -r node_modules
   npm install
   ```

---

**Most issues are resolved by ensuring both servers are running! 🚀**