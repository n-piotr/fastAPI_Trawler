from uuid import uuid4

from fastapi import APIRouter, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from pyrogram import Client
from sqlalchemy.exc import IntegrityError
from starlette import status
from starlette.responses import RedirectResponse

from core.repositories import user_repository
from core.settings import templating, redis
from core.settings import settings
from core.database import session, Post, User
from core.types import UserDetail, UserRegisterForm, UserLoginForm
from core.utils import create_user_verify_url, get_auth_user
from core.tasks import send_email
from core.dependencies import IsAuthenticated
from . import get_tg_messages

router = APIRouter()


@router.get(
    path="/",
    response_class=HTMLResponse,
    name="trawler_index"
)
async def index(request: Request):
    # print(request.user.identity)  # core.middleware.auth.AuthenticatedUser object
    # b'01HHHSW8XQY9F3T0KBN9X3C3XJ'
    # NotImplementedError - if user is not authenticated

    # with session() as s:
    #     objs = s.query(Post).all()

    tg_messages = await get_tg_messages(request=request)

    return templating.TemplateResponse(
        name="trawler/index.html",
        context={
            "request": request,
            "tg_messages": tg_messages,
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


# TODO redirect to index after successful login
@router.get(
    path="/login",
    response_class=HTMLResponse,
    name="login"
)
async def login(request: Request):
    return templating.TemplateResponse(
        name="trawler/sign-in.html",
        context={
            "request": request
        }
    )


@router.post(
    path="/login",
    response_class=HTMLResponse,
    name="login"
)
async def _login(request: Request, data: UserLoginForm = Depends(dependency=UserLoginForm.as_form)):
    user = user_repository.get_by_email(email=data.email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user not found")

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not active")

    if not data.validate_password(hash_password=user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="password invalid")

    # SESSION AUTHORIZATION:
    response = await login(request=request)  # get TemplateResponse
    session_id = str(uuid4())
    await redis.set(
        name=session_id,
        value=user.id,
        ex=24*60*60
    )  # put into redis for 24h
    response.set_cookie(
        key="session",
        value=session_id
    )
    return response


@router.get(
    path="/logout",
    response_class=RedirectResponse,
    name="logout"
)
async def logout(request: Request):
    response = RedirectResponse(url="/login")
    response.delete_cookie(key="session")
    await redis.delete(request.cookies.get("session"))
    return response


@router.get(
    path="/register",
    response_class=HTMLResponse,
    name="register"
)
async def register(request: Request):
    return templating.TemplateResponse(
        name="trawler/sign-up.html",  # TODO one name (register/sign-up/trawler_register)
        context={
            "request": request
        }
    )


@router.post(
    path="/register",
    response_class=HTMLResponse,
    name="register"
)
async def _register(request: Request, data: UserRegisterForm = Depends(dependency=UserRegisterForm.as_form)):
    user = UserDetail.create(data=data)  # extracts email and pass from data, hashes pass
    try:
        user = user_repository.create(obj=user, exclude={"date_register"})
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email is exist")
    else:
        verify_url = await create_user_verify_url(user_id=user.id)
        send_email.delay(email=user.email, url=verify_url)  # TODO ..8000/api/verify/.. to ..8000/verify.. "OK" template
    return await register(request=request)


@router.get(
    path="/settings",
    response_class=HTMLResponse,
    name="settings",
    dependencies=[IsAuthenticated]  # TODO add to Admin
)
async def user_settings(request: Request):

    user = await get_auth_user(request=request)  # TEMP, can get user from request:
    # print(request.user.identity)

    return templating.TemplateResponse(
        name="trawler/settings.html",
        context={
            "request": request,
            "user": user
        }
    )


@router.post(
    path="/settings",
    response_class=HTMLResponse,
    name="settings"
)
async def _user_settings(
        request: Request,
        tg_groups: str = Form(),
        filter_in: str = Form(),
        filter_out: str = Form(),
        depth: int = Form()
):
    # user = await get_auth_user(request=request)

    user_id = request.user.identity

    with session() as s:
        user = s.query(User).filter_by(id=user_id.decode()).first()
        # print(user.settings)
        # The JSON type, when used with the SQLAlchemy ORM, does not detect in-place mutations to the structure

        new_settings = user.settings.copy()  # create a copy of the settings
        new_settings['tg_groups'] = tg_groups  # update the copy
        new_settings['filter_in'] = filter_in
        new_settings['filter_out'] = filter_out
        new_settings['depth'] = depth
        # print(new_settings)
        user.settings = new_settings  # assign the updated copy back to user.settings
        # print(user.settings)
        s.commit()

    return await user_settings(request=request)
