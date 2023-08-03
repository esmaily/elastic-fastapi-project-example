from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException

router = APIRouter()


@router.get("/")
async def article_list():
    return {"atic list"}
    # return await User.objects.all()


@router.get("//{title}")
async def article_by_title():
    return {"my by tit"}
    # return await User.objects.all()


@router.post("/")
async def article_store():
    return {"my post"}
    # return await User.objects.all()
