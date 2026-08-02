from fastapi import APIRouter
from sqlalchemy import func

from app.database import ChatLog, CustomerVisit, ReviewAnalysis, SessionLocal

router = APIRouter()


@router.get("/dashboard/stats")
def get_dashboard_stats():
    database = SessionLocal()

    try:
        total_visits = database.query(func.count(CustomerVisit.id)).scalar() or 0

        returning_customers = (
            database.query(func.count(CustomerVisit.id))
            .filter(CustomerVisit.status == "returning_customer")
            .scalar()
            or 0
        )

        unknown_visits = (
            database.query(func.count(CustomerVisit.id))
            .filter(CustomerVisit.status == "unknown")
            .scalar()
            or 0
        )

        sentiment_rows = (
            database.query(
                ReviewAnalysis.sentiment,
                func.count(ReviewAnalysis.id),
            )
            .group_by(ReviewAnalysis.sentiment)
            .all()
        )

        chat_rows = (
            database.query(
                ChatLog.intent,
                func.count(ChatLog.id),
            )
            .group_by(ChatLog.intent)
            .all()
        )

        return {
            "total_visits": total_visits,
            "returning_customers": returning_customers,
            "unknown_visits": unknown_visits,
            "sentiment_counts": dict(sentiment_rows),
            "chats_by_intent": dict(chat_rows),
        }
    finally:
        database.close()