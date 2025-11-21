from fastapi import APIRouter, Depends
from fastapi import Response, Request
from fastapi.encoders import jsonable_encoder
from schemas import UserBody, SuccessMsg, UserInfo, Csrf
from database import db_signup, db_login
from starlette.status import HTTP_201_CREATED
from auth_utils import AuthJwtCsrf
from fastapi_csrf_protect import CsrfProtect

router = APIRouter(
    prefix="/api",
    tags=["auth"],
    responses={404: {"description": "認証エラー"}},
)

auth = AuthJwtCsrf()

@router.get("/csrf-token", response_model=Csrf)
async def get_csrf_token(csrf_protect: CsrfProtect = Depends()):
    csrf_token = csrf_protect.generate_csrf()
    response = {"csrf_token": csrf_token}
    return response

@router.post("/register", response_model=UserInfo)
async def signup_user(request: Request, user: UserBody, csrf_protect: CsrfProtect = Depends()):
    csrf_token = csrf_protect.get_csrf_from_headers(request.headers)
    csrf_protect.validate_csrf(csrf_token)
    user = jsonable_encoder(user)
    new_user = await db_signup(user)
    return new_user

@router.post("/login", response_model=SuccessMsg)
async def login_user(request:Request, response: Response, user: UserBody, csrf_protect: CsrfProtect = Depends()):
    csrf_token = csrf_protect.get_csrf_from_headers(request.headers)
    csrf_protect.validate_csrf(csrf_token)
    
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

@router.post("/logout", response_model=SuccessMsg)
async def logout_user(response: Response, request: Request, csrf_protect: CsrfProtect = Depends()):
    csrf_token = csrf_protect.get_csrf_from_headers(request.headers)
    csrf_protect.validate_csrf(csrf_token)
    response.set_cookie(
        key="access_token", 
        value="", 
        httponly=True,  
        samesite="none",
        secure=True,
        max_age=0
    )
    
    return SuccessMsg(message="ログアウトに成功しました。")

@router.get("/user", response_model=UserInfo)
def get_user_refresh_jwt(request: Request, response: Response):
    new_token, subject = auth.verify_update_jwt(request)
    
    response.set_cookie(
        key="access_token",
        value=f"Bearer {new_token}",
        httponly=True,
        samesite="none",
        secure=True
    )
    
    return UserInfo(email=subject)