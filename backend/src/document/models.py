import datetime
from sqlalchemy import String, Text
from sqlalchemy.dialects.postgresql import UUID, ARRAY, FLOAT
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from src.config.database import Base


class Document(Base):
    __tablename__ = "document"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=func.gen_random_uuid())
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(Text)
    embedding: Mapped[list[float]] = mapped_column(ARRAY(FLOAT))
    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow)


    answer_links = relationship("AnswerDocument", back_populates="document", cascade="all, delete-orphan") 