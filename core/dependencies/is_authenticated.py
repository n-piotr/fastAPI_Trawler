from typing import NoReturn

from fastapi import HTTPException, status, Depends
from fastapi.requests import Request


async def _is_authenticated(request: Request) -> NoReturn:
    if not request.user.is_authenticated:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


IsAuthenticated = Depends(dependency=_is_authenticated)