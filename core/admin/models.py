# https://aminalaee.dev/sqladmin/ - docs
from sqladmin import ModelView

from ..database import Post, Category, User


__all__ = [
    "PostAdmin",
    "CategoryAdmin",
    "UserAdmin"
]


class PostAdmin(ModelView, model=Post):
    name_plural = "посты"
    column_list = ["title", "date_created"]


class CategoryAdmin(ModelView, model=Category):
    name_plural = "категории"
    column_list = ["name"]


class UserAdmin(ModelView, model=User):
    name_plural = "пользователи"
    column_list = ["id", "email"]



