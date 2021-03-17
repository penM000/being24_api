from fastapi import APIRouter, Depends, HTTPException,Query
from typing import List


router = APIRouter(
    prefix="/serch",
    tags=["serch"],
    responses={404: {"description": "Not found"}},
)

async def get_mainkey_from_latest_tag_fuzzy_search(mainkey, tags):
    if len(tags) == 0:
        return []
    if tags[0] is None:
        return []
    cursor = database.search_tag_collection.find(
        {
            "$and": [{"tags": {"$regex": re.escape(key)}} for key in tags],
        },
        {
            "_id": 0,
            mainkey: 1
        }
    ).sort(mainkey)
    result = [
        doc[mainkey] async for doc in cursor
        if mainkey in doc and doc[mainkey] is not None
    ]
    return result


async def get_mainkey_from_latest_tag_perfect_matching(mainkey, tags):

    if len(tags) == 0:
        return []
    if tags[0] is None:
        return []
    cursor = database.search_tag_collection.find(
        {
            "tags": {"$all": tags}
        },
        {
            "_id": 0,
            mainkey: 1,
            "date": 1
        }
    ).sort(mainkey)
    result = [
        doc[mainkey] async for doc in cursor
        if mainkey in doc and doc[mainkey] is not None
    ]
    return result



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


