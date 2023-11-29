from typing import Any, Type

from pydantic import BaseModel
from sqlalchemy import select

from .abstract import AbstractRepository
from ..database import Base, session

__all__ = [
    "SQLAlchemyRepository"
]


class SQLAlchemyRepository(AbstractRepository):
    model: Type[Base]
    schema: Type[BaseModel]

    def __init__(self):
        self.session = session

    def get(self, pk: Any) -> BaseModel:
        with self.session() as session:
            obj = session.get(self.model, pk)
            if obj is not None:
                return self.schema.model_validate(obj=obj, from_attributes=True)

    def create(self, obj: BaseModel) -> BaseModel:
        obj = self.model(**obj.model_dump())
        with self.session() as session:
            session.add(obj)
            session.commit()
            return self.schema.model_validate(obj=obj, from_attributes=True)

    def update(self, pk: Any, obj: BaseModel) -> BaseModel:
        with self.session() as session:
            _obj = session.get(self.model, pk)
            if _obj is not None:
                for k, v in obj.model_dump():
                    setattr(_obj, k, v)
                    session.commit()
                    return obj

    def delete(self, pk: Any) -> None:
        with self.session() as session:
            obj = session.get(self.model, pk)
            session.delete(obj)
            session.commit()

    def all(self) -> list[BaseModel]:
        with self.session() as session:
            objs = session.scalars(select(self.model)).all()
            return [self.schema.model_validate(obj=obj, from_attributes=True) for obj in objs]
