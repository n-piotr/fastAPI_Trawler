import typing

from starlette.middleware.authentication import AuthenticationBackend, AuthCredentials, AuthenticationError
from starlette.requests import HTTPConnection

from core.repositories import user_repository
from core.settings import redis
from core.utils import verify_jwt_token


__all__ = ["JWTAuthenticationBackend", "SessionAuthenticationBackend"]


class AuthenticatedUser:

    def __init__(self, identity: str, email: str) -> None:
        self.is_authenticated = True
        self.identity = identity
        self.display_name = email


class JWTAuthenticationBackend(AuthenticationBackend):  # API auth

    async def authenticate(
        self, conn: HTTPConnection
    ) -> typing.Optional[typing.Tuple["AuthCredentials", "AuthenticatedUser"]]:
        # print(conn.headers)  # TEMP debug
        if "Authorization" not in conn.headers:
            return

        token = conn.headers.get("Authorization")
        try:
            user_id = verify_jwt_token(jwt_token=token)
        except ValueError as e:
            return
        else:
            user = user_repository.get(pk=user_id)
            if user is None:
                return
            return AuthCredentials(["authenticated"]), AuthenticatedUser(identity=user_id, email=user.email)


class SessionAuthenticationBackend(AuthenticationBackend):  # Web app auth

    async def authenticate(
        self, conn: HTTPConnection
    ) -> typing.Optional[typing.Tuple["AuthCredentials", "AuthenticatedUser"]]:
        if "session" not in conn.cookies:
            return

        token = conn.cookies.get("session")
        user_id = await redis.get(name=token)
        if user_id is None:
            return
        user = user_repository.get(pk=user_id.decode())
        if user is None:
            return
        return AuthCredentials(["authenticated"]), AuthenticatedUser(identity=user_id, email=user.email)
