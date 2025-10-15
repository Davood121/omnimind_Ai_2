# OmniMind - Run Instructions

## What You Built

A complete, voice-first, self-evolving AI assistant with:
- **Local AI Brain**: Ollama with phi3:medium (reasoning) and codellama:7b-instruct (coding)
- **Voice Interface**: Speech recognition + text-to-speech
- **Emotion Analysis**: Adapts tone based on your mood
- **Open-Source Search**: SearXNG, Wikipedia, YaCy (concurrent, free)
- **Safe File Manager**: List/read/create files (home directory only)
- **Code Generator**: Creates code but never executes without permission
- **Web UI**: Modern dark interface with voice/text input
- **AI Error Doctor**: Auto-diagnoses issues and applies safe fallbacks

---

## Quick Start (3 Steps)

### Step 1: Start Ollama
Open a terminal and run:
```bash
ollama pull phi3:medium
ollama run phi3:medium
```
Keep this terminal open. Ollama must be running for AI features to work.

### Step 2: Start the Web Server
Double-click: **START_WEB.bat**

Or manually:
```bash
cd "c:\Users\davoo\OneDrive\Desktop\AI  penta dose\OmniMind"
python server.py
```

### Step 3: Open in Browser
Visit: **http://127.0.0.1:5055/**

---

## Using OmniMind

### Web Interface
- **Text Input**: Type your message and click Send
- **Voice Input**: Click the 🎤 mic button (uses browser speech recognition)
- **Web Search**: Use the search box to query open-source engines
- **Status**: Shows "Thinking...", "Searching...", "OK", or "Error"

### Voice Desktop App (Alternative)
Run: `python main.py`
- Say: "play Indian song" → Opens YouTube search (no autoplay)
- Say: "search latest Python news" → Returns aggregated results
- Say: "list ~/Documents" → Lists files safely
- All actions require your permission ("Shall I proceed?")

---

## Features & Commands

### 1. Ask Questions
- Type or say: "What is quantum computing?"
- Uses local phi3:medium model (private, offline)

### 2. Web Search (Open-Source)
- Type: "search latest AI news"
- Queries: SearXNG + Wikipedia + YaCy concurrently
- Returns merged, de-duplicated results
- Never auto-opens links

### 3. Play Music
- Say: "play Indian classical music"
- Opens YouTube search for royalty-free tracks
- No autoplay, no downloads

### 4. File Operations (Safe)
- "list ~/Documents" → Lists directory
- "read ~/Documents/notes.txt" → Reads file
- "create ~/Documents/ideas.txt" → Creates empty file
- Restricted to your home directory only

### 5. Code Generation
- "generate code to merge CSV files"
- Uses codellama:7b-instruct
- Returns code as text, never executes

### 6. Emotion Adaptation
- Detects your mood from text
- Adjusts response tone (gentle/calm/upbeat)
- Changes TTS speed slightly

---

## Configuration

### Open-Source Search Engines
Edit `config.json`:
```json
{
  "searxng_url": "https://searxng.example.org",
  "yacy_url": "http://localhost:8090"
}
```

Or set environment variables:
```powershell
setx SEARXNG_URL "https://searxng.example.org"
setx YACY_URL "http://localhost:8090"
```

**Note**: Wikipedia works without config. If SearXNG/YaCy aren't configured, you'll get partial results.

### Change Server Port
```powershell
setx PORT 5056
```
Then restart the server and visit: http://127.0.0.1:5056/

---

## Troubleshooting

### "I'm having trouble with the local AI engine"
**Problem**: Ollama not running or model not pulled
**Fix**:
```bash
ollama pull phi3:medium
ollama run phi3:medium
```
Keep the terminal open.

### "Web search failed"
**Problem**: Search engines not configured
**Fix**: 
- Wikipedia always works (no config needed)
- For full results, set `searxng_url` in config.json
- Or use a public SearXNG instance: https://searx.space

### Microphone not working (web)
**Problem**: Browser permissions
**Fix**: 
- Click the mic icon
- Allow microphone access when prompted
- Chrome/Edge work best for Web Speech API

### PyAudio installation failed
**Problem**: Windows binary not available via pip
**Fix**:
```bash
pip install pipwin
pipwin install pyaudio
```

### Torch installation too large
**Problem**: Full PyTorch is 2GB+
**Fix** (CPU-only, smaller):
```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

### Port already in use
**Problem**: Another app using port 5055
**Fix**: Change port (see Configuration above)

---

## AI Mini Error Doctor

OmniMind automatically diagnoses common issues:

| Error Category | Auto-Action | User Advice |
|---------------|-------------|-------------|
| Ollama unreachable | Fallback response | Start Ollama: `ollama run phi3:medium` |
| SearXNG down | Partial results (Wikipedia + YaCy) | Check SEARXNG_URL in config.json |
| YaCy down | Partial results (SearXNG + Wikipedia) | Start YaCy or remove from config |
| Transformers missing | Disable emotion temporarily | `pip install transformers torch` |

All diagnostics appear in API responses under `"diagnostic"` field.

---

## Architecture

```
OmniMind/
├── server.py              # Flask backend (serves web + APIs)
├── main.py                # Voice-first desktop app
├── config.json            # Configuration (search URLs, etc.)
├── requirements.txt       # Python dependencies
├── brain/
│   ├── ollama_interface.py    # Local AI client
│   └── emotion_analyzer.py    # Mood detection
├── skills/
│   ├── multi_search.py        # Concurrent search aggregator
│   ├── search_engines.py      # SearXNG, Wikipedia, YaCy
│   ├── media_player.py        # YouTube search (no autoplay)
│   ├── file_manager.py        # Safe file ops
│   └── coder.py               # Code generation
├── utils/
│   ├── safety_guard.py        # Dangerous command blocker
│   ├── error_doctor.py        # Auto-diagnostics
│   └── config.py              # Config loader
├── memory/
│   ├── user_profile.json      # Your preferences
│   └─�� conversations.json     # Interaction history
└── web/
    ├── index.html             # Frontend UI
    ├── styles.css             # Dark theme
    └── script.js              # API client + voice input
```

---

## Privacy & Safety

✅ **100% Local AI**: All reasoning happens on your machine via Ollama  
✅ **No Cloud**: No data sent to external AI services  
✅ **Permission-Gated**: Always asks before taking action  
✅ **Safe File Access**: Restricted to home directory with path validation  
✅ **No Auto-Execution**: Code generation returns text only  
✅ **Dangerous Command Blocker**: Denies rm, del, format, etc.  
✅ **Open-Source Search**: SearXNG, Wikipedia, YaCy (no tracking)  

---

## Next Steps

### Add More Skills
1. Calendar integration
2. Email drafting (local only)
3. Note-taking with tags
4. Task automation

### Improve Memory
1. Better conversation summarization
2. Long-term preference learning
3. Context-aware responses

### Enhance UI
1. WebSocket streaming for real-time responses
2. Dark/light theme toggle
3. Voice output in browser (Web Speech Synthesis API)

---

## Support

If you encounter issues:
1. Check TROUBLESHOOTING.md
2. Verify Ollama is running: `ollama list`
3. Test API health: http://127.0.0.1:5055/api/health
4. Check browser console (F12) for frontend errors

---

**You now have a fully functional, private, voice-first AI assistant!**

Enjoy OmniMind! 🚀
