import json

from typing import Any, List
from app.core.db import Article
from app.core.elasticsearch import es
from fastapi import APIRouter, Body, Depends, HTTPException
from app.tasks import create_article_task

router = APIRouter()


@router.get("/", response_model=List[Article])
async def article_list():
     return await Article.objects.all()


@router.get("/get/{title}", response_model=Article)
async def article_by_title(title: str):
    return await Article.objects.filter(title=title).get()


@router.post("/")
async def article_store(article: Article):
    payload = json.dumps({
        "title": article.title,
        "content": article.content,
        "author": article.author,
        "created_at": article.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": article.created_at.strftime("%Y-%m-%d %H:%M:%S")
    })
    """ 
    store articles in rabbit mq queues
    """
    create_article_task.delay(payload)

    return {"success":True,"message":"article has been store in article queue"}


@router.get("/search/")
async def search(search_by: str | None):

    # Build the Elasticsearch script query
    script_query = {
        "query": {
            "bool": {
                "must": {
                    "term": {
                        "content": search_by
                    }
                }
            }
        }
    }

    # Execute the search query
    search_results = es.search(index="articles", body=script_query)

    # Process and return the search results
    results = search_results["hits"]["hits"]
    return {"results": results}
