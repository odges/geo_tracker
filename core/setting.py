from starlette.config import Config

config = Config(".env")

POSTGRES_DB_HOST: str = config("POSTGRES_DB_HOST", cast=str)
POSTGRES_DB_PORT: str = config("POSTGRES_DB_PORT", cast=str)
POSTGRES_DB_NAME: str = config("POSTGRES_DB_NAME", cast=str)
POSTGRES_DB_USER: str = config("POSTGRES_DB_USER", cast=str)
POSTGRES_DB_PASSWORD: str = config("POSTGRES_DB_PASSWORD", cast=str)

DB_CONNECTION = f"postgresql://{POSTGRES_DB_USER}:{POSTGRES_DB_PASSWORD}@{POSTGRES_DB_HOST}:{POSTGRES_DB_PORT}/{POSTGRES_DB_NAME}"

MAX_CONNECTIONS_COUNT: int = 10
MIN_CONNECTIONS_COUNT: int = 10

DEBUG: bool = config("DEBUG", cast=bool)

REDIS_HOST: str = config("REDIS_HOST", cast=str)
REDIS_PORT: str = config("REDIS_PORT", cast=str)

REDIS_CONNECTION = f"redis://{REDIS_HOST}:{REDIS_PORT}"
REDIS_POOL_MIN = 1
REDIS_POOL_MAX = 10
