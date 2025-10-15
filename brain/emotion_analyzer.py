from typing import Dict, Any, Optional

try:
    from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
except Exception:  # transformers not installed yet
    AutoTokenizer = None
    AutoModelForSequenceClassification = None
    pipeline = None


class EmotionAnalyzer:
    """
    Uses the cardiffnlp/twitter-roberta-base-emotion model to detect user emotion.
    Falls back to neutral if the model isn't available.

    Emotions typically include: anger, joy, sadness, fear, love, surprise
    """

    def __init__(self, model_name: str = "cardiffnlp/twitter-roberta-base-emotion"):
        self.model_name = model_name
        self._pipe = None
        self._available = False
        self._init_pipeline()

    def _init_pipeline(self):
        if AutoTokenizer is None or AutoModelForSequenceClassification is None or pipeline is None:
            self._available = False
            return
        try:
            tok = AutoTokenizer.from_pretrained(self.model_name)
            mdl = AutoModelForSequenceClassification.from_pretrained(self.model_name)
            self._pipe = pipeline("text-classification", model=mdl, tokenizer=tok, return_all_scores=True, top_k=None)
            self._available = True
        except Exception:
            self._available = False

    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Returns a dict: { 'emotion': <label>, 'score': <confidence>, 'raw': <raw_output> }
        """
        if not text.strip():
            return {"emotion": "neutral", "score": 1.0, "raw": []}
        if not self._available:
            return {"emotion": "neutral", "score": 0.0, "raw": []}
        try:
            out = self._pipe(text)
            # out is typically a list of list of dicts when return_all_scores=True
            # e.g., [[{'label': 'anger', 'score': 0.01}, ...]]
            scores = out[0]
            best = max(scores, key=lambda x: x.get('score', 0.0)) if scores else {"label": "neutral", "score": 0.0}
            return {"emotion": best.get('label', 'neutral'), "score": float(best.get('score', 0.0)), "raw": scores}
        except Exception:
            return {"emotion": "neutral", "score": 0.0, "raw": []}

    @staticmethod
    def style_for_emotion(emotion: str) -> Dict[str, Any]:
        """
        Map emotion to response style and TTS adjustments.
        Returns: { 'tone': str, 'tts_rate_delta': int, 'preface': Optional[str] }
        """
        e = (emotion or "").lower()
        if e in ("sadness", "sad"):
            return {"tone": "gentle", "tts_rate_delta": -15, "preface": "I'm here with you. "}
        if e in ("anger", "angry"):
            return {"tone": "calm", "tts_rate_delta": -10, "preface": "Let's take a steady approach. "}
        if e in ("joy", "happy"):
            return {"tone": "upbeat", "tts_rate_delta": +5, "preface": "Great news! "}
        if e in ("fear", "anxious"):
            return {"tone": "reassuring", "tts_rate_delta": -10, "preface": "You're safe; we'll handle this carefully. "}
        if e in ("love",):
            return {"tone": "warm", "tts_rate_delta": 0, "preface": None}
        if e in ("surprise",):
            return {"tone": "neutral", "tts_rate_delta": 0, "preface": None}
        return {"tone": "neutral", "tts_rate_delta": 0, "preface": None}
