from typing import Annotated, Any

from fastapi import Depends, HTTPException, status
from pydantic import BaseModel

from .alchemy import SQLAlchemyRepository
from .abstract import AbstractRepository
from ..database import Category as CategoryModel
from ..types import CategoryDetail

__all__ = ["Category"]


class CategoryRepository(SQLAlchemyRepository):
    model = CategoryModel
    schema = CategoryDetail
    # model = "categories"  # for raw SQL
    # pk = "id"  # for raw SQL


class CategoryManager(AbstractRepository):

    def __init__(self, repository: AbstractRepository):
        self.repository = repository

    def get(self, pk: Any) -> BaseModel:
        obj = self.repository.get(pk=pk)
        if obj is not None:
            return obj
        raise HTTPException(status_code=404, detail="category not found")

    def create(self, obj: BaseModel) -> BaseModel:
        try:
            obj = self.repository.create(obj=obj)
        except:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="category exists")
        else:
            return obj

    def update(self, pk: Any, obj: BaseModel) -> BaseModel:
        try:
            obj = self.repository.update(pk=pk, obj=obj)
        except:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid")
        else:
            return obj

    def delete(self, pk: Any) -> None:
        self.repository.delete(pk=pk)

    def all(self) -> list[BaseModel]:
        return self.repository.all()


category_repository = CategoryRepository()
category_manager = CategoryManager(repository=category_repository)
Category = Annotated[CategoryModel, Depends(dependency=lambda: category_manager)]
