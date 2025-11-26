from fastapi import APIRouter
from fastapi import Response, Request, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from schemas import Todo, TodoCreate, TodoUpdate
from database import db_create_todo,db_get_single_todo, db_get_todos, db_update_todo, db_delete_todo
from starlette.status import HTTP_201_CREATED
from fastapi_csrf_protect import CsrfProtect
from auth_utils import AuthJwtCsrf

router = APIRouter(
    prefix="/api/todo",
    tags=["todo"],
    responses={404: {"description": "項目が見つかりません"}},
)

auth= AuthJwtCsrf()

@router.post("/", response_model=Todo)
async def create_todo(
    request: Request, 
    response: Response, 
    data: TodoCreate, 
    csrf_protect: CsrfProtect = Depends()
    ):

    email, new_token = await auth.verify_csrf_update_jwt(request, csrf_protect)
    todo = jsonable_encoder(data)
    todo["owner_email"] = email

    res = await db_create_todo(todo)
    response.status_code = HTTP_201_CREATED
    response.set_cookie(
        key="access_token",
        value=f"Bearer {new_token}",
        httponly=True,
        samesite="lax",
        secure=False
    )

    if res:
        return res
    return HTTPException(
        status_code=404, detail="Create Task Failed")

@router.get("/", response_model=list[Todo])
async def get_todos(request: Request):
    email = auth.verify_jwt(request)
    res = await db_get_todos(email)
    return res

@router.get("/{id}", response_model=Todo)
async def get_single_todo(id: str, request: Request, response: Response):
    new_token, _ = auth.verify_update_jwt(request)
    
    response.set_cookie(
        key="access_token",
        value=f"Bearer {new_token}",
        httponly=True,
        samesite="lax",
        secure=False
    )

    todo =  await db_get_single_todo(id)
    if todo:
        return todo
    return HTTPException(
        status_code=404, detail="Task of ID: {id} doesn't exist")

@router.put("/{id}", response_model=Todo)
async def update_todo(
    request:Request, 
    response: Response, 
    id: str, 
    data: TodoUpdate, 
    csrf_protect: CsrfProtect = Depends()
    ):

    email, new_token = await auth.verify_csrf_update_jwt(request, csrf_protect)

    response.set_cookie(
        key="access_token",
        value=f"Bearer {new_token}",
        httponly=True,
        samesite="lax",
        secure=False
    )
    
    todo = jsonable_encoder(data)
    todo['owner_email'] = email
    todo = {k: v for k, v in data.dict().items() if v is not None}
    updated_todo = await db_update_todo(id, todo)
    if updated_todo:
        return updated_todo
    return HTTPException(
        status_code=404, detail="Update Task Failed")  

@router.delete("/{id}")
async def delete_todo(
    request:Request, 
    response: Response, 
    id: str, 
    csrf_protect: CsrfProtect = Depends()
    ):

    email, new_token = await auth.verify_csrf_update_jwt(request, csrf_protect)

    response.set_cookie(
        key="access_token",
        value=f"Bearer {new_token}",
        httponly=True,
        samesite="lax",
        secure=False
    )
    
    deleted_todo = await db_delete_todo(id, email)
    if deleted_todo:
        return {"message": "Task deleted successfully"}
    return HTTPException(
        status_code=404, detail="Delete Task Failed")