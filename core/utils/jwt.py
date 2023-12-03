from datetime import datetime, timedelta

from jose import jwt, JWTError

from core.settings import settings

__all__ = [
    "create_jwt_token",
    "verify_jwt_token"
]


def create_jwt_token(user_id: str) -> str:
    return jwt.encode(
        claims={
            "sub": user_id,
            "exp": datetime.utcnow() + timedelta(seconds=settings.EXP_JWT)
        },
        key=settings.SECRET_KEY.get_secret_value()
    )


def verify_jwt_token(jwt_token: str) -> str:
    try:
        claims = jwt.decode(
            token=jwt_token,
            key=settings.SECRET_KEY.get_secret_value(),
            algorithms=jwt.ALGORITHMS.HS256
        )
    except JWTError:
        raise ValueError("Invalid JWT token or expired")
    else:
        return claims.get("sub")
