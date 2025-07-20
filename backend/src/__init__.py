from fastapi import APIRouter
from src.answer import routers as answer_routers

main_router = APIRouter(prefix="/api/v1")
main_router.include_router(answer_routers.router)

