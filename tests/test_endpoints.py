from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

HEADERS = {"X-API-Key": "demo-retail-key"}


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_api_key_is_required():
    response = client.get("/dashboard/stats")

    assert response.status_code == 401


def test_sentiment_endpoint():
    response = client.post(
        "/analyze-sentiment",
        headers=HEADERS,
        json={"text": "The product quality is excellent."},
    )

    assert response.status_code == 200
    assert response.json()["sentiment"] == "positive"


def test_chatbot_endpoint():
    response = client.post(
        "/chatbot",
        headers=HEADERS,
        json={"message": "What are your store hours?"},
    )

    assert response.status_code == 200
    assert response.json()["intent"] == "store_hours"


def test_dashboard_endpoint():
    response = client.get(
        "/dashboard/stats",
        headers=HEADERS,
    )

    assert response.status_code == 200
    assert "total_visits" in response.json()