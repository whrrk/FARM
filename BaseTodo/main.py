from fastapi import FastAPI
from routers import route_todo, route_auth
from schemas import SuccessMsg

app = FastAPI(
    title="TODO管理API",
    description="このAPIはTODO項目の作成・取得・更新・削除を行います。",
    version="1.0.0",
)

app.include_router(route_todo.router)
app.include_router(route_auth.router)

@app.get("/", response_model=SuccessMsg)
def root():
    return {"message": "Welome to FastAPI!"}
