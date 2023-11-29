from typing import Optional
from datetime import datetime

from pydantic import Field, PositiveInt

from .base import Schema

__all__ = [
    "PostCreate",
    "PostEdit",
    "PostDetail"
]


class PostCreate(Schema):
    title: str = Field(
        default=...,
        title="Post Title",
        min_length=2,
        max_length=128,
        examples=["Python Intern-developer"]
    )
    body: str = Field(
        default=...,
        min_length=50,
        max_length=500,
        title="Post Body",
        examples=["We have cookies..."]
    )
    salary: Optional[str] = Field(
        default=None,
        max_length=16,
        title="Salary",
        examples=["420 $"]
    )
    date_created: datetime = Field(
        default_factory=datetime.utcnow
    )


class PostEdit(PostCreate):
    ...


class PostDetail(PostCreate):
    id: PositiveInt = Field(
        default=...,
        title="Post ID",
        examples=[42]
    )
