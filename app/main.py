from fastapi import FastAPI
from app.core.db import database, User
from app.api.api import api_router

app = FastAPI(title="FastAPI Elastic Example Project")

app.include_router(api_router, prefix="/api")
from app.core.listener import init_listen_queues


@app.get("/")
async def root():
    return {"FastAPI Elastic Example Project Main Page"}


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()
    # consume_message()
    init_listen_queues()

@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()
