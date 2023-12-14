from fastapi import HTTPException
from fastapi.requests import Request

from core.database import session, User
from core.settings import redis

__all__ = ["get_auth_user"]


async def get_auth_user(request: Request):
    """ Get currently authenticated user from database """

    # Get session ID from cookies
    session_id = request.cookies.get("session")
    if not session_id:
        raise HTTPException(status_code=400, detail="Session not found")

    # Get user ID from Redis
    user_id = await redis.get(session_id)
    if not user_id:
        raise HTTPException(status_code=400, detail="User not found")

    with session() as s:
        user = s.query(User).filter_by(id=user_id.decode()).first()  # .first(), .all() or .one() methods

    return user
