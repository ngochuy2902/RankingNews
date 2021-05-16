import logging

from fastapi import APIRouter, FastAPI
from starlette.middleware.cors import CORSMiddleware
from settings import BaseConfig as Conf

from .article import article_app
from .audio import audio_app
from .auth import auth_app
from .category import category_app
from .rank import rank_app
from .user import user_app

from data.mysqldb import pool, init_pool


async def shutdown():
    if bool(pool):
        pool.close()
        await pool.wait_closed()


async def startup():
    pool = await init_pool(host=Conf.MYSQL_HOST, port=3306, user=Conf.USER, password=Conf.MYSQL_PASSWORD,
                           db=Conf.MYSQL_DATABASE)
    if bool(pool) is False:
        raise ValueError("pool error connect")


def init_app():
    app = FastAPI()
    app.add_event_handler(event_type="startup", func=startup)
    app.add_event_handler(event_type="shutdown", func=shutdown)
    origins = [
        "http://localhost:3000",
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(article_app)
    app.include_router(auth_app)
    app.include_router(category_app)
    app.include_router(user_app)
    app.include_router(rank_app)
    app.include_router(audio_app)
    return app
