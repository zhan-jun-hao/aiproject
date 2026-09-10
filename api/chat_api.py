import uuid

from fastapi import APIRouter, Header

from schema.chat_schema import ChatRequest, ChatResult
from service.chat_service import chat


router = APIRouter(
    prefix="/api/chat",
    tags=["AI客服"]
)

@router.post("", response_model=ChatResult)
async def chat_api(request: ChatRequest):

    conversation_id = request.conversation_id
    if conversation_id is None:
        conversation_id = str(uuid.uuid4())

    result = await chat(
        message=request.message,
        conversation_id=conversation_id,
    )

    return ChatResult(
        message=result,
        code=200,
        conversation_id=conversation_id
    )