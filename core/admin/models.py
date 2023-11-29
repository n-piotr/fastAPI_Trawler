# https://aminalaee.dev/sqladmin/ - docs
from sqladmin import ModelView

from ..database import Post, Category


__all__ = [
    "PostAdmin",
    "CategoryAdmin"
]


class PostAdmin(ModelView, model=Post):
    name_plural = "посты"
    column_list = ["title", "date_created"]


class CategoryAdmin(ModelView, model=Category):
    name_plural = "категории"
    column_list = ["name"]


