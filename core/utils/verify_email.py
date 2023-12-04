from uuid import uuid4

from core.settings import redis


__all__ = [
    "save_to_redis",
    "get_from_redis",
    "create_user_verify_url",
    "delete_from_redis",
]


async def save_to_redis(name: str, value: str):
    await redis.set(
        name=name,
        value=value,
        ex=300
    )


async def get_from_redis(name: str) -> str:
    return await redis.get(name=name)


async def delete_from_redis(name: str) -> None:
    await redis.delete(name)


# link to send by e-mail
async def create_user_verify_url(user_id: str) -> str:
    code = str(uuid4())
    await save_to_redis(name=code, value=user_id)
    return f"http://127.0.0.1:8000/api/verify/{code}"
