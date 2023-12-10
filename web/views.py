from fastapi import APIRouter, Form
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


@router.get(
    path="/contact",
    response_class=HTMLResponse,
    name="trawler_contact"
)
async def contact(request: Request):
    return templating.TemplateResponse(
        name="trawler/contact.html",
        context={
            "request": request
        }
    )


@router.post(
    path="/contact",
    response_class=HTMLResponse,
    name="trawler_contact"
)
async def _contact(
        request: Request,
        name: str = Form(),
        email: str = Form(),
        message: str = Form()
):
    # actions TODO with data from html contact from
    print(name)
    print(email)
    print(message)
    return await contact(request=request)
