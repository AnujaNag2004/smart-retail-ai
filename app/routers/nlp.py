from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.database import ReviewAnalysis, SessionLocal
from app.services.nlp_service import analyze_sentiment, load_sentiment_model

router = APIRouter()

sentiment_model = load_sentiment_model()


class SentimentRequest(BaseModel):
    text: str = Field(min_length=1, max_length=2000)


@router.post("/analyze-sentiment")
def analyze_review(request: SentimentRequest):
    result = analyze_sentiment(request.text, sentiment_model)

    database = SessionLocal()

    try:
        database.add(
            ReviewAnalysis(
                sentiment=result["sentiment"],
                confidence=result["confidence"],
            )
        )
        database.commit()
    finally:
        database.close()

    return result