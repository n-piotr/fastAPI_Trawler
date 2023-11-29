from fastapi import APIRouter
from .v1 import router as v1_router

__all__ = ["router"]

router = APIRouter(
    prefix="/api"
)
router.include_router(router=v1_router)
