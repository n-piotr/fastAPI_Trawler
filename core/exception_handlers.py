from http.client import HTTPException

from starlette.requests import Request
from starlette.responses import RedirectResponse


async def not_authenticated(request: Request, exc: HTTPException):
    """ to handle unauthenticated access on web app
    exception_handlers=... in app.py
    dependencies=[IsAuthenticated] in web/views.py
    """
    return RedirectResponse(url="/login")
