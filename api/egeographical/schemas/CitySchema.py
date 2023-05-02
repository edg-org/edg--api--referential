from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from api.egeographical.schemas.AreaSchema import AreaSchema


class CityCoordinates(BaseModel):
    altitude: float
    latitude: float
    longitude: float


class CityInfos(BaseModel):
    prefecture_code: int
    name: str
    type: str
    level: str
    coordinates: Optional[CityCoordinates]


class CityBase(BaseModel):
    code: Optional[int]
    prefecture_id: Optional[int]
    type_id: Optional[int]
    level_id: Optional[int]
    zipcode: Optional[int]
    infos: CityInfos

    class Config:
        orm_mode = True


class CreateCity(CityBase):
    pass


class CitySchema(CityBase):
    id: int
    is_activated: bool
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]


class CityItemSchema(CitySchema):
    areas: list[AreaSchema] = []
