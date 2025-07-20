
from sqlalchemy import ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from src.config.database import Base

class AnswerDocument(Base):
    __tablename__ = "answer_document"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=func.gen_random_uuid())
    answer_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("answer.id", ondelete="CASCADE"), index=True)
    document_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("document.id", ondelete="CASCADE"), index=True)
    relevance_score: Mapped[float] = mapped_column(Float)

    answer = relationship("Answer", back_populates="documents")
    document = relationship("Document", back_populates="answer_links")