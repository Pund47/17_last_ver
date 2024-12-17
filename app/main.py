from fastapi import FastAPI
from .routers import task
from .routers import user
#python -m uvicorn app.main:app
app = FastAPI()
app.include_router(task.router)
app.include_router(user.router)


@app.get("/")
async def welcome():
    return {"message":"Welcome to Taskmanager"}