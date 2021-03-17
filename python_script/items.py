import asyncio
import datetime
import json
import random
import string
import copy

import aiofiles

import database
import re


async def test():
    await database.database_update_structure()




# システム状態変数
update_status = "NO"
last_update = ""
all_mainkey = {}


# データベース最適化




# ページ切り出し


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





# fullnameと日付で全情報を取得


async def get_metatitle_search(metatitle):
    result = await database.mainkey_search("metatitle", metatitle)
    return result


async def get_fullname_search(metatitle):
    result = await database.mainkey_search("fullname", metatitle)
    return result





async def get_status():
    global all_mainkey
    JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
    dt_now = datetime.datetime.now(JST)
    if "fullname" not in all_mainkey:
        all_mainkey["fullname"] = await database.get_all_mainkey_from_db(
            "fullname"
        )
    fulldate = await database.get_last_update_date()
    status = {
        "update_status": update_status,
        "date": dt_now.date(),
        "total_fullname": len(all_mainkey["fullname"]),
        "last_update": fulldate}
    return status





async def get_rate_from_mainkey_during_the_period(mainkey, key, start, stop):
    max_dates = 367
    try:
        startdatetime = datetime.datetime.strptime(start, '%Y-%m-%d')
        stopdatetime = datetime.datetime.strptime(stop, '%Y-%m-%d')
    except BaseException:
        return {}
    startdate = datetime.date(
        startdatetime.year,
        startdatetime.month,
        startdatetime.day)
    stopdate = datetime.date(
        stopdatetime.year,
        stopdatetime.month,
        stopdatetime.day)
    date_range = int((stopdate - startdate).days)
    temp = []
    if max_dates < date_range:
        temp = [str(stopdate - datetime.timedelta(days=i))
                for i in range(max_dates)]
    else:
        temp = [str(stopdate - datetime.timedelta(days=i))
                for i in range(date_range)]
    if len(temp) == 0:
        return {}

    query = {"$or": [{mainkey: key, "date": date} for date in temp]}

    cursor = database.data_collection.find(query, {
        "_id": 0, "date": 1, "rating": 1, "rating_votes": 1}).sort("date", -1)
    result = {
        doc["date"]: {key: doc[key] for key in doc.keys()
                      if (key != "date")} async for doc in cursor
    }
    return result





async def get_dates_from_mainkey(mainkey, key, _range, _page):
    dates = await database.get_date_from_mainkey_db(mainkey, key)
    return make_page(dates, _range, _page)


async def get_id_from_metatitle(metatitle):
    result = await database.get_id("metatitle", metatitle)
    return result


async def get_id_from_fullname(fullname):
    result = await database.get_id("fullname", fullname)
    return result


async def get_id_during_time_from_created_at(start, stop):
    result = await database.get_id_during_time_from_created_at(start, stop)
    return result



