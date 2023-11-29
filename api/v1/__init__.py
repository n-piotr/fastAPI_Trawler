from fastapi import APIRouter

from .category import router as category_router

__all__ = ["router"]

router = APIRouter(
    prefix="/v1"
)
router.include_router(router=category_router)
