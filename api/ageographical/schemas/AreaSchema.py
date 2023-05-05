from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from api.ageographical.schemas.AgencySchema import (
    AgencySchema,
)


class AreaCoordinates(BaseModel):
    altitude: float
    latitude: float
    longitude: float


class AreaInfos(BaseModel):
    city_code: int
    name: str
    type: str  # neighborhood, district, village,  industrial area, administrative area
    coordinates: Optional[AreaCoordinates]


class AreaBase(BaseModel):
    code: Optional[int]
    city_id: Optional[int]
    type_id: Optional[int]
    zipcode: Optional[int]
    infos: AreaInfos

    class Config:
        orm_mode = True


class CreateArea(AreaBase):
    pass


class AreaSchema(AreaBase):
    id: int
    is_activated: bool
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]


class AreaItemSchema(AreaSchema):
    agencies: list[AgencySchema] = []
