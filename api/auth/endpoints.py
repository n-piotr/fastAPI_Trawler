from fastapi import APIRouter, status, HTTPException, Path
from sqlalchemy.exc import IntegrityError

from core.types import UserDetail, UserRegisterForm, UserLoginForm, TokenDetail
from core.repositories import user_repository
from core.utils import create_jwt_token, create_user_verify_url, get_from_redis, delete_from_redis
from core.tasks import send_email


__all__ = ["router"]


router = APIRouter()


@router.post(
    path="/register",
    response_model=UserDetail,
    response_model_exclude={"password"},
    status_code=status.HTTP_201_CREATED
)
async def sing_up(data: UserRegisterForm):
    user = UserDetail.create(data=data)
    try:
        user = user_repository.create(obj=user, exclude={"date_register"})
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email is exist")
    else:
        verify_url = await create_user_verify_url(user_id=user.id)
        send_email.delay(email=user.email, url=verify_url)
        return user


@router.post(
    path="/login",
    response_model=TokenDetail,
    status_code=status.HTTP_202_ACCEPTED
)
async def sing_in(data: UserLoginForm):
    user = user_repository.get_by_email(email=data.email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user not found")

    # if not user.is_active:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not active")

    if not data.validate_password(hash_password=user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="password invalid")

    jwt_token = create_jwt_token(user_id=user.id)
    return TokenDetail(token=jwt_token)


@router.get(
    path="/verify/{code}"
)
async def verify_email(code: str = Path()):
    user_id = await get_from_redis(name=code)
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    await delete_from_redis(code)
    user_repository.activate(pk=user_id.decode())
    return {"status": "OK"}
