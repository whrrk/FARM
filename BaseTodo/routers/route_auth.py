from fastapi import APIRouter, Depends
from fastapi import Response, Request,HTTPException
from fastapi.encoders import jsonable_encoder
from schemas import UserBody, SuccessMsg, UserInfo, Csrf
from database import db_signup, db_login, db_get_user_by_email
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

@router.post("/signup", response_model=UserInfo)
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
        samesite="lax",
        secure=True
    )
    
    return SuccessMsg(message="ログインに成功しました。")

@router.post("/logout", response_model=SuccessMsg)
async def logout_user(response: Response):
    response.delete_cookie("access_token")
    
    return SuccessMsg(message="ログアウトに成功しました。")

@router.get("/me")
async def get_current_user(request: Request):
    try:
        token = request.cookies.get("access_token")
        if not token:
            raise HTTPException(status_code=401, detail="No token")
        
        if token.startswith("Bearer "):
            token = token.replace("Bearer ", "")

        email = auth.decode_jwt(token)
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = await db_get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return {"email": email}

    except Exception as e:
        raise HTTPException(status_code=401, detail="Authentication failed")

@router.get("/user", response_model=UserInfo)
def get_user_refresh_jwt(request: Request, response: Response):
    new_token, subject = auth.verify_update_jwt(request)
    
    response.set_cookie(
        key="access_token",
        value=f"Bearer {new_token}",
        httponly=True,
        samesite="lax",
        secure=True
    )
    
    return UserInfo(email=subject)