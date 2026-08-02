# AI-Powered Smart Retail & Customer Intelligence Platform

## 1. Project Overview

This project is a full-stack retail AI platform that combines computer vision, natural language processing, machine learning, REST APIs, and a dashboard.

The platform can:

- Classify product images into retail categories
- Recognize returning demo customers from face images
- Log customer visits in a database
- Analyze customer-review sentiment
- Answer retail FAQ questions using a chatbot
- Display customer intelligence statistics in a dashboard

## 2. System Architecture

```text
Streamlit Frontend / Swagger API
              |
              v
        FastAPI Backend
              |
   -------------------------
   |          |            |
   v          v            v
Vision      NLP        Chatbot
Module      Module     Module
   |          |            |
   -------------------------
              |
              v
SQLite Database + Saved ML Models

## 3. Technology Stack

Python
FastAPI
Streamlit
TensorFlow / Keras
OpenCV LBPH
Scikit-learn
SQLAlchemy and SQLite
Docker
Pytest

## 4. Computer Vision Module

### Product Image Classification

A TensorFlow/Keras convolutional neural network was trained using the Fashion-MNIST dataset.

- Training images: 55,000
- Validation images: 5,000
- Test images: 10,000
- Categories: 10 fashion-product classes
- Test accuracy: 88.53%

The trained model is stored as:

```text
app/models/product_classifier.h5

The FastAPI endpoint is:

POST /classify-product

It accepts a JPG or PNG file and returns the predicted category with a confidence score.

## Face Recognition

Customer recognition is implemented with OpenCV LBPH face recognition.

Dataset: public Olivetti Faces research dataset

Demo customers: CUST-001 and CUST-002

Images per demo customer: 5

Model file: app/models/lbph_face_recognizer.yml

Customer label mapping: app/models/face_db.pkl

The endpoint is:

POST /recognize-face

It returns a customer ID, recognition status, and match distance. Each recognition is also stored as a customer visit in SQLite.

## 5. Natural Language Processing Module

### Sentiment Analysis

The sentiment-analysis model uses:


TF-IDF Vectorizer + Logistic Regression

It predicts one of three sentiment classes:
Positive
Negative
Neutral

The model is saved as:
app/models/sentiment_model.pkl

The endpoint is:
POST /analyze-sentiment

It accepts customer review text and returns the predicted sentiment with a confidence score. Each result is logged in the review_analyses database table.

##FAQ Chatbot
The chatbot uses a hybrid design:

Rule-based matching for exact common questions

TF-IDF plus Logistic Regression intent classification as fallback

A low-confidence fallback response for unrelated questions

Supported FAQ topics include store hours, returns, order status, refunds, shipping, payments, greetings, and goodbyes.

The endpoint is:
POST /chatbot

Each chatbot request is stored in the chat_logs database table.

## 6. API, Dashboard, and Security

FastAPI provides Swagger documentation at:

http://127.0.0.1:8000/docs

Main API endpoints:

Method	Endpoint	          Purpose
POST	/classify-product	  Predict product category
POST	/recognize-face	      Recognize demo customer
POST	/analyze-sentiment	  Analyze review sentiment
POST	/chatbot	          Answer retail FAQ
GET	    /dashboard/stats      Return retail statistics
GET	    /health	              Check API health


Protected endpoints use the X-API-Key request header.

The Streamlit dashboard displays:

Total customer visits
Returning customers
Unknown visitors
Sentiment counts
Chatbot intent counts

7. Testing and Deployment

Automated tests were created using Pytest.
5 tests passed

The application is Dockerized using a Dockerfile and can be run with:

docker build -t smart-retail-ai .
docker run --rm -p 8001:8000 -p 8502:8501 smart-retail-ai

8. Ethics and Privacy

The face-recognition module uses public research images and fake customer IDs for demonstration only.

A real retail deployment must include:
Informed customer consent
Data minimization
Secure storage and access control
Biometric-data deletion policy
Bias and false-positive testing
An opt-out mechanism

9. Limitations and Future Work

Replace the small demo sentiment dataset with a large retail-review dataset.
Upgrade the product model to MobileNetV2 transfer learning.
Add live webcam recognition with WebSockets.
Deploy the Docker image to Render, Railway, AWS, or Google Cloud Run.
Add monitoring for model-confidence drift.