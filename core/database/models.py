from sqlalchemy import (
    Column,
    SMALLINT,
    VARCHAR,
    CheckConstraint,
    INT,
    ForeignKey,
    TIMESTAMP,
    CHAR,
    BOOLEAN
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from ulid import parse

from .base import Base

__all__ = [
    "Base",
    "Category",
    "Post",
    "User",
    "Message"
]


class Category(Base):
    __tablename__ = "categories"
    __table_args__ = (
        CheckConstraint("length(name) >= 2"),
        CheckConstraint("length(slug) >= 2"),
        CheckConstraint("slug not like '% %'")
    )
    id = Column(SMALLINT, primary_key=True)
    name = Column(VARCHAR(32), nullable=False, unique=True)
    slug = Column(VARCHAR(32), nullable=False, unique=True)

    posts = relationship(argument="Post", back_populates="category")
    # argument="Post" - Post model is the target of relationship
    # back_populates="category" - attribute 'category' will be added to instances of Post model that points
    # back to the Category instance that the post belongs to.

    def __str__(self):
        return self.name


class Post(Base):
    __tablename__ = "posts"
    __table_args__ = (
        CheckConstraint("length(title) >= 2"),
        CheckConstraint("length(body) >= 50"),
    )

    id = Column(INT, primary_key=True)
    title = Column(VARCHAR(256), nullable=False)
    body = Column(VARCHAR(3000), nullable=False)
    tg_link = Column(VARCHAR(256), nullable=True)  # TODO switch to nullable=False after migration and filling
    date_created = Column(TIMESTAMP, nullable=False)
    category_id = Column(
        SMALLINT,
        ForeignKey("categories.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False
    )

    category = relationship(argument="Category", back_populates="posts")

    def __str__(self):
        return self.title


class User(Base):
    __tablename__ = "users"

    id = Column(CHAR(26), primary_key=True)  # ULID
    email = Column(VARCHAR(128), nullable=False, unique=True)
    password = Column(CHAR(60), nullable=False)  # hash
    is_active = Column(BOOLEAN, default=False)
    is_staff = Column(BOOLEAN, default=False)
    settings = Column(JSONB,
                      default={"tg_groups": "telegram_groups", "filter_in": "python", "filter_out": "snake", "depth": 1}
                      )
    messages = relationship(argument="Message", back_populates="user")

    @property
    def date_register(self):
        return parse(self.id).timestamp().datetime

    def __str__(self):
        return self.email


class Message(Base):  # Saved messages by User
    __tablename__ = "messages"

    id = Column(INT, primary_key=True)
    tg_chat_username = Column(VARCHAR(256), nullable=True)  # TODO update after creation in db
    tg_message_id = Column(INT, nullable=True)  # TODO update after creation in db
    user_id = Column(
        CHAR(26),
        ForeignKey("users.id", ondelete="RESTRICT", onupdate="CASCADE"),
        # nullable=False  # TODO maybe uncomment later if works
    )

    user = relationship(argument="User", back_populates="messages")

    def __str__(self):
        return f"https://t.me/{self.tg_chat_username}/{self.tg_message_id}"
