from fastapi import APIRouter
from fastapi import Response, Request, HTTPException
from fastapi.encoders import jsonable_encoder
from schemas import Todo, TodoBody
from database import db_create_todo,db_get_single_todo, db_get_todos, db_update_todo, db_delete_todo
from starlette.status import HTTP_201_CREATED
import jwt

router = APIRouter(
    prefix="/api/todo",
    tags=["todo"],
    responses={404: {"description": "項目が見つかりません"}},
)

@router.post("/", response_model=Todo)
async def create_todo(request: Request, response: Response, data: TodoBody):
    todo = jsonable_encoder(data)
    res = await db_create_todo(todo)
    response.status_code = HTTP_201_CREATED
    if res:
        return res
    return HTTPException(
        status_code=404, detail="Create Task Failed")

@router.get("/", response_model=list[Todo])
async def get_todos():
    res = await db_get_todos()
    return res

@router.get("/{id}", response_model=Todo)
async def get_single_todo(id: str):
    todo =  await db_get_single_todo(id)
    if todo:
        return todo
    return HTTPException(
        status_code=404, detail="Task of ID: {id} doesn't exist")

@router.put("/{id}", response_model=Todo)
async def update_todo(id: str, data: TodoBody):
    todo = jsonable_encoder(data)
    updated_todo = await db_update_todo(id, todo)
    if updated_todo:
        return updated_todo
    return HTTPException(
        status_code=404, detail="Update Task Failed")  

@router.delete("/{id}")
async def delete_todo(id: str):
    deleted_todo = await db_delete_todo(id)
    if deleted_todo:
        return {"message": "Task deleted successfully"}
    return HTTPException(
        status_code=404, detail="Delete Task Failed")
