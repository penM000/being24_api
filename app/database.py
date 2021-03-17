import motor.motor_asyncio
import datetime
import copy
import dateutil.parser
import re

# データベース名設定
database_name = "ayame_api"
data_collection_name = "data_collection"
search_tag_collection_name = "tag_search"
update_date_collection_name = "last_update_date"

# データベースインスタンス作成
client = motor.motor_asyncio.AsyncIOMotorClient(
    'mongodb://mongodb:27017/?compressors=snappy')
db = client[database_name]
collection = db[data_collection_name]
data_collection = db[data_collection_name]
search_tag_collection = db[search_tag_collection_name]
update_date_collection = db[update_date_collection_name]

# インデックス作成
async def make_index():
    await data_collection.create_index("id")
    await data_collection.create_index("fullname")
    await data_collection.create_index("date")
    await data_collection.create_index([("date", -1)])
    await data_collection.create_index([("tags", 1)])

    await search_tag_collection.create_index("id")
    await search_tag_collection.create_index("fullname")
    await search_tag_collection.create_index("created_at")
    await search_tag_collection.create_index([("tags", 1)])
    await search_tag_collection.create_index([("metatitle", 1)])

# データベース圧縮
async def compact_db():
    await db.command({"compact": data_collection_name})
    await db.command({"compact": search_tag_collection_name})
    await db.command({"compact": update_date_collection_name})



















