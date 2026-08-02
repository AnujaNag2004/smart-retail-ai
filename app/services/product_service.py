from pathlib import Path

import cv2
import numpy as np
import tensorflow as tf

MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "product_classifier.h5"

CLASS_NAMES = [
    "T-shirt/top",
    "Trouser",
    "Pullover",
    "Dress",
    "Coat",
    "Sandal",
    "Shirt",
    "Sneaker",
    "Bag",
    "Ankle boot",
]


def load_product_model():
    return tf.keras.models.load_model(MODEL_PATH)


def predict_product(image, model):
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    resized_image = cv2.resize(rgb_image, (96, 96))
    model_input = np.expand_dims(resized_image.astype("float32"), axis=0)

    model_input = tf.keras.applications.mobilenet_v2.preprocess_input(model_input)

    probabilities = model.predict(model_input, verbose=0)[0]
    predicted_index = int(np.argmax(probabilities))

    return {
        "category": CLASS_NAMES[predicted_index],
        "confidence": round(float(probabilities[predicted_index]), 4),
    }