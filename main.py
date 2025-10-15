-import json
import os
import time
from typing import Dict, Any

import speech_recognition as sr
import pyttsx3

from brain.ollama_interface import OllamaInterface
from brain.emotion_analyzer import EmotionAnalyzer
from skills.media_player import play_music
from skills.multi_search import multi_search
from skills.file_manager import manage_files
from skills.coder import generate_code
from utils.safety_guard import is_safe_command


SYSTEM_PROMPT_BASE = (
    "You are OmniMind — a wise, empathetic, and helpful personal AI. "
    "You run entirely on the user's device. Privacy is non-negotiable. "
    "You adapt your tone based on the user's emotion and history. "
    "You never perform irreversible actions without explicit consent. "
    "Remember: {user_summary}. Always explain what you'll do and ask: 'Shall I proceed?' "
    "Prioritize safety, clarity, and kindness."
)

MEMORY_DIR = os.path.join(os.path.dirname(__file__), 'memory')
PROFILE_PATH = os.path.join(MEMORY_DIR, 'user_profile.json')
CONV_PATH = os.path.join(MEMORY_DIR, 'conversations.json')
SUMMARY_CACHE = os.path.join(MEMORY_DIR, 'last_summary.txt')


def ensure_memory_files():
    os.makedirs(MEMORY_DIR, exist_ok=True)
    if not os.path.exists(PROFILE_PATH):
        with open(PROFILE_PATH, 'w', encoding='utf-8') as f:
            json.dump({
                "preferences": {"tone": "neutral", "verbosity": "concise", "music": []},
                "summary": "User profile initialized. No preferences learned yet."
            }, f, ensure_ascii=False, indent=2)
    if not os.path.exists(CONV_PATH):
        with open(CONV_PATH, 'w', encoding='utf-8') as f:
            json.dump({"history": []}, f, ensure_ascii=False, indent=2)
    if not os.path.exists(SUMMARY_CACHE):
        with open(SUMMARY_CACHE, 'w', encoding='utf-8') as f:
            f.write("")


def load_user_summary() -> str:
    try:
        with open(PROFILE_PATH, 'r', encoding='utf-8') as f:
            profile = json.load(f)
        return profile.get('summary', 'No user summary available yet.')
    except Exception:
        return 'No user summary available yet.'


def append_conversation(user_text: str, assistant_text: str):
    try:
        with open(CONV_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        data = {"history": []}
    data.setdefault("history", []).append({
        "timestamp": time.time(),
        "user": user_text,
        "assistant": assistant_text,
    })
    with open(CONV_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def speak(engine, text: str):
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception:
        pass


def listen(recognizer: sr.Recognizer, mic: sr.Microphone) -> str:
    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=20)
        try:
            # Use Google Web Speech API (free). Requires internet.
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            return "[speech_recognition_error]"
    except Exception:
        return ""


def decide_action(nl_instruction: str) -> Dict[str, Any]:
    """
    Very small rule-based intent detector for Phase 1.
    We'll ask Ollama for better parsing in later phases.
    """
    lower = nl_instruction.lower()
    if any(k in lower for k in ["play", "song", "music"]):
        return {"action": "play_music", "query": nl_instruction}
    return {"action": "answer", "query": nl_instruction}


def ask_permission(engine, description: str) -> bool:
    prompt = f"I can {description}. Shall I proceed?"
    print(prompt)
    speak(engine, prompt)
    # For Phase 1, get a quick yes/no via voice; fallback to keyboard enter
    r = sr.Recognizer()
    try:
        with sr.Microphone() as m:
            r.adjust_for_ambient_noise(m, duration=0.5)
            audio = r.listen(m, timeout=5, phrase_time_limit=4)
        try:
            text = r.recognize_google(audio).lower()
            if any(x in text for x in ["yes", "yeah", "yup", "sure", "ok"]):
                return True
            if any(x in text for x in ["no", "nope", "stop", "cancel"]):
                return False
        except Exception:
            pass
    except Exception:
        pass
    print("Press Enter to proceed, or type 'n' to cancel: ", end="")
    ans = input().strip().lower()
    return ans != 'n'


def main():
    ensure_memory_files()

    user_summary = load_user_summary()
    system_prompt = SYSTEM_PROMPT_BASE.format(user_summary=user_summary)

    # Init TTS engine
    tts_engine = pyttsx3.init()
    tts_engine.setProperty('rate', 175)

    # Init ASR
    recognizer = sr.Recognizer()
    try:
        mic = sr.Microphone()
    except Exception as e:
        print("Microphone not available:", e)
        speak(tts_engine, "Microphone not available. Exiting.")
        return

    # Init Ollama
    ollama = OllamaInterface(model="phi3:medium")

    # Summarize recent history for profile context
    try:
        with open(CONV_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        history = data.get('history', [])[-20:]
        convo_text = "\n".join([f"User: {h.get('user','')}\nAssistant: {h.get('assistant','')}" for h in history])
        if convo_text.strip():
            summary_prompt = (
                "Summarize the user's stable preferences in one short sentence. "
                "Focus on likes/dislikes and desired answer style."
            )
            new_summary = ollama.generate(
                SYSTEM_PROMPT_BASE.format(user_summary=user_summary),
                f"Recent interactions:\n{convo_text}\n\n{summary_prompt}",
                temperature=0.1,
                max_tokens=128,
            ).strip()
            # Update profile
            with open(PROFILE_PATH, 'r', encoding='utf-8') as pf:
                profile = json.load(pf)
            profile['summary'] = new_summary or profile.get('summary', '')
            with open(PROFILE_PATH, 'w', encoding='utf-8') as pf:
                json.dump(profile, pf, ensure_ascii=False, indent=2)
            # Persist for visibility
            with open(SUMMARY_CACHE, 'w', encoding='utf-8') as sf:
                sf.write(profile['summary'])
            # Refresh system prompt
            user_summary = profile['summary']
            system_prompt = SYSTEM_PROMPT_BASE.format(user_summary=user_summary)
    except Exception:
        pass

    print("OmniMind is listening. Say something like 'play Indian song'. Ctrl+C to exit.")
    speak(tts_engine, "OmniMind is ready.")

    while True:
        try:
            print("Listening...")
            user_text = listen(recognizer, mic)
            if not user_text:
                continue
            if user_text == "[speech_recognition_error]":
                msg = "Speech recognition service is unavailable at the moment."
                print(msg)
                speak(tts_engine, msg)
                time.sleep(1)
                continue

            print("You:", user_text)

            # Emotion analysis and tone adaptation
            emo = EmotionAnalyzer()
            emo_res = emo.analyze(user_text)
            style = EmotionAnalyzer.style_for_emotion(emo_res.get('emotion'))
            # Adjust TTS rate temporarily
            base_rate = tts_engine.getProperty('rate')
            tts_engine.setProperty('rate', max(120, min(220, base_rate + style.get('tts_rate_delta', 0))))

            intent = decide_action(user_text)

            if intent["action"] == "play_music":
                will_do = f"search YouTube for royalty-free results matching: {intent['query']} and open results in your browser without auto-playing"
                if ask_permission(tts_engine, will_do):
                    result = play_music(intent['query'])
                    reply = (style.get('preface') or '') + result
                    print(reply)
                    speak(tts_engine, reply)
                    append_conversation(user_text, reply)
                else:
                    msg = (style.get('preface') or '') + "Canceled as requested."
                    print(msg)
                    speak(tts_engine, msg)
                    append_conversation(user_text, msg)
                # Restore voice rate
                tts_engine.setProperty('rate', base_rate)
                continue

            # Web search intent (open-source engines, concurrent)
            if any(k in user_text.lower() for k in ["search", "look up", "find on the web"]):
                if not is_safe_command(user_text):
                    deny_msg = (style.get('preface') or '') + "This request includes unsafe terms, so I won't proceed."
                    print(deny_msg)
                    speak(tts_engine, deny_msg)
                    append_conversation(user_text, deny_msg)
                else:
                    will_do = (
                        f"search using open-source engines (SearXNG, Wikipedia, YaCy) for: {user_text}. "
                        "I will not open links without your permission."
                    )
                    if ask_permission(tts_engine, will_do):
                        try:
                            results = multi_search(user_text, count_per_engine=5)
                            lines = [f"{i+1}. {r.get('title','(no title)')} - {r.get('url','')}" for i, r in enumerate(results[:10])]
                            answer = (style.get('preface') or '') + ("\n".join(lines) if lines else "No results found.")
                        except Exception as e:
                            answer = (style.get('preface') or '') + f"Web search failed: {e}"
                        print(answer)
                        speak(tts_engine, answer)
                        append_conversation(user_text, answer)
                    else:
                        msg = (style.get('preface') or '') + "Canceled as requested."
                        print(msg)
                        speak(tts_engine, msg)
                        append_conversation(user_text, msg)
                tts_engine.setProperty('rate', base_rate)
                continue

            # File manager intents
            if user_text.lower().startswith("list "):
                target = user_text[5:].strip() or '~'
                will_do = f"list files in: {target} (restricted to your home directory)."
                if ask_permission(tts_engine, will_do):
                    try:
                        res = manage_files('list', target)
                        entries = "\n".join(res['entries'][:50]) or "(empty)"
                        reply = (style.get('preface') or '') + f"Directory: {res['path']}\n{entries}"
                    except Exception as e:
                        reply = (style.get('preface') or '') + f"Failed to list: {e}"
                    print(reply)
                    speak(tts_engine, reply)
                    append_conversation(user_text, reply)
                else:
                    msg = (style.get('preface') or '') + "Canceled as requested."
                    print(msg)
                    speak(tts_engine, msg)
                    append_conversation(user_text, msg)
                tts_engine.setProperty('rate', base_rate)
                continue

            if user_text.lower().startswith("read "):
                target = user_text[5:].strip()
                will_do = f"read file: {target} (only within your home directory)."
                if ask_permission(tts_engine, will_do):
                    try:
                        res = manage_files('read', target)
                        snippet = res['content'][:800]
                        reply = (style.get('preface') or '') + f"First part of {res['path']}:\n{snippet}"
                    except Exception as e:
                        reply = (style.get('preface') or '') + f"Failed to read: {e}"
                    print(reply)
                    speak(tts_engine, reply)
                    append_conversation(user_text, reply)
                else:
                    msg = (style.get('preface') or '') + "Canceled as requested."
                    print(msg)
                    speak(tts_engine, msg)
                    append_conversation(user_text, msg)
                tts_engine.setProperty('rate', base_rate)
                continue

            if user_text.lower().startswith("create "):
                target = user_text[7:].strip()
                will_do = f"create a text file at: {target} (only within your home directory)."
                if ask_permission(tts_engine, will_do):
                    try:
                        res = manage_files('create', target)
                        reply = (style.get('preface') or '') + f"Created: {res['path']}"
                    except Exception as e:
                        reply = (style.get('preface') or '') + f"Failed to create: {e}"
                    print(reply)
                    speak(tts_engine, reply)
                    append_conversation(user_text, reply)
                else:
                    msg = (style.get('preface') or '') + "Canceled as requested."
                    print(msg)
                    speak(tts_engine, msg)
                    append_conversation(user_text, msg)
                tts_engine.setProperty('rate', base_rate)
                continue

            # Coding assistant intent
            if any(k in user_text.lower() for k in ["write code", "generate code", "create script"]):
                will_do = "draft code with CodeLlama and present it to you without executing anything."
                if ask_permission(tts_engine, will_do):
                    try:
                        res = generate_code(user_text)
                        explanation = res.get('explanation', '')[:800]
                        reply = (style.get('preface') or '') + explanation
                    except Exception as e:
                        reply = (style.get('preface') or '') + f"Code generation failed: {e}"
                    print(reply)
                    speak(tts_engine, reply)
                    append_conversation(user_text, reply)
                else:
                    msg = (style.get('preface') or '') + "Canceled as requested."
                    print(msg)
                    speak(tts_engine, msg)
                    append_conversation(user_text, msg)
                tts_engine.setProperty('rate', base_rate)
                continue

            # Fallback: ask Ollama to answer concisely.
            user_prompt = (
                (style.get('preface') or '') +
                "User said: '" + user_text + "'. "
                "If this is a request to perform an action, describe the safe steps and ask for permission. "
                "Otherwise, answer concisely."
            )
            answer = ollama.generate(system_prompt, user_prompt)
            print("OmniMind:", answer)
            speak(tts_engine, answer)
            append_conversation(user_text, answer)

            # Restore base TTS rate
            tts_engine.setProperty('rate', base_rate)

        except KeyboardInterrupt:
            print("Exiting OmniMind.")
            break
        except Exception as e:
            print("Unexpected error:", e)
            time.sleep(1)


if __name__ == "__main__":
    main()
