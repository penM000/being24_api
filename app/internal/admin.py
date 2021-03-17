import copy
import datetime
import json
import random
import string

import dateutil
import asyncio
import aiofiles
from fastapi import APIRouter

from ..database import make_index, compact_db
from .admin_query import update_data_db, update_tag_text_search_db, update_last_update_date


router = APIRouter()




def randomname(n):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))


def convert_str_in_a_document_to_datetime(document):
    doc = copy.copy(document)
    try:
        doc["created_at"] = dateutil.parser.parse(str(doc["created_at"]))
    except BaseException:
        pass
    try:
        doc["updated_at"] = dateutil.parser.parse(str(doc["updated_at"]))
    except BaseException:
        pass
    try:
        doc["commented_at"] = dateutil.parser.parse(str(doc["commented_at"]))
    except BaseException:
        pass
    return doc

def convert_str_to_int(document):
    doc = copy.copy(document)
    try:
        doc["size"] = int(doc["size"])
    except BaseException:
        pass
    try:
        doc["rating"] = int(doc["rating"])
    except BaseException:
        pass
    try:
        doc["rating_votes"] = int(doc["rating_votes"])
    except BaseException:
        pass
    try:
        doc["comments"] = int(doc["comments"])
    except BaseException:
        pass
    try:
        doc["revisions"] = int(doc["revisions"])
    except BaseException:
        pass
    return doc


async def run(cmd, cwd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        cwd=cwd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    print(f'[{cmd!r} exited with {proc.returncode}]')
    if stdout:
        print(f'[stdout]\n{stdout.decode()}')
    if stderr:
        print(f'[stderr]\n{stderr.decode()}')
    return proc.returncode



update_status=""
@router.get("/update")
async def update(password: str):
    # アップデートパスワード読み込み
    update_password = "hello world"
    try:
        with open("/password.txt") as f:
            update_password = f.read()
    except BaseException:
        update_password = str(randomname(10))
        f = open("/password.txt", 'w')
        f.write(update_password)
        f.close()
    
    # パスワード認証
    if password != update_password:
        return 
    
    # 状態変数
    global update_status
    update_status = "NO"

    # アップデート処理中なら終了
    if update_status == "NO":
        update_status = "progress"
    else:
        return update_status

    # クローラ非同期マルチプロセス実行

    update_status = "get data"
    return_code = await run("python3 /update/ayame/src/get_all.py", "/update/ayame")
    if int(return_code) != 0:
        update_status = "NO"
        return "being24 error"

    # クロールデータのメモリロード
    try:
        json_contents = ""
        async with aiofiles.open(
            '/update/ayame/data/data.json',
            mode='r'
        ) as f:
            json_contents = await f.read()
        json_load = json.loads(str(json_contents))
    except BaseException:
        update_status = "NO"
        return "file load error"

    # データベース更新
    # try:
    # データベースインデックス作成
    await make_index()

    # 進捗状況用変数
    total = len(json_load)
    now_count = 0

    # 時刻インスタンス生成
    JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
    dt_now = datetime.datetime.now(JST)

    for idata in json_load:

        # 進捗状況更新
        now_count += 1
        update_status = str(now_count) + "/" + str(total) + \
            " : " + str(round((now_count / total) * 100, 2)) + "%"
        # データ構造の自動生成

        newdocument = {key: idata[key]
                       for key in idata.keys() if (key != "tags")}
        newdocument["tags"] = idata["tags"].split(" ")
        newdocument["date"] = str(dt_now.date())
        newdocument = convert_str_in_a_document_to_datetime(
            newdocument)
        newdocument = convert_str_to_int(newdocument)
        try:
            newdocument["id"]
        except BaseException:
            print(newdocument)
        # data db更新
        await update_data_db(copy.copy(newdocument))

        # tag検索用db更新
        await update_tag_text_search_db(copy.copy(newdocument))

    update_status = "NO"
    # データベース最適化
    await compact_db()

    # データベース更新日更新
    await update_last_update_date()
    return "update complete"


