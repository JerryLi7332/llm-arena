from fastapi import APIRouter

from .ai_codes import ai_codes_router

games_router = APIRouter()

games_router.include_router(ai_codes_router, prefix="/ai-codes", tags=["游戏模块"])

__all__ = ["games_router"]
