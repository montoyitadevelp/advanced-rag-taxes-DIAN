import datetime
from sqlalchemy import Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from src.config.database import Base

class Answer(Base):
    __tablename__ = "answer"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=func.gen_random_uuid())
    question_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("question.id", ondelete="CASCADE"), index=True)
    answer_text: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow)
    
    question = relationship("Question", back_populates="answers")
    documents = relationship("AnswerDocument", back_populates="answer", cascade="all, delete-orphan")