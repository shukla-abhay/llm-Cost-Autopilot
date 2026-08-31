"""
Train the complexity classifier on routing_dataset.json and save it.
Run: python -m app.router.train
"""

import json
import joblib
from pathlib import Path
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from app.router.classifier import extract_features

DATASET_PATH = Path(__file__).parent.parent.parent.parent / "datasets" / "routing_dataset.json"
MODEL_PATH = Path(__file__).parent.parent.parent.parent / "models" / "classifier.pkl"


def train():
    data = json.loads(DATASET_PATH.read_text())

    X = [extract_features(d["prompt"]) for d in data]
    y = [d["complexity"] for d in data]

    model = LogisticRegression(max_iter=1000)

    scores = cross_val_score(model, X, y, cv=5)
    print(f"Cross-validation accuracy: {scores.mean():.2%} (+/- {scores.std():.2%})")

    model.fit(X, y)

    MODEL_PATH.parent.mkdir(exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

    # Quick test
    tests = [
        "What is the capital of France?",
        "Write a Python function to check if a number is prime.",
        "Design a scalable microservices architecture for 1 million users.",
    ]
    for t in tests:
        from app.router.classifier import predict
        # reload after save
        result = predict(t)
        print(f"[{result['complexity'].upper()} {result['confidence']}] {t[:60]}")


if __name__ == "__main__":
    train()
