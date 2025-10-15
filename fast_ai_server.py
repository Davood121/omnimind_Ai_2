import http.server
import socketserver
import json
import pyttsx3
import threading
import time
from pathlib import Path

# Initialize TTS engine
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 180)
tts_engine.setProperty('volume', 0.9)

# Simple fast responses
QUICK_RESPONSES = {
    "hello": "Hello! I'm OmniMind, your AI assistant.",
    "hi": "Hi there! How can I help you today?",
    "how are you": "I'm functioning perfectly and ready to assist!",
    "what can you do": "I can chat, answer questions, and help with various tasks.",
    "play music": "Opening YouTube music search for you!",
    "search": "Searching the web for your query!",
    "time": f"The current time is {time.strftime('%H:%M:%S')}",
    "date": f"Today is {time.strftime('%Y-%m-%d')}",
    "weather": "I'd need internet access to check the weather for you.",
    "joke": "Why don't scientists trust atoms? Because they make up everything!",
    "help": "I'm here to help! Ask me anything or try commands like 'play music' or 'search'."
}

def get_fast_response(message):
    """Get quick AI response without heavy models"""
    msg_lower = message.lower().strip()
    
    # Check for exact matches
    if msg_lower in QUICK_RESPONSES:
        return QUICK_RESPONSES[msg_lower]
    
    # Check for partial matches
    for key, response in QUICK_RESPONSES.items():
        if key in msg_lower:
            return response
    
    # Default intelligent response
    if "?" in message:
        return f"That's an interesting question about '{message}'. I'm processing with my fast response system!"
    else:
        return f"I understand you said '{message}'. I'm OmniMind, ready to help with any task!"

def speak_text(text):
    """Speak text using TTS in background thread"""
    def speak():
        try:
            tts_engine.say(text)
            tts_engine.runAndWait()
        except:
            pass
    
    thread = threading.Thread(target=speak, daemon=True)
    thread.start()

class FastAIHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/chat':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            message = data.get('message', '')
            
            # Get fast response
            ai_response = get_fast_response(message)
            
            # Speak the response
            speak_text(ai_response)
            
            response = {
                "response": ai_response,
                "status": "success",
                "speaking": True,
                "voice_active": True,
                "hologram_sync": True
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        elif self.path == '/api/status':
            response = {
                "status": "operational",
                "neural_load": "15%",
                "processing": "2.4 GHz",
                "memory": "4.2/16 GB",
                "connection": "Active",
                "voice_ready": True,
                "hologram_active": True
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

PORT = 9000
print("OmniMind Fast AI Server")
print("=" * 40)
print(f"Server: http://localhost:{PORT}")
print("Voice: Enabled")
print("Hologram: Synchronized")
print("Speed: Ultra Fast")
print("=" * 40)

with socketserver.TCPServer(("", PORT), FastAIHandler) as httpd:
    httpd.serve_forever()