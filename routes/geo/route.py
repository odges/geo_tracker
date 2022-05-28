from fastapi import APIRouter, Response

from apps.geo_data.schema import UserGeo

router = APIRouter()


@router.post("/geo")
def recive_user_geo(user_geo: UserGeo):
    """receive geo data"""
    return Response(status_code=200)
