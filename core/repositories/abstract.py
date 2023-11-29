from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel


class AbstractRepository(ABC):

    @abstractmethod
    def get(self, pk: Any) -> BaseModel:
        raise NotImplementedError

    @abstractmethod
    def create(self, obj: BaseModel) -> BaseModel:
        raise NotImplementedError

    @abstractmethod
    def update(self, pk: Any, obj: BaseModel) -> BaseModel:
        raise NotImplementedError

    @abstractmethod
    def delete(self, pk: Any) -> None:
        raise NotImplementedError

    @abstractmethod
    def all(self) -> list[BaseModel]:
        raise NotImplementedError
