from .base import Schema


__all__ = ["TokenDetail"]


class TokenDetail(Schema):
    token: str
    expire: int = 300
