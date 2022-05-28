from typing import Callable

from fastapi import FastAPI
from core.database import (
    connect_to_db,
    connect_to_redis,
    close_db_connection,
    close_redis_connection,
)


def create_start_app_handler(app: FastAPI) -> Callable:
    async def start_app() -> None:
        await connect_to_db(app)
        await connect_to_redis(app)

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:
    async def stop_app() -> None:
        await close_db_connection(app)
        await close_redis_connection(app)

    return stop_app
