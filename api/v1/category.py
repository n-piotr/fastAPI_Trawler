from fastapi import APIRouter, Path, HTTPException
from starlette import status

from core.repositories import Category
from core.types import CategoryDetail

router = APIRouter()


@router.get(
    path="/category",
    response_model=list[CategoryDetail],
    summary="Список категорий",
    tags=["Категория"]
)
async def all_categories(repository: Category):
    return repository.all()


@router.get(
    path="/category/{pk}",
    response_model=CategoryDetail,
    status_code=status.HTTP_200_OK,
    summary="Получение категории",
    description="""
    **Получение категории по ID**
    """,
    tags=["Категория"]
)
async def get_category(repository: Category, pk: int = Path(ge=1, title="Category ID", example=42)):
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
    return repository.get(pk=pk)
