# main.py
from fastapi import FastAPI

from app.routes.route import router

app = FastAPI()
app.include_router(router)
