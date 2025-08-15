import datetime
from sqlalchemy import Text
from sqlalchemy.dialects.postgresql import UUID, ARRAY, FLOAT
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from src.config.database import Base

class Question(Base):
    __tablename__ = "question"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=func.gen_random_uuid())
    question_text: Mapped[str] = mapped_column(Text)
    embedding: Mapped[list[float]] = mapped_column(ARRAY(FLOAT))
    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow)

    answers = relationship("Answer", back_populates="question", cascade="all, delete-orphan")