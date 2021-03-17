from fastapi import APIRouter, Depends, HTTPException,Query
from typing import List


router = APIRouter(
    prefix="/serch",
    tags=["serch"],
    responses={404: {"description": "Not found"}},
)

@router.get("/metatitle/{metatitle}")
async def get_all_fullname(metatitle : str ):
    return tags

@router.get("/fullname/{fullname}")
async def get_all_fullname(fullname : str ):
    return tags


@router.get("/fullname/tag/perfect")
async def get_all_fullname(tags : List[str] = Query(None) ):
    return tags

@router.get("/fullname/tag/fuzzy")
async def get_all_fullname(tags : List[str] = Query(None) ):
    return tags

@router.get("/pageid/tag/perfect")
async def get_all_fullname(tags : List[str] = Query(None) ):
    return tags

@router.get("/pageid/tag/fuzzy")
async def get_all_fullname(tags : List[str] = Query(None) ):
    return tags