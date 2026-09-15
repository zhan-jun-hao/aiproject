from pydantic import BaseModel, Field

from schema.agent_output_schema import (
    OrderCard,
    CourseCard
)


class ChatResult(BaseModel):

    code: int

    conversation_id: str

    message: str

    order: OrderCard | None = None

    course: CourseCard | None = None

    suggestions: list[str] = Field(
        default_factory=list
    )

class ChatRequest(BaseModel):
    message: str
    conversation_id: str | None = None