from fastapi import FastAPI
from contextlib import asynccontextmanager
from typing import AsyncIterator, Optional, Union

from aiopg.sa import create_engine
from aiopg.sa.connection import SAConnection
from aiopg.sa.engine import Engine
from aiopg.sa.result import RowProxy
from psycopg2.extras import DictCursor
from sqlalchemy.sql import Update
from sqlalchemy.sql.selectable import Select


from aioredis import ConnectionPool, Redis

from core.setting import (
    REDIS_POOL_MAX,
    REDIS_POOL_MIN,
    REDIS_CONNECTION,
    POSTGRES_DB_NAME,
    POSTGRES_DB_USER,
    POSTGRES_DB_PORT,
    POSTGRES_DB_HOST,
    POSTGRES_DB_PASSWORD,
)


class DatabaseException(Exception):
    pass


class ReturnMoreOneRowDatabaseException(DatabaseException):
    pass


class NoRowsDatabaseException(DatabaseException):
    pass


class Database:
    __engine: Optional[Engine] = None

    @classmethod
    async def start(cls) -> None:
        if not cls.__engine:
            cls.__engine = await create_engine(
                user=POSTGRES_DB_USER,
                database=POSTGRES_DB_NAME,
                host=POSTGRES_DB_HOST,
                password=POSTGRES_DB_PASSWORD,
                port=POSTGRES_DB_PORT,
                cursor_factory=DictCursor,
            )

    @classmethod
    async def stop(cls) -> None:
        if cls.__engine:
            cls.__engine.close()
            cls.__engine = None

    @classmethod
    @asynccontextmanager
    async def connection(cls) -> AsyncIterator[SAConnection]:
        async with cls.__engine.acquire() as connection:
            yield connection

    @classmethod
    async def fetch(cls, query: Union[str, Select], *args, **kwargs) -> list[RowProxy]:
        async with cls.connection() as conn:
            records = await conn.execute(query, *args, **kwargs)
            results: list[RowProxy] = await records.fetchall()
            return results

    @classmethod
    async def bulk(cls, sql: str, args: list[tuple]) -> None:
        if not args:
            return
        async with cls.connection() as connection:
            await connection.execute(sql, args)

    @classmethod
    async def get_rows(cls, query: Union[str, Select], *args, **kwargs) -> list[dict]:
        async with cls.connection() as connection:
            request = await connection.execute(query, *args, **kwargs)
            rows = await request.fetchall()
            return list(map(dict, rows))

    @classmethod
    async def fetchone(cls, query: Union[str, Select]) -> dict:
        """
            Fetch one row

        Args:
            query: SQL query

        Raises:
            ReturnMoreOneRowDatabaseException: возвращается больше одной строки
            NoRowsDatabaseException: нет строк для возврата
        """

        rows = await cls.fetch(query)
        rows = [dict(row) for row in rows]

        if len(rows) == 1:
            return rows[0]
        elif len(rows) > 1:
            raise ReturnMoreOneRowDatabaseException
        else:
            raise NoRowsDatabaseException

    @classmethod
    async def execute(cls, query: Union[str, Select, Update], *args, **kwargs) -> None:
        async with cls.connection() as connection:
            await connection.execute(query, *args, **kwargs)


async def connect_to_redis(app: FastAPI) -> None:
    pool_redis = ConnectionPool.from_url(
        REDIS_CONNECTION, minsize=REDIS_POOL_MIN, maxsize=REDIS_POOL_MAX
    )
    app.state.redis = Redis(connection_pool=pool_redis)
    app.state.pool_redis = pool_redis


async def close_redis_connection(app: FastAPI) -> None:
    pool_redis: ConnectionPool = app.state.pool_redis
    await pool_redis.disconnect()

    redis: Redis = app.state.redis

    await redis.close()
