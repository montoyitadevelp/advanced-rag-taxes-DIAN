from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from src.config.database import get_db
from src.question.schemas import QuestionRequest
from src.answer.schemas import AnswerResponse
from src.utils.rag.rag_manager import RagManager

router = APIRouter(prefix="/answer", tags=["Answer"])

@router.post(
   "/create", 
   status_code=status.HTTP_201_CREATED, 
   response_model=AnswerResponse
)
async def generate_answer(
    payload: QuestionRequest = Body(),
    db: AsyncSession = Depends(get_db)
):
    try:
        return await RagManager(db).process_question(payload)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Failed to generate answer",
                "details": str(e),
                "method": "generate_answer"
            }
        )
