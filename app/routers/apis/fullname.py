import datetime
from fastapi import APIRouter, Depends, HTTPException
from ...internal.api_query import       \
    get_all_mainkey_from_db,            \
    get_data_from_mainkey_and_date_db,  \
    get_date_from_mainkey_db,           \
    get_latest_metadata_db

router = APIRouter(
    prefix="/fullname",
    tags=["fullname"],
    responses={404: {"description": "Not found"}},
)

def make_page(_list, _range, _page):
    _min = abs(_range) * (abs(_page) - 1)
    _max = abs(_range) * (abs(_page))
    if _min < 0:
        _min = 0
    if _max > len(_list):
        _max = len(_list)
    return _list[_min: _max]

def str_to_date(date):
    try:
        normalization_date = datetime.datetime.strptime(date, '%Y-%m-%d')
        normalization_date = str(
            datetime.date(
                normalization_date.year,
                normalization_date.month,
                normalization_date.day))
    except BaseException:
        normalization_date = date
    return normalization_date

#キャッシュ
all_fullname=[]
@router.get("/")
async def get_all_fullname(_range = 10 ,_page = 1 ):
    global all_fullname
    if len(all_fullname):
        pass
    else:
        all_fullname = await get_all_mainkey_from_db("fullname")
    return make_page(all_fullname, _range, _page)


@router.get("/{fullname}")
async def get_latest_metadata(fullname: str):
    return await get_latest_metadata_db("fullname", fullname)

@router.get("/{fullname}/dates")
async def get_dates(fullname: str, _range: int, _page :int):
    dates = await get_date_from_mainkey_db("fullname", fullname)
    return make_page(dates, _range, _page)



@router.get("/{fullname}/{date}")
async def get_metadata(fullname: str, date: str):
    result = get_data_from_mainkey_and_date_db(
        "fullname",
        fullname,
        str_to_date(date)
    )
    return await result


@router.get("/{fullname}/rate")
async def get_data(fullname: str, start: str, stop: str):
    return 


