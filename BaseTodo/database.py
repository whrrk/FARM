from decouple import config
from typing import Union
import motor.motor_asyncio
from bson.objectid import ObjectId
from fastapi import HTTPException
from auth_utils import AuthJwtCsrf
import asyncio

MONGO_API_KEY = config("MONGO_API_KEY")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_API_KEY)
client.get_io_loop = asyncio.get_event_loop

database = client.FASTAPI
collection_todos = database.todo
collection_user = database.user
auth = AuthJwtCsrf()

def todo_serializer(todo) -> dict:
    return {
        "id": str(todo["_id"]),
        "title": todo["title"],
        "description": todo["description"],
        "owner_email": todo["owner_email"],
        "done": todo["done"]
    }

def user_serializer(user) -> dict:
    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "password": user["password"],
    }

async def db_create_todo(data: dict) -> Union[dict, bool]:
    todo = await collection_todos.insert_one(data)
    new_todo = await collection_todos.find_one({"_id": todo.inserted_id})
    
    if new_todo:
        return todo_serializer(new_todo)
    
    return False

async def db_get_todos(email: str) -> list:
    todos = []
    cursor = collection_todos.find({"owner_email": email})

    async for todo in cursor:
        todo["id"] = str(todo["_id"])
        todo.pop("_id", None)
        todos.append(todo)

    return todos

async def db_get_single_todo(id: str) -> Union[dict, bool]:
    todo = await collection_todos.find_one({"_id": ObjectId(id)})
    if todo:
        return todo_serializer(todo)
    
    return False

async def db_update_todo(id: str, data: dict) -> Union[dict, bool]:
    todo = await collection_todos.find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": data}
    )

    if todo:
        updated_todo = await collection_todos.find_one({"_id": ObjectId(id)})
        return todo_serializer(updated_todo)
    
    return False

async def db_delete_todo(id: str, email: str) -> bool:  
    todo = await collection_todos.delete_one(
        {"_id": ObjectId(id), "owner_email": email}
        )
    
    if todo.deleted_count:
        return True
    
    return False

async def db_signup(data: dict) -> dict:
    email = data.get("email")
    password = data.get("password")
    overlap_user = await collection_user.find_one({"email": email})
    
    if overlap_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    if not password or len(password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters long")
    
    user = await collection_user.insert_one({"email": email, "password": auth.generate_hashed_password(password)})
    new_user = await collection_user.find_one({"_id": user.inserted_id})
    
    return user_serializer(new_user)

async def db_login(data: dict) -> str:
    email = data.get("email")
    password = data.get("password")
    user = await collection_user.find_one({"email": email})

    if not user or not auth.verify_password(password, user["password"]):
        raise HTTPException(
            status_code=401, detail="Invalid email or password")
    
    token = auth.encode_jwt(user["email"])

    return token

async def db_get_user_by_email(email: str) -> str|bool:
    user = await collection_user.find_one({"email": email})

    if user:
        return user
    
    return False
    