from flask import Flask, request, jsonify
from flask_cors import CORS
import pyttsx3
import threading

app = Flask(__name__)
CORS(app)

# Initialize TTS
tts = pyttsx3.init()
tts.setProperty('rate', 180)

def speak(text):
    def _speak():
        tts.say(text)
        tts.runAndWait()
    threading.Thread(target=_speak, daemon=True).start()

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message', '')
    
    # Fast responses
    responses = {
        'hello': 'Hello! I am OmniMind, your AI assistant.',
        'hi': 'Hi there! How can I help you?',
        'how are you': 'I am functioning perfectly!',
        'what can you do': 'I can chat, answer questions, and help with tasks.',
        'time': 'The current time is available in your system.',
        'help': 'I am here to help! Ask me anything.'
    }
    
    # Get response
    msg_lower = message.lower()
    response = responses.get(msg_lower, f"I understand: {message}. I'm ready to help!")
    
    # Speak response
    speak(response)
    
    return jsonify({
        'response': response,
        'status': 'success',
        'speaking': True
    })

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({
        'status': 'operational',
        'neural_load': '25%',
        'processing': '2.4 GHz',
        'memory': '6.2/16 GB',
        'connection': 'Active'
    })

if __name__ == '__main__':
    print("OmniMind Backend Starting...")
    print("Server: http://localhost:7000")
    print("Voice: Enabled")
    app.run(host='0.0.0.0', port=7000, debug=False)