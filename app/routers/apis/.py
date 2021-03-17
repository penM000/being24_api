from fastapi import APIRouter, Depends, HTTPException,Query
from typing import List


router = APIRouter(
    prefix="/tag_serch",
    tags=["tag_serch"],
    responses={404: {"description": "Not found"}},
)

@router.get("/fullname/perfect")
async def get_all_fullname(tags : List[str] = Query(None) ):
    return tags

@router.get("/fullname/fuzzy")
async def get_all_fullname(tags : List[str] = Query(None) ):
    return tags

@router.get("/pageid/perfect")
async def get_all_fullname(tags : List[str] = Query(None) ):
    return tags

@router.get("/pageid/fuzzy")
async def get_all_fullname(tags : List[str] = Query(None) ):
    return tags