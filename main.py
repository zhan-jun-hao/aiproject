from fastapi import FastAPI

from api.chat_api import router as chat_router

# uvicorn main:app --reload
app = FastAPI(
    title="好课来 AI 客服"
)

app.include_router(chat_router)