from datetime import datetime
from pydantic import BaseModel, Field, validator


class UserGeo(BaseModel):
    user_id: int = Field(title="ID пользователя")
    longitude: float = Field(title="Долгота")
    latitude: float = Field(title="Ширина")
    datetime_at: datetime = Field(
        default_factory=lambda: datetime.now(), title="Время получения"
    )

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
