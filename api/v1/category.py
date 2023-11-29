from fastapi import APIRouter, Path, HTTPException
from starlette import status

from fastapi_cache.decorator import cache

from core.repositories import Category
from core.types import CategoryDetail

from core.tasks import ping  # Celery test

router = APIRouter()


@router.get(
    path="/categories",
    response_model=list[CategoryDetail],
    summary="Список категорий",
    tags=["Категория"]
)
@cache(expire=60)
async def all_categories(manager: Category):
    ping.delay()  # Celery test
    print(ping.delay())  # Celery task id

    return manager.all()


@router.get(
    path="/categories/{pk}",
    response_model=CategoryDetail,
    # dependencies=[IsAuthenticated],
    status_code=status.HTTP_200_OK,
    summary="Получение категории",
    description="""
    **Получение категории по ID**
    """,
    tags=["Категория"]
)
@cache(expire=60)
async def get(manager: Category, pk: int = Path(ge=1, title="Category ID", example=42)):
    """Ссылка для получения категории по ID

    Args:
    ----
        pk: ID категории

    Returns:
    -------
        Объект категории

    Raises:
    ------
        HTTPException 404 Если категория не найдена
    """
    return manager.get(pk=pk)


async def update(manager: Category, pk: int = Path(ge=1, example=42)):
    pass


async def delete(manager: Category, pk: int = Path(ge=1, example=42)):
    return manager.delete(pk=pk)
