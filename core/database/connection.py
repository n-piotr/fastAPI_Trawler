from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.settings import settings

__all__ = [
    "engine",
    "session"
]


engine = create_engine(url=settings.DATABASE_URL.unicode_string())
session = sessionmaker(bind=engine)
