# AI-Powered Smart Retail & Customer Intelligence Platform

A full-stack retail AI project that combines product image classification, customer face recognition, review sentiment analysis, an FAQ chatbot, and a dashboard.

## Features

- Product category classification using a MobileNetV2 transfer-learning model
- Customer face recognition using OpenCV LBPH
- Customer visit logging with SQLite
- Sentiment analysis for customer reviews
- Hybrid FAQ chatbot: rule matching plus ML intent classification
- FastAPI backend with Swagger API documentation
- Streamlit frontend dashboard
- API-key endpoint protection
- Docker deployment support
- Automated endpoint tests

## Tech Stack

- Python
- FastAPI
- Streamlit
- TensorFlow / Keras
- OpenCV
- Scikit-learn
- SQLAlchemy / SQLite
- Docker

## Project Structure

```text
smart-retail-ai/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── security.py
│   ├── models/
│   ├── routers/
│   └── services/
├── data/
├── notebooks/
├── tests/
├── frontend.py
├── Dockerfile
├── requirements.txt
└── README.md