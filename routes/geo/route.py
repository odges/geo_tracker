from fastapi import APIRouter, Response

from apps.geo_data.schema import UserGeo
from apps.geo_data.repository import create_record_geo, create_session, create_user

router = APIRouter()


@router.post("/geo")
async def recive_user_geo(user_geo: UserGeo):
    """receive geo data"""
    return await create_record_geo(user_geo=user_geo)


@router.post("/user")
async def create_use_route():
    """receive geo data"""
    return await create_user(password="some")


@router.post("/session")
async def create_session_route(user_id: int = 1):
    """receive geo data"""
    return await create_session(user_id=user_id)
