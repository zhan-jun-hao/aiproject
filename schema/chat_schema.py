from pydantic import BaseModel

class ChatResult(BaseModel):
    message: str
    code: int
    conversation_id: str

class ChatRequest(BaseModel):
    message: str
    conversation_id: str | None = None