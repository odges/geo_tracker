from apps.geo_data.schema import UserGeo
from core.database import Database


async def create_record_geo(user_geo: UserGeo) -> None:

    sql = """
        INSERT INTO location(
            session_id, point, datetime_at
        )
        VALUES (%(session_id)s, %(point)s, %(datetime_at)s);    
    """
    await Database.execute(
        sql,
        session_id=user_geo.session_id,
        point=user_geo.wkt,
        datetime_at=user_geo.datetime_at,
    )


async def create_session(user_id: int) -> None:

    sql = """
        INSERT INTO session_record(user_id)
        VALUES (%(user_id)s);
    """

    await Database.execute(sql, user_id=user_id)


async def create_user(password: str) -> None:

    sql = """
        INSERT INTO "user"(
            password)
            VALUES (%(password)s);
    """

    await Database.execute(sql, password=password)
