"""
Complexity Classifier — prompt ko easy/medium/hard classify karta hai.
"""

import re
import joblib
from pathlib import Path

import os
MODEL_PATH = Path(os.getenv("MODEL_PATH", str(Path(__file__).parent.parent.parent.parent / "models" / "classifier.pkl")))

HARD_KEYWORDS = [
    "analyze", "analysis", "compare", "comparison", "design", "architecture",
    "prove", "proof", "mathematical", "derive", "derivation", "optimize",
    "security", "vulnerability", "research", "thesis", "dissertation",
    "multi", "multiple", "several", "comprehensive", "detailed", "in-depth",
    "step-by-step", "trade-off", "tradeoff", "scalable", "distributed",
    "fault-tolerant", "formal", "induction", "complexity", "algorithm"
]

MEDIUM_KEYWORDS = [
    "explain", "summarize", "summary", "write", "draft", "compare",
    "difference", "how does", "how do", "create", "build", "develop",
    "describe", "discuss", "review", "evaluate", "plan", "design"
]


def extract_features(prompt: str) -> list:
    text = prompt.lower()
    words = text.split()

    length = len(words)
    hard_kw = sum(1 for k in HARD_KEYWORDS if k in text)
    medium_kw = sum(1 for k in MEDIUM_KEYWORDS if k in text)
    question_marks = text.count("?")
    sentences = len(re.findall(r'[.!?]', text)) + 1
    avg_word_len = sum(len(w) for w in words) / max(len(words), 1)

    return [length, hard_kw, medium_kw, question_marks, sentences, avg_word_len]


def predict(prompt: str) -> dict:
    model = joblib.load(MODEL_PATH)
    features = [extract_features(prompt)]
    label = model.predict(features)[0]
    proba = model.predict_proba(features)[0]
    classes = model.classes_.tolist()
    confidence = round(float(proba[classes.index(label)]), 3)
    return {"complexity": label, "confidence": confidence}
