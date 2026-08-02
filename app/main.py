from fastapi import Depends, FastAPI

from app.database import Base, engine
from app.routers import chatbot, dashboard, nlp, vision
from app.security import require_api_key

Base.metadata.create_all(bind=engine)

app = FastAPI()

api_key_dependency = [Depends(require_api_key)]

app.include_router(vision.router, dependencies=api_key_dependency)
app.include_router(nlp.router, dependencies=api_key_dependency)
app.include_router(chatbot.router, dependencies=api_key_dependency)
app.include_router(dashboard.router, dependencies=api_key_dependency)


@app.get("/")
def home():
    return {"message": "Smart Retail AI Platform is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}