from fastapi import APIRouter, Depends, HTTPException


router = APIRouter(
    prefix="/pageid",
    tags=["pageid"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_all_fullname(_range = 10 ,_page = 1 ):
    return "ok"

@router.get("/{pageid}")
async def get_data(pageid: str):
    return 

@router.get("/{pageid}/dates")
async def get_data(pageid: str):
    return 

@router.get("/{pageid}/{date}")
async def get_data(pageid: str, date: str):
    return 

@router.get("/{pageid}/rate")
async def get_data(pageid: str, start: str, stop: str):
    return 