"""
FastAPI server to bridge the React frontend with OmniMind backend.
Provides REST API endpoints for the holographic UI to interact with the AI.
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
from skills.real_time_search import search_anything, get_current_news
from skills.enhanced_news import get_detailed_news, get_breaking_news
from skills.conversation_enhancer import ConversationEnhancer, get_smart_suggestions
from skills.multi_engine_search import search_web_multi_engine
from skills.memory_enhancer import get_memory_context, save_memory_markers

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

# Initialize conversation enhancer (after MEMORY_DIR is defined)
# conv_enhancer will be initialized in the chat function

MEMORY_DIR = os.path.join(os.path.dirname(__file__), 'memory')
PROFILE_PATH = os.path.join(MEMORY_DIR, 'user_profile.json')
CONV_PATH = os.path.join(MEMORY_DIR, 'conversations.json')


class ChatMessage(BaseModel):
    message: str
    context: Optional[str] = None


class SystemStatus(BaseModel):
    status: str
    neural_load: str
    processing: str
    memory: str
    connection: str


@app.get("/")
async def root():
    return {"message": "OmniMind API is running", "version": "2.0"}


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


@app.get("/api/profile")
async def get_profile():
    """Get user profile"""
    try:
        with open(PROFILE_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {"preferences": {}, "summary": "No profile available"}


@app.get("/api/conversations")
async def get_conversations():
    """Get conversation history"""
    try:
        with open(CONV_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("history", [])[-20:]  # Last 20 messages
    except Exception:
        return []

@app.get("/api/greeting")
async def get_smart_greeting():
    """Get contextual greeting based on user patterns"""
    try:
        enhancer = ConversationEnhancer(MEMORY_DIR)
        greeting = enhancer.get_contextual_greeting()
        patterns = enhancer.analyze_conversation_patterns()
        
        return {
            "greeting": greeting,
            "context": patterns,
            "status": "success"
        }
    except Exception as e:
        return {
            "greeting": "Hello! How can I assist you today?",
            "context": {},
            "status": "error"
        }


@app.get("/api/skills")
async def get_skills():
    """Get list of available skills"""
    return {"skills": skills_manager.get_available_skills()}


@app.post("/api/execute-skill")
async def execute_skill(request: dict):
    """Execute a specific skill"""
    skill_id = request.get("skill_id")
    query = request.get("query", "")
    params = request.get("params", {})
    
    result = skills_manager.execute_skill(skill_id, query, params)
    return result


@app.post("/api/chat")
async def chat(message: ChatMessage):
    """Send a message to OmniMind and get response"""
    try:
        # Ensure memory directory exists
        os.makedirs(MEMORY_DIR, exist_ok=True)
        
        # Check for specific query types
        msg_lower = message.message.lower().strip()
        
        # Enhanced News queries with multi-engine search fallback
        if any(word in msg_lower for word in ['news', 'headlines', 'current events', 'latest news']):
            if 'ai' in msg_lower or 'artificial intelligence' in msg_lower:
                # Use multi-engine search for AI news
                response = search_web_multi_engine("latest AI artificial intelligence news")
            elif 'detailed' in msg_lower or 'summary' in msg_lower or 'analyze' in msg_lower:
                if 'india' in msg_lower:
                    response = get_detailed_news("India", 5)
                elif 'world' in msg_lower:
                    response = get_detailed_news("world", 5)
                else:
                    response = get_detailed_news("latest", 5)
            elif 'breaking' in msg_lower or 'urgent' in msg_lower:
                response = get_breaking_news()
            elif 'india' in msg_lower:
                response = get_detailed_news("India", 3)
            elif 'world' in msg_lower:
                response = get_detailed_news("world", 3)
            else:
                # Fallback to multi-engine search for general news
                try:
                    response = get_detailed_news("latest", 3)
                    if "Unable to fetch" in response or "temporarily unavailable" in response:
                        response = search_web_multi_engine("latest news today")
                except:
                    response = search_web_multi_engine("latest news today")
        
        # Let AI handle knowledge questions directly - no Wikipedia routing
        elif msg_lower.startswith(('what is ', 'who is ', 'define ', 'explain ', 'tell me about ', 'describe ')):
            # Skip to AI response - don't route to Wikipedia
            pass
        
        # Multi-engine web search for explicit search requests
        elif any(msg_lower.startswith(word) for word in ['search for ', 'find ', 'look up ', 'google ']) or 'search' in msg_lower:
            # Use multi-engine search for better results
            search_query = message.message.replace('search for ', '').replace('find ', '').replace('look up ', '').replace('google ', '').strip()
            response = search_web_multi_engine(search_query)
        else:
            # Check if message is a skill command
            detected_skill = skills_manager.detect_skill(message.message)
            
            if detected_skill:
                # Execute skill
                skill_result = skills_manager.execute_skill(detected_skill, message.message)
                
                if skill_result["success"]:
                    response = f"✓ {skill_result['skill']}: {skill_result['result']}"
                else:
                    response = f"✗ {skill_result['skill']}: {skill_result.get('error', 'Failed to execute')}"
                
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
                    "skill_executed": detected_skill
                })
                
                with open(CONV_PATH, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                # Add TTS for skill responses
                try:
                    import pyttsx3
                    import threading
                    
                    def speak_response():
                        try:
                            engine = pyttsx3.init()
                            engine.setProperty('rate', 175)
                            engine.say(response)
                            engine.runAndWait()
                            engine.stop()
                        except:
                            pass
                    
                    threading.Thread(target=speak_response, daemon=True).start()
                    
                    words = len(response.split())
                    speech_duration = (words / 2.9) * 1000
                    
                except:
                    speech_duration = 3000
                
                return {
                    "response": response, 
                    "status": "success", 
                    "skill_executed": detected_skill,
                    "speaking": True,
                    "speech_duration": int(speech_duration)
                }
        
        if 'response' in locals():
            # Save search/news response to conversation history
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
            
            # Add TTS for search/news responses too
            try:
                import pyttsx3
                import threading
                
                def speak_response():
                    try:
                        engine = pyttsx3.init()
                        engine.setProperty('rate', 175)
                        engine.say(response)
                        engine.runAndWait()
                        engine.stop()
                    except:
                        pass
                
                threading.Thread(target=speak_response, daemon=True).start()
                
                # Estimate speech duration
                words = len(response.split())
                speech_duration = (words / 2.9) * 1000
                
            except:
                speech_duration = 3000
            
            return {
                "response": response, 
                "status": "success",
                "speaking": True,
                "speech_duration": int(speech_duration)
            }
        
        # Load user summary
        try:
            with open(PROFILE_PATH, 'r', encoding='utf-8') as f:
                profile = json.load(f)
                user_summary = profile.get('summary', 'No user summary available.')
        except Exception:
            user_summary = 'No user summary available.'

        # Load conversation history for enhanced context
        try:
            with open(CONV_PATH, 'r', encoding='utf-8') as f:
                conv_data = json.load(f)
                recent_history = conv_data.get("history", [])[-10:]  # Last 10 exchanges for better context
        except Exception:
            recent_history = []
        
        # Build comprehensive context from recent conversation
        context = ""
        if recent_history:
            context = "\n\nConversation Memory (maintain continuity and reference previous topics):\n"
            for i, h in enumerate(recent_history, 1):
                user_msg = h.get('user', '')
                assistant_msg = h.get('assistant', '')
                context += f"[{i}] User: {user_msg}\n[{i}] Assistant: {assistant_msg}\n\n"
            
            # Add memory instructions
            context += "\nIMPORTANT: Reference previous messages when relevant. Build upon the conversation naturally."
        
        system_prompt = (
            "You are OmniMind — an advanced AI assistant with exceptional memory and contextual understanding. "
            "You are running locally on the user's device for complete privacy. "
            "\n\nCORE MEMORY ABILITIES:\n"
            "- ALWAYS remember and reference previous messages in our conversation\n"
            "- Build upon topics we've discussed before\n"
            "- Notice patterns in the user's questions and interests\n"
            "- Maintain conversation continuity across multiple exchanges\n"
            "- Connect current questions to previous context when relevant\n\n"
            "Your enhanced capabilities:\n"
            "- Contextual conversations that flow naturally\n"
            "- Deep understanding of user's communication style\n"
            "- Ability to recall and reference earlier topics\n"
            "- Intelligent follow-up questions based on conversation history\n"
            "- Adaptive responses based on user's demonstrated interests\n\n"
            f"User profile & preferences: {user_summary}\n"
            "CONVERSATION GUIDELINES:\n"
            "- Always check if current question relates to previous messages\n"
            "- Reference earlier topics when they're relevant\n"
            "- Build upon the conversation thread naturally\n"
            "- Show that you remember what we've discussed\n"
            "- Ask clarifying questions that show contextual understanding\n"
            f"{context}"
        )

        # Enhanced user prompt with strong memory emphasis
        user_prompt = f"Current user message: {message.message}\n\nIMPORTANT MEMORY INSTRUCTIONS:\n- Review our conversation history above\n- Reference previous topics if this message relates to them\n- Show that you remember what we've discussed\n- Build upon earlier exchanges naturally\n- If this continues a previous topic, acknowledge that connection\n\nProvide a contextually aware, engaging response that demonstrates your memory of our conversation."
        
        # Get AI response with better parameters
        response = ollama.generate(
            system_prompt, 
            user_prompt,
            temperature=0.6,  # Balanced creativity with consistency
            max_tokens=600    # Longer responses for detailed context
        )
        
        # Check if response contains error
        if response.startswith("[Error]"):
            return {"response": response, "status": "error"}
        
        # Initialize conversation enhancer
        conv_enhancer = ConversationEnhancer(MEMORY_DIR)
        
        # Enhance response with personality and context
        response = conv_enhancer.enhance_response(response, message.message)
        
        # Generate smart suggestions
        suggestions = get_smart_suggestions(message.message)
        
        # Update user preferences based on interaction
        conv_enhancer.update_user_preferences(message.message, response)
        
        # Save advanced memory markers
        save_memory_markers(MEMORY_DIR, message.message, response)

        # Add TTS functionality
        try:
            import pyttsx3
            import threading
            
            def speak_response():
                try:
                    engine = pyttsx3.init()
                    engine.setProperty('rate', 175)
                    engine.setProperty('volume', 1.0)
                    
                    # Get available voices
                    voices = engine.getProperty('voices')
                    if len(voices) > 1:
                        engine.setProperty('voice', voices[1].id)  # Female voice
                    
                    engine.say(response)
                    engine.runAndWait()
                    engine.stop()
                except Exception as e:
                    print(f"TTS Error: {e}")
            
            # Start TTS in background thread
            tts_thread = threading.Thread(target=speak_response, daemon=True)
            tts_thread.start()
            
            # Estimate speech duration
            words = len(response.split())
            speech_duration = (words / 2.9) * 1000  # ~2.9 words per second
            
        except Exception as e:
            print(f"TTS initialization failed: {e}")
            speech_duration = 3000  # Default 3 seconds

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

        return {
            "response": response, 
            "status": "success", 
            "speaking": True,
            "speech_duration": int(speech_duration),
            "hologram_sync": True,
            "suggestions": suggestions,
            "conversation_context": conv_enhancer.analyze_conversation_patterns()
        }
    
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return {"response": f"Error: {str(e)}", "status": "error"}


@app.websocket("/ws/voice")
async def websocket_voice(websocket: WebSocket):
    """WebSocket endpoint for real-time voice communication"""
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            # Process voice data here
            await websocket.send_text(json.dumps({
                "type": "status",
                "message": "Voice processing active"
            }))
    except WebSocketDisconnect:
        print("WebSocket disconnected")


if __name__ == "__main__":
    import uvicorn
    print("Starting OmniMind API Server...")
    print("Frontend: http://localhost:5173")
    print("API Docs: http://localhost:8000/docs")
    print("Enhanced AI Chat Features:")
    print("   - Contextual conversations")
    print("   - Smart suggestions")
    print("   - Personality adaptation")
    print("   - User preference learning")
    uvicorn.run(app, host="0.0.0.0", port=8000)