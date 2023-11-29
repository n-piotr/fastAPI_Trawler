# from typing import Any, Type
#
# from psycopg2.extras import NamedTupleConnection
# from pydantic import BaseModel
#
# from core.repositories.abstract import AbstractRepository
# from settings import settings
#
# conn = NamedTupleConnection(dsn=settings.DATABASE_URL.unicode_string())
#
#
# class SQLRepository(AbstractRepository):
#
#     model: str
#     schema: Type[BaseModel]
#     pk: str
#
#     def __init__(self):
#         self.session = conn
#
#     def get(self, pk: Any) -> BaseModel:
#         with self.session.cursor() as cur:
#             cur.execute(f"SELECT * FROM {self.model} WHERE {self.pk} = %s;", (pk, ))
#             obj = cur.fetchone()
#             if obj:
#                 return self.schema.model_validate(obj=obj, from_attributes=True)
#
#     def create(self, obj: BaseModel) -> BaseModel:
#         pass
#
#     def update(self, pk: Any, obj: BaseModel) -> BaseModel:
#         pass
#
#     def delete(self, pk: Any) -> None:
#         pass
#
#     def close(self):
#         self.session.close()
