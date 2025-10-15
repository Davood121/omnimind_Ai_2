from flask import Flask, request, jsonify
from flask_cors import CORS
import pyttsx3
import threading
import time
import psutil

# Optional web search dependency (duckduckgo_search). Runs free with no API key.
try:
    from duckduckgo_search import DDGS
    SEARCH_AVAILABLE = True
    SEARCH_ERROR = None
except Exception as e:
    SEARCH_AVAILABLE = False
    SEARCH_ERROR = str(e)

try:
    from brain.ollama_interface import OllamaInterface
    ollama = OllamaInterface(model="qwen2.5:3b")
    AI_AVAILABLE = True
except:
    AI_AVAILABLE = False

try:
    from skills.news_fetcher import get_india_news, get_world_news
    NEWS_AVAILABLE = True
except:
    NEWS_AVAILABLE = False

try:
    from skills.weather import get_weather
    from skills.wikipedia_search import search_wikipedia
    from skills.time_date import get_current_time, get_date
    from skills.calculator import calculate
    EXTRA_SKILLS = True
except:
    EXTRA_SKILLS = False

app = Flask(__name__)
CORS(app)

# Initialize TTS with proper settings
tts_lock = threading.Lock()

def speak(text):
    """Speak text with proper TTS engine handling"""
    def _speak():
        with tts_lock:
            try:
                engine = pyttsx3.init()
                engine.setProperty('rate', 175)
                engine.setProperty('volume', 1.0)
                
                # Get available voices
                voices = engine.getProperty('voices')
                if len(voices) > 1:
                    engine.setProperty('voice', voices[1].id)  # Female voice
                
                engine.say(text)
                engine.runAndWait()
                engine.stop()
            except Exception as e:
                print(f"TTS Error: {e}")
    
    thread = threading.Thread(target=_speak, daemon=True)
    thread.start()
    return thread

def estimate_speech_duration(text):
    """Estimate how long it takes to speak the text"""
    words = len(text.split())
    # Average speaking rate: 175 words per minute = ~2.9 words per second
    duration = (words / 2.9) * 1000  # Convert to milliseconds
    return int(duration)

# -----------------------
# Real-time Web Search
# -----------------------

def perform_web_search(query, max_results=5, region='wt-wt', safesearch='moderate', timelimit=None):
    """Perform a free, real-time web search using DuckDuckGo.
    Returns a list of {title, url, snippet, source} dicts.
    """
    if not query or not isinstance(query, str):
        return []
    if SEARCH_AVAILABLE:
        try:
            results = []
            # DDGS().text returns an iterator of dicts: {title, href, body}
            with DDGS() as ddgs:
                rows = ddgs.text(
                    query,
                    region=region,
                    safesearch=safesearch,
                    timelimit=timelimit,
                    max_results=int(max_results)
                )
                for r in rows:
                    results.append({
                        'title': r.get('title'),
                        'url': r.get('href') or r.get('url'),
                        'snippet': r.get('body') or r.get('description') or r.get('snippet'),
                        'source': 'duckduckgo'
                    })
            return results
        except Exception as e:
            return [{
                'title': 'Search error',
                'url': None,
                'snippet': str(e),
                'source': 'duckduckgo'
            }]
    else:
        return [{
            'title': 'Search not available',
            'url': None,
            'snippet': 'Install duckduckgo-search to enable web search.',
            'source': 'system',
            'error': SEARCH_ERROR
        }]

def synthesize_from_results(query, results):
    """If AI is available, synthesize a concise answer from search results with citations."""
    if not AI_AVAILABLE or not results:
        return None
    try:
        bullets = []
        for idx, r in enumerate(results, start=1):
            title = r.get('title') or 'Result'
            snippet = r.get('snippet') or ''
            url = r.get('url') or ''
            bullets.append(f"[{idx}] {title}: {snippet} (source: {url})")
        context = "\n".join(bullets)
        system_prompt = (
            "You are OmniMind, a holographic AI assistant. "
            "Use the provided web results to answer concisely with citations like [1], [2]. "
            "If uncertain, say so."
        )
        user_message = (
            f"Question: {query}\n"
            f"Web results:\n{context}\n"
            "Provide a 2-6 sentence answer with citations."
        )
        return ollama.generate(system_prompt, user_message)
    except Exception as e:
        return f"Unable to synthesize answer: {e}"

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message', '')
    msg_lower = message.lower()
    
    # Check for news queries
    if NEWS_AVAILABLE and ('news' in msg_lower or 'headlines' in msg_lower):
        if 'india' in msg_lower:
            response = get_india_news()
        elif 'world' in msg_lower:
            response = get_world_news()
        else:
            response = get_india_news()
    # Weather
    elif EXTRA_SKILLS and 'weather' in msg_lower:
        city = 'Delhi'
        if 'in' in msg_lower:
            words = message.split()
            try:
                city = words[words.index('in') + 1]
            except:
                pass
        response = get_weather(city)
    # Wikipedia
    elif EXTRA_SKILLS and ('what is' in msg_lower or 'who is' in msg_lower or 'tell me about' in msg_lower):
        query = message.replace('what is', '').replace('who is', '').replace('tell me about', '').strip()
        response = search_wikipedia(query)
    # Time
    elif EXTRA_SKILLS and ('time' in msg_lower or 'clock' in msg_lower):
        response = get_current_time()
    # Date
    elif EXTRA_SKILLS and ('date' in msg_lower or 'today' in msg_lower and 'is' in msg_lower):
        response = get_date()
    # Calculator
    elif EXTRA_SKILLS and ('calculate' in msg_lower or 'solve' in msg_lower or any(op in message for op in ['+', '-', '*', '/', '='])):
        expr = message.replace('calculate', '').replace('solve', '').replace('what is', '').strip()
        response = calculate(expr)
    # Use real AI if available
    elif AI_AVAILABLE:
        try:
            system_prompt = "You are OmniMind, a holographic AI assistant. Keep responses concise and helpful."
            response = ollama.generate(system_prompt, message)
        except:
            response = f"I understand your question about '{message}'. Let me help you with that."
    else:
        # Fallback responses
        responses = {
            'hello': 'Hello! I am OmniMind, your holographic AI assistant.',
            'hi': 'Hi there! Your holographic interface is fully operational.',
            'how are you': 'All systems are functioning at optimal levels!',
            'what can you do': 'I can chat, control systems, play music, search the web, and synchronize with your holographic display.',
        }
        
        msg_lower = message.lower().strip()
        response = None
        
        for key, resp in responses.items():
            if key in msg_lower:
                response = resp
                break
        
        if not response:
            response = f"I understand your question about '{message}'. Let me help you with that."
    
    # Speak response and calculate duration for hologram sync
    speak_thread = speak(response)
    speech_duration = estimate_speech_duration(response)
    
    return jsonify({
        'response': response,
        'status': 'success',
        'speaking': True,
        'speech_duration': speech_duration,
        'hologram_sync': True
    })

@app.route('/api/search', methods=['GET', 'POST'])
def search():
    """Real-time web search endpoint with optional AI summarization.
    Accepts GET params or POST JSON: {q/query, max_results, region, safesearch, timelimit, summarize}
    """
    data = request.get_json() if request.method == 'POST' else request.args
    data = data or {}
    query = data.get('q') or data.get('query') or ''
    max_results = int(data.get('max_results', 5))
    region = data.get('region', 'wt-wt')
    safesearch = data.get('safesearch', 'moderate')
    timelimit = data.get('timelimit') or None
    summarize = data.get('summarize', False)

    if isinstance(summarize, str):
        summarize = summarize.lower() in ('1', 'true', 'yes', 'y', 'on')

    results = perform_web_search(query, max_results, region, safesearch, timelimit)
    answer = synthesize_from_results(query, results) if summarize else None

    return jsonify({
        'query': query,
        'results': results,
        'answer': answer,
        'ai_available': AI_AVAILABLE,
        'search_available': SEARCH_AVAILABLE
    })

@app.route('/api/status', methods=['GET'])
def status():
    # Get real system stats
    cpu_percent = psutil.cpu_percent(interval=0.1)
    memory = psutil.virtual_memory()
    
    return jsonify({
        'status': 'operational',
        'neural_load': f'{cpu_percent:.1f}%',
        'processing': '2.4 GHz',
        'memory': f'{memory.used/1024**3:.1f}/{memory.total/1024**3:.1f} GB',
        'connection': 'Active'
    })

@app.route('/api/conversations', methods=['GET'])
def conversations():
    return jsonify([
        {
            'timestamp': time.time(),
            'user': 'System initialized',
            'assistant': 'OmniMind holographic interface is now active.'
        }
    ])

@app.route('/api/execute-skill', methods=['POST'])
def execute_skill():
    data = request.get_json()
    skill_id = data.get('skill_id', '')
    query = data.get('query', '')

    # Web search skill (real-time info)
    if skill_id in ('web_search', 'search'):
        max_results = int(data.get('max_results', 5))
        region = data.get('region', 'wt-wt')
        safesearch = data.get('safesearch', 'moderate')
        timelimit = data.get('timelimit') or None
        summarize = data.get('summarize', False)
        if isinstance(summarize, str):
            summarize = summarize.lower() in ('1', 'true', 'yes', 'y', 'on')

        results = perform_web_search(query, max_results, region, safesearch, timelimit)
        answer = synthesize_from_results(query, results) if summarize else None
        if answer:
            speak(answer)
        return jsonify({
            'success': True,
            'skill_id': skill_id,
            'query': query,
            'results': results,
            'answer': answer,
            'ai_available': AI_AVAILABLE,
            'search_available': SEARCH_AVAILABLE
        })

    # Default skill execution (placeholder)
    result = f"Executing {skill_id}: {query}"
    speak(result)
    
    return jsonify({
        'success': True,
        'result': result
    })

if __name__ == '__main__':
    print("OmniMind Holographic Backend")
    print("=" * 40)
    print("Server: http://localhost:8000")
    print("Voice: Enabled")
    print("Hologram: Synchronized")
    print(f"AI Model: {'qwen2.5:3b' if AI_AVAILABLE else 'Basic Responses'}")
    print(f"Search: {'Enabled' if SEARCH_AVAILABLE else 'Disabled'}")
    print(f"Extra Skills: {'Enabled' if EXTRA_SKILLS else 'Disabled'}")
    print("  - News, Weather, Wikipedia, Time, Calculator")
    print("=" * 40)
    app.run(host='0.0.0.0', port=8000, debug=False)
