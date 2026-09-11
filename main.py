from fastapi import FastAPI

from api.chat_api import router as chat_router
from middleware.user_context_filter import UserContextMiddleware

# uvicorn main:app --reload
app = FastAPI(
    title="好课来 AI 客服"
)

app.add_middleware(
    UserContextMiddleware,
    internal_secret="zhanjunhao",
    require_internal_secret=True,
    ignored_paths=[
            "/docs",
            "/openapi.json",
            "/favicon.ico",
            "/redoc"
        ]
)

app.include_router(chat_router)