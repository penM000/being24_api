from fastapi import APIRouter, Depends, HTTPException


router = APIRouter(
    prefix="/fullname",
    tags=["fullname"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_all_fullname(_range = 10 ,_page = 1 ):
    return "ok"

@router.get("/{fullname}")
async def get_data(fullname: str):
    return 

@router.get("/{fullname}/dates")
async def get_data(fullname: str):
    return 

@router.get("/{fullname}/{date}")
async def get_data(fullname: str, date: str):
    return 

@router.get("/{fullname}/rate")
async def get_data(fullname: str, start: str, stop: str):
    return 