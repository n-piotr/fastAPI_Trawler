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
from sqlalchemy.orm import relationship
from ulid import parse

from .base import Base

__all__ = [
    "Base",
    "Category",
    "Post",
    "User"
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

    @property
    def date_register(self):
        return parse(self.id).timestamp().datetime

    def __str__(self):
        return self.email
