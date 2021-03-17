from ..database import update_date_collection, data_collection, search_tag_collection
import datetime
import re
# データベース最終更新日取得
async def get_last_update_date():
    result = await update_date_collection.find_one(
        {"last_update": "last_update"},
        {"_id": 0, "fulldate": 1, "date": 1}
    )
    return result

async def get_date(mainkey, key):
    """
    取得可能な日時をデータベースに問い合わせ
    """
    cursor = data_collection.find(
        {
            mainkey: key
        }, 
        {
            "_id": 0, 
            "date": 1
        }).sort("date", -1)
    result = [doc["date"] async for doc in cursor]
    return result

async def get_latest_metadata_db(mainkey, key):
    """
    タグコレクションから最新のメタデータを問い合わせ
    """
    return await search_tag_collection.find_one(
        {mainkey: key},
        {"_id": 0}
    )

async def get_all_mainkey_from_db(mainkey):
    """
    全区間データからカラム名で集計
    """
    pipeline = [
        {
            "$group": {"_id": "$" + mainkey}
        },
        {
            "$sort": {"_id": 1}
        }
    ]
    cursor = data_collection.aggregate(pipeline, allowDiskUse=True)
    result = [doc["_id"] async for doc in cursor if doc["_id"] is not None]
    return result


async def mainkey_search(mainkey, key, sorting_by="rating"):
    cursor = search_tag_collection.find(
        {
            mainkey: {"$regex": re.escape(key)},
        },
        {
            "_id": 0,
            mainkey: 1,
        }
    ).sort(sorting_by, -1)
    result = [
        doc[mainkey] async for doc in cursor
        if mainkey in doc and doc[mainkey] is not None
    ]
    return result


async def get_data_from_mainkey_and_date_db(mainkey, key, date):
    document = await data_collection.find_one(
        {
            mainkey: key,
            "date": date
        },
        {
            "_id": 0
        }
    )
    return document


async def get_id_from_metatitle(metatitle):
    document = await search_tag_collection.find_one(
        {
            "metatitle": metatitle,
        },
        {
            "_id": 0,
            "id": 1
        }
    )
    return document


async def get_id(mainkey, key):
    document = await search_tag_collection.find_one(
        {
            mainkey: key,
        },
        {
            "_id": 0,
            "id": 1
        }
    )
    return document


async def get_id_during_time_from_created_at(start, stop):
    try:
        start = datetime.datetime.strptime(start, '%Y-%m-%d')
        stop = datetime.datetime.strptime(stop, '%Y-%m-%d')
    except BaseException:
        return

    cursor = search_tag_collection.find(
        {"created_at": {'$lt': stop, '$gte': start}})
    result = [doc["id"] async for doc in cursor if doc["id"] is not None]
    return result