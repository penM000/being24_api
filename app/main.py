from fastapi import Depends, FastAPI
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from .internal import admin
from .routers.apis import fullname, search, pageid


app = FastAPI()
# orginsの許可
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
# プロキシヘッダー読み取り
app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")


app.include_router(fullname.router)
app.include_router(pageid.router)
app.include_router(search.router)
app.include_router(
    admin.router,
    prefix="",
    tags=["admin"],
    responses={418: {"description": "I'm a teapot"}},
)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
    