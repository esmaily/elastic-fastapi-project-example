from fastapi import FastAPI
from app.core.db import database, User
from app.api.api import api_router

app = FastAPI(title="FastAPI Elastic Example Project")

app.include_router(api_router, prefix="/api")


@app.get("/")
async def root():
    return {"my bab"}
    # return await User.objects.all()


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()
    # create a dummy entry
    # await User.objects.get_or_create(email="jeffry@test.com")


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()
