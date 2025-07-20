from uuid import UUID
from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)


class QuestionReadSchema(BaseModel):
    id: UUID
    question_text: str

    class Config:
        from_attributes = True