from pydantic import BaseModel
from typing import Optional
from decouple import config

CSRF_KEY = config("CSRF_KEY")

class Todo(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    owner_email: str
    done: bool

class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    done: bool = False

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    done: bool = False

class SuccessMsg(BaseModel):
    message: str

class UserBody(BaseModel):
    email: str
    password: str

class UserInfo(BaseModel):
    id: Optional[str] = None    
    email: str

class Csrf(BaseModel):
    csrf_token: str

class CsrfSettings(BaseModel):
    secret_key: str = CSRF_KEY