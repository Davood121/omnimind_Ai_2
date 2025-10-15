import os
import json
from typing import Any, Dict

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from brain.ollama_interface import OllamaInterface
from brain.emotion_analyzer import EmotionAnalyzer
from skills.multi_search import multi_search
from skills.media_player import play_music
from skills.file_manager import manage_files
from skills.coder import generate_code
from utils.safety_guard import is_safe_command
from utils.error_doctor import ai_mini_error_doctor

app = Flask(__name__, static_folder='web', static_url_path='/')
CORS(app)

ollama = OllamaInterface(model="phi3:medium")
emotion = EmotionAnalyzer()


@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})


@app.route('/api/query', methods=['POST'])
def api_query():
    data: Dict[str, Any] = request.get_json(force=True, silent=True) or {}
    text = (data.get('text') or '').strip()
    if not text:
        return jsonify({"error": "empty input"}), 400

    try:
        emo_res = emotion.analyze(text)
    except Exception as e:
        diag = ai_mini_error_doctor('emotion-analyze', e)
        emo_res = {"emotion": "neutral", "score": 0, "diagnostic": diag}

    try:
        system_prompt = (
            "You are OmniMind — a wise, empathetic, and helpful personal AI. "
            "Privacy is non-negotiable. Be concise."
        )
        user_prompt = f"User said: '{text}'. Answer concisely."
        answer = ollama.generate(system_prompt, user_prompt)
        return jsonify({"answer": answer, "emotion": emo_res})
    except Exception as e:
        diag = ai_mini_error_doctor('ollama-generate', e)
        # Fallback to a simple deterministic response
        fallback = "I'm having trouble with the local AI engine. Here's a basic response."
        return jsonify({"answer": fallback, "emotion": emo_res, "diagnostic": diag}), 200


@app.route('/api/search', methods=['POST'])
def api_search():
    data = request.get_json(force=True, silent=True) or {}
    query = (data.get('query') or '').strip()
    if not query:
        return jsonify({"error": "empty query"}), 400
    if not is_safe_command(query):
        return jsonify({"error": "unsafe terms detected"}), 400
    try:
        results = multi_search(query, count_per_engine=5)
        return jsonify({"results": results})
    except Exception as e:
        diag = ai_mini_error_doctor('multi-search', e)
        return jsonify({"results": [], "diagnostic": diag}), 200


@app.route('/api/files', methods=['POST'])
def api_files():
    data = request.get_json(force=True, silent=True) or {}
    action = (data.get('action') or '').strip()
    path = (data.get('path') or '').strip()
    content = data.get('content')
    if action not in {"list", "read", "create"}:
        return jsonify({"error": "unsupported action"}), 400
    try:
        res = manage_files(action, path, content)
        return jsonify(res)
    except Exception as e:
        diag = ai_mini_error_doctor('file-manager', e)
        return jsonify({"error": str(e), "diagnostic": diag}), 400


@app.route('/api/code', methods=['POST'])
def api_code():
    data = request.get_json(force=True, silent=True) or {}
    task = (data.get('task') or '').strip()
    if not task:
        return jsonify({"error": "empty task"}), 400
    try:
        res = generate_code(task)
        return jsonify(res)
    except Exception as e:
        diag = ai_mini_error_doctor('code-generate', e)
        return jsonify({"error": str(e), "diagnostic": diag}), 400


@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', '5055'))
    app.run(host='127.0.0.1', port=port, debug=False)
