"""
OmniMind API Server - Port 8002
Copy of api_server.py running on port 8002
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import asyncio
from typing import Optional
import os

from brain.ollama_interface import OllamaInterface
from system_monitor import SystemMonitor
from skills_manager import skills_manager

app = FastAPI(title="OmniMind API")

# Initialize system monitor
system_monitor = SystemMonitor()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI with available model
ollama = OllamaInterface(model="qwen2.5:3b")

MEMORY_DIR = os.path.join(os.path.dirname(__file__), 'memory')
PROFILE_PATH = os.path.join(MEMORY_DIR, 'user_profile.json')
CONV_PATH = os.path.join(MEMORY_DIR, 'conversations.json')


class ChatMessage(BaseModel):
    message: str
    context: Optional[str] = None


@app.get("/")
async def root():
    return {"message": "OmniMind API is running", "version": "2.0", "port": 8002}


@app.get("/api/status")
async def get_status():
    """Get current system status with real-time data"""
    stats = system_monitor.get_all_stats()
    
    return {
        "status": "operational",
        "neural_load": f"{stats['cpu']['usage_percent']}%",
        "processing": f"{stats['cpu']['frequency_ghz']} GHz",
        "memory": f"{stats['memory']['used_gb']}/{stats['memory']['total_gb']} GB",
        "connection": "Active",
        "detailed": stats
    }


@app.get("/api/conversations")
async def get_conversations():
    """Get conversation history"""
    try:
        with open(CONV_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("history", [])[-20:]  # Last 20 messages
    except Exception:
        return []


@app.post("/api/chat")
async def chat(message: ChatMessage):
    """Send a message to OmniMind and get response"""
    try:
        # Ensure memory directory exists
        os.makedirs(MEMORY_DIR, exist_ok=True)
        
        # Check if message is a skill command
        detected_skill = skills_manager.detect_skill(message.message)
        
        if detected_skill:
            # Execute skill
            skill_result = skills_manager.execute_skill(detected_skill, message.message)
            
            if skill_result["success"]:
                response = f"✓ {skill_result['skill']}: {skill_result['result']}"
            else:
                response = f"✗ {skill_result['skill']}: {skill_result.get('error', 'Failed to execute')}"
        else:
            # Get AI response
            system_prompt = (
                "You are OmniMind — a wise, empathetic, and helpful personal AI. "
                "You run entirely on the user's device. Privacy is non-negotiable. "
                "Keep responses concise and helpful."
            )
            response = ollama.generate(system_prompt, message.message)

        # Save to conversation history
        try:
            with open(CONV_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception:
            data = {"history": []}
        
        import time
        data.setdefault("history", []).append({
            "timestamp": time.time(),
            "user": message.message,
            "assistant": response,
        })
        
        with open(CONV_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return {"response": response, "status": "success"}
    
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return {"response": f"Error: {str(e)}", "status": "error"}


if __name__ == "__main__":
    import uvicorn
    print("Starting OmniMind API Server on port 8002...")
    print("Frontend: http://localhost:5173")
    print("API Docs: http://localhost:8002/docs")
    uvicorn.run(app, host="0.0.0.0", port=8002)