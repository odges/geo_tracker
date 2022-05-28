from typing import Callable

from fastapi import FastAPI
from core.database import (
    Database,
)


def create_start_app_handler(app: FastAPI) -> Callable:
    async def start_app() -> None:
        await Database.start()

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:
    async def stop_app() -> None:
        await Database.stop()

    return stop_app
