from typing import Any, List
from app.core.db import Article
from fastapi import APIRouter, Body, Depends, HTTPException
from app.tasks import create_article_task

router = APIRouter()
import json


@router.get("/", response_model=List[Article])
async def article_list():
    return await Article.objects.all()


@router.get("/{title}", response_model=Article)
async def article_by_title(title: str):
    return await Article.objects.filter(title=title).get()


@router.post("/", response_model=Article)
async def article_store(article: Article):
    payload = json.dumps({
        "title": article.title,
        "content": article.content,
        "author": article.author,
        "created_at": article.created_at.strftime("%Y-%m-%d %H:%M:%S")
    })
    create_article_task.delay(payload)
    return await article.save()
