from pathlib import Path
import json
import random
import re

import joblib

MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "chatbot_model.pkl"
INTENTS_PATH = Path(__file__).resolve().parents[2] / "data" / "intents.json"


def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def load_chatbot():
    model = joblib.load(MODEL_PATH)

    with open(INTENTS_PATH, "r") as file:
        intents_data = json.load(file)

    responses_by_tag = {}
    patterns_by_tag = {}

    for intent in intents_data["intents"]:
        tag = intent["tag"]
        responses_by_tag[tag] = intent["responses"]
        patterns_by_tag[tag] = [clean_text(pattern) for pattern in intent["patterns"]]

    return model, responses_by_tag, patterns_by_tag


def get_chatbot_response(message, model, responses_by_tag, patterns_by_tag):
    cleaned_message = clean_text(message)

    for tag, patterns in patterns_by_tag.items():
        if cleaned_message in patterns:
            return {
                "reply": random.choice(responses_by_tag[tag]),
                "intent": tag,
                "confidence": 1.0,
            }

    probabilities = model.predict_proba([cleaned_message])[0]
    predicted_index = int(probabilities.argmax())
    confidence = float(probabilities[predicted_index])
    predicted_tag = model.classes_[predicted_index]

    if confidence < 0.35:
        return {
            "reply": "Sorry, I could not understand that. Please contact customer support for help.",
            "intent": "fallback",
            "confidence": round(confidence, 4),
        }

    return {
        "reply": random.choice(responses_by_tag[predicted_tag]),
        "intent": predicted_tag,
        "confidence": round(confidence, 4),
    }