import pickle
from sqlalchemy.ext.asyncio import AsyncSession
from src.question.models import Question


class QuestionManager:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_question(self, payload: dict, embedding: list[float]) -> Question:
        """
        Create a new question in the database.
        
        :param payload: The request payload containing the question text.
        :param embedding: The embedding vector for the question.
        :return: The created Question object.
        """
        try:
            question = await self._create({
                "question": payload.question,
                "embedding": embedding
            })
            return question
        except ValueError as e:
            raise ValueError({
                "error": "Error creating question",
                "details": str(e),
                "method": "QuestionManager.create_question"
            })
        
    
    async def _create(self, payload: dict, is_flush=False) -> Question:
        """
        Internal method to create a question in the database.
        :param payload: The payload containing the question text and embedding.
        :param is_flush: Whether to flush the session after adding the question.
        :return: The created Question object.
        """
        try:
            question = Question(
                question_text=payload["question"],
                embedding=pickle.dumps(payload["embedding"])
            )
            self.db.add(question)
            if is_flush:
                await self.db.flush()
            else:
                await self.db.commit()
            await self.db.refresh(question)
            return question
        except Exception as e:
            raise ValueError({
                "error": "Error creating question",
                "details": str(e),
                "method": "QuestionManager._create_question"
            })
