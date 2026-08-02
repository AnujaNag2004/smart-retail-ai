from pathlib import Path
import pickle

import cv2

MODEL_FOLDER = Path(__file__).resolve().parents[1] / "models"
RECOGNIZER_PATH = MODEL_FOLDER / "lbph_face_recognizer.yml"
FACE_DATABASE_PATH = MODEL_FOLDER / "face_db.pkl"

FACE_MATCH_THRESHOLD = 150.0


def load_face_recognizer():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(str(RECOGNIZER_PATH))

    with open(FACE_DATABASE_PATH, "rb") as file:
        label_to_customer = pickle.load(file)

    return recognizer, label_to_customer


def recognize_face(image, recognizer, label_to_customer):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized_image = cv2.resize(gray_image, (64, 64))

    predicted_label, distance = recognizer.predict(resized_image)

    if distance > FACE_MATCH_THRESHOLD:
        return {
            "customer_id": None,
            "status": "unknown",
            "distance": round(float(distance), 2),
        }

    return {
        "customer_id": label_to_customer[predicted_label],
        "status": "returning_customer",
        "distance": round(float(distance), 2),
    }