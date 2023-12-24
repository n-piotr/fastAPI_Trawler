# https://aminalaee.dev/sqladmin/ - docs
from sqladmin import ModelView

from ..database import Post, Category, User, Message


__all__ = [
    "PostAdmin",
    "CategoryAdmin",
    "UserAdmin",
    "MessageAdmin"
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


class MessageAdmin(ModelView, model=Message):
    name_plural = "сообщения"
    column_list = ["tg_chat_username", "tg_message_id", "user_id"]



