from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, validator


class UserGeo(BaseModel):
    user_id: int = Field(title="ID пользователя", default=1)
    longitude: float = Field(title="Долгота")
    latitude: float = Field(title="Ширина")
    datetime_at: datetime = Field(
        default_factory=lambda: datetime.now(), title="Время получения"
    )
    session_id: UUID = Field(default_factory=lambda: uuid4())

    @validator("latitude")
    def longitude_validate(cls, longitude: float):
        if not -180 <= longitude <= 180:
            raise ValueError("Longitude is not +/- 180 degrees")
        return longitude

    @validator("latitude")
    def latitude_validate(cls, latitude: float):
        if not -90 <= latitude <= 90:
            raise ValueError("Latitude is not +/- 90 degrees")
        return latitude

    @property
    def wkt(self) -> str:
        return f"SRID=4326;POINT({self.longitude} {self.latitude})"
