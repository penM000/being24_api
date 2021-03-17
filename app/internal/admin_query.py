import datetime
import copy
from ..database import data_collection, search_tag_collection, update_date_collection

def same_dictionary_check(dict1, dict2, exclusion_key_list=["date"]):
    """
    辞書が同じならTrue
    """
    # 辞書の独立化
    copy_dict1, copy_dict2 = copy.copy(dict1), copy.copy(dict2)
    for exclusion_key in exclusion_key_list:
        try:
            del copy_dict1[exclusion_key]
        except KeyError:
            pass

        try:
            del copy_dict2[exclusion_key]
        except KeyError:
            pass
    if copy_dict1 == copy_dict2:
        return True
    else:
        return False


async def get_date(mainkey, key):
    cursor = data_collection.find({mainkey: key}, {
        "_id": 0, "date": 1}).sort("date", -1)
    result = [doc["date"] async for doc in cursor]
    return result


async def update_data_db(newdocument, mainkey="id"):
    # 時刻インスタンス生成
    JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
    dt_now = datetime.datetime.now(JST)
    # 最新データとの比較
    # 日付のリストを取得
    dates = await get_date(mainkey, newdocument[mainkey])
    old_document = None
    if len(dates) == 0:
        pass
    else:
        old_document = await data_collection.find_one(
            {
                mainkey: newdocument[mainkey],
                "date": dates[0]
            },
            {
                "_id": 0
            }
        )
    if old_document is None:
        pass
    elif same_dictionary_check(newdocument, old_document, ["_id", "date"]):
        return

    document = await data_collection.find_one(
        {
            mainkey: newdocument[mainkey],
            "date": str(dt_now.date())
        }
    )
    # 新規登録データ
    if document is None:
        result = await data_collection.insert_one(newdocument)
    # 更新データ(同じ日付の更新)
    else:
        # データベースID取得
        _id = document['_id']
        # データベース更新
        result = await data_collection.replace_one(
            {'_id': _id},
            newdocument
        )
    return result

# tag検索用コレクション更新


async def update_tag_text_search_db(newdocument, mainkey="id"):
    document = await search_tag_collection.find_one(
        {mainkey: newdocument[mainkey]}
    )
    # 新規登録データ
    if document is None:
        result = await search_tag_collection.insert_one(newdocument)
    # 更新データ(同じ日付の更新)
    else:
        # データベースID取得
        _id = document['_id']
        # データベース更新
        result = await search_tag_collection.replace_one(
            {'_id': _id},
            newdocument
        )
    return result


# データベース最終更新日更新


async def update_last_update_date():
    JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
    dt_now = datetime.datetime.now(JST)
    document = await update_date_collection.find_one(
        {"last_update": "last_update"}
    )
    newdocument = {
        "last_update": "last_update",
        "fulldate": str(dt_now),
        "date": str(dt_now.date())
    }
    if document is None:
        result = await update_date_collection.insert_one(newdocument)
    # 更新データ(同じ日付の更新)
    else:
        # データベースID取得
        _id = document['_id']
        # データベース更新

        result = await update_date_collection.replace_one(
            {'_id': _id}, newdocument
        )
    return result