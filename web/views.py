from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.requests import Request

from core.settings import templating
from core.database import session, Post

router = APIRouter()


@router.get(
    path="/",
    response_class=HTMLResponse,
    name="trawler_index"
)
async def index(request: Request):
    with session() as s:
        objs = s.query(Post).all()
    return templating.TemplateResponse(
        name="trawler/index.html",
        context={
            "request": request,
            "posts": objs
        }
    )

