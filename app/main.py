from fastapi import FastAPI
from app.routes import tasks, auth

app = FastAPI()

app.include_router(auth.router)
app.include_router(tasks.router)
