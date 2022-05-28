from fastapi import FastAPI

import aiopg
from aioredis import ConnectionPool, Redis

from core.setting import (
    REDIS_POOL_MAX,
    REDIS_POOL_MIN,
    REDIS_CONNECTION,
    DB_CONNECTION,
    MAX_CONNECTIONS_COUNT,
    MIN_CONNECTIONS_COUNT,
)


async def connect_to_db(app: FastAPI) -> None:
    app.state.pool_postgres = await aiopg.create_pool(
        DB_CONNECTION,
        minsize=MIN_CONNECTIONS_COUNT,
        maxsize=MAX_CONNECTIONS_COUNT,
    )


async def close_db_connection(app: FastAPI) -> None:
    await app.state.pool_postgres.close()


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
