from fastapi import APIRouter
from fastapi import Response, Request, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from schemas import Todo, TodoBody
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
async def create_todo(request: Request, response: Response, data: TodoBody, csrf_protect: CsrfProtect = Depends()):
    new_token = auth.verify_csrf_update_jwt(
        request, csrf_protect, request.headers
    )
    todo = jsonable_encoder(data)
    res = await db_create_todo(todo)
    response.status_code = HTTP_201_CREATED
    response.set_cookie(
        key="access_token",
        value=f"Bearer {new_token}",
        httponly=True,
        samesite="none",
        secure=True
    )

    if res:
        return res
    return HTTPException(
        status_code=404, detail="Create Task Failed")

@router.get("/", response_model=list[Todo])
async def get_todos(request: Request):
    auth.verify_jwt(request)
    res = await db_get_todos()
    return res

@router.get("/{id}", response_model=Todo)
async def get_single_todo(id: str, request: Request, response: Response):
    new_token, _ = auth.verify_update_jwt(request)
    
    response.set_cookie(
        key="access_token",
        value=f"Bearer {new_token}",
        httponly=True,
        samesite="none",
        secure=True
    )

    todo =  await db_get_single_todo(id)
    if todo:
        return todo
    return HTTPException(
        status_code=404, detail="Task of ID: {id} doesn't exist")

@router.put("/{id}", response_model=Todo)
async def update_todo(request:Request, response: Response, id: str, data: TodoBody, csrf_protect: CsrfProtect = Depends()):
    new_token = auth.verify_csrf_update_jwt(
        request, csrf_protect, request.headers
    )

    response.set_cookie(
        key="access_token",
        value=f"Bearer {new_token}",
        httponly=True,
        samesite="none",
        secure=True
    )
    
    todo = jsonable_encoder(data)
    updated_todo = await db_update_todo(id, todo)
    if updated_todo:
        return updated_todo
    return HTTPException(
        status_code=404, detail="Update Task Failed")  

@router.delete("/{id}")
async def delete_todo(request:Request, response: Response, id: str, data: TodoBody, csrf_protect: CsrfProtect = Depends()):
    new_token = auth.verify_csrf_update_jwt(
        request, csrf_protect, request.headers
    )

    response.set_cookie(
        key="access_token",
        value=f"Bearer {new_token}",
        httponly=True,
        samesite="none",
        secure=True
    )
    
    deleted_todo = await db_delete_todo(id)
    if deleted_todo:
        return {"message": "Task deleted successfully"}
    return HTTPException(
        status_code=404, detail="Delete Task Failed")