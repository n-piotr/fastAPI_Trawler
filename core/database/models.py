from sqlalchemy import (
    Column,
    SMALLINT,
    VARCHAR,
    CheckConstraint,
    INT,
    ForeignKey,
    TIMESTAMP
)
from sqlalchemy.orm import relationship

from .base import Base

__all__ = [
    "Base",
    "Category",
    "Post"
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
    title = Column(VARCHAR(128), nullable=False)
    body = Column(VARCHAR(500), nullable=False)
    salary = Column(VARCHAR(128), nullable=True)
    category_id = Column(
        SMALLINT,
        ForeignKey("categories.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False
    )
    date_created = Column(TIMESTAMP, nullable=False)

    category = relationship(argument="Category", back_populates="posts")

    def __str__(self):
        return self.title
