from pathlib import Path
import re

import joblib

MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "sentiment_model.pkl"


def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def load_sentiment_model():
    return joblib.load(MODEL_PATH)


def analyze_sentiment(text, model):
    cleaned_text = clean_text(text)
    probabilities = model.predict_proba([cleaned_text])[0]
    predicted_index = int(probabilities.argmax())

    return {
        "sentiment": model.classes_[predicted_index],
        "confidence": round(float(probabilities[predicted_index]), 4),
    }