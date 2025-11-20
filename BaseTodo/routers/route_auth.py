from fastapi import APIRouter, HTTPException
from fastapi import Response, Request
from fastapi.encoders import jsonable_encoder
from schemas import UserBody, SuccessMsg, UserInfo
from database import db_signup, db_login
from starlette.status import HTTP_201_CREATED
from auth_utils import AuthJwtCsrf

router = APIRouter(
    prefix="/api",
    tags=["auth"],
    responses={404: {"description": "認証エラー"}},
)

auth = AuthJwtCsrf()

@router.post("/register", response_model=UserInfo, status_code=HTTP_201_CREATED)
async def signup_user(user: UserBody):
    user = jsonable_encoder(user)
    new_user = await db_signup(user)
    return new_user

@router.post("/login", response_model=SuccessMsg)
async def login_user(response: Response, user: UserBody):
    user = jsonable_encoder(user)
    token = await db_login(user)
   
    response.set_cookie(
        key="access_token",
        value=f"Bearer {token}",
        httponly=True,
        samesite="none",
        secure=True
    )
    
    return SuccessMsg(message="ログインに成功しました。")