from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.database import ChatLog, SessionLocal
from app.services.chatbot_service import get_chatbot_response, load_chatbot

router = APIRouter()

chatbot_model, responses_by_tag, patterns_by_tag = load_chatbot()


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=1000)


@router.post("/chatbot")
def chat_with_bot(request: ChatRequest):
    result = get_chatbot_response(
        request.message,
        chatbot_model,
        responses_by_tag,
        patterns_by_tag,
    )

    database = SessionLocal()

    try:
        database.add(
            ChatLog(
                intent=result["intent"],
                confidence=result["confidence"],
            )
        )
        database.commit()
    finally:
        database.close()

    return result