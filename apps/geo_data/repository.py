from aiopg import Pool
from apps.geo_data.schema import UserGeo


async def create_record_geo(user_geo: UserGeo, db: Pool) -> None:
    async with db.acquire() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute()
