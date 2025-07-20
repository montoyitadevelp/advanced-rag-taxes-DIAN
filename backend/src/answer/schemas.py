from uuid import UUID
from pydantic import BaseModel
from typing import List


class AnswerResponse(BaseModel):
    answer: str
    sources: List[str]


class AnswerReadSchema(BaseModel):
    id: UUID
    answer_text: str
    question_id: UUID

    class Config:
        from_attributes = True


