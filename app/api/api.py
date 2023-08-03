from fastapi import APIRouter
from app.api import articles

api_router = APIRouter()
api_router.include_router(articles.router, prefix="/articles")
