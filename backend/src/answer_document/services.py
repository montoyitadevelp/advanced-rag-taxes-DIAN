from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.answer_document.models import AnswerDocument
from src.document.models import Document

class AnswerDocumentManager:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def post_link_documents_to_answer(self, answer_id: UUID, top_docs: list[tuple[float, Document]]):
        """
        Create and link documents to an answer with relevance scores.
        :param answer_id: UUID of the answer.
        :param top_docs: List of (score, Document) tuples.
        """
        try:
            for score, doc in top_docs:
                await self._create({
                    "answer_id": answer_id,
                    "document_id": doc.id,
                    "relevance_score": score
                })
        except Exception as e:
            raise ValueError({
                "error": "Error linking documents to answer",
                "details": str(e),
                "method": "AnswerDocumentManager.post_link_documents_to_answer"
            })

    async def _create(self, payload: dict, is_flush: bool = False) -> AnswerDocument:
        """
        Internal method to create an AnswerDocument.
        :param payload: Dict with answer_id, document_id, relevance_score.
        :param is_flush: If True, flush instead of commit.
        :return: Created AnswerDocument.
        """
        try:
            answer_doc = AnswerDocument(**payload)
            self.db.add(answer_doc)
            if is_flush:
                await self.db.flush()
            else:
                await self.db.commit()
            await self.db.refresh(answer_doc)
            return answer_doc
        except Exception as e:
            raise ValueError({
                "error": "Error creating answer document",
                "details": str(e),
                "method": "AnswerDocumentManager._create_answer_document"
            })