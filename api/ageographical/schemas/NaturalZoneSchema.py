from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from api.ageographical.schemas.RegionSchema import (
    RegionSchema,
)


class ZoneCoordinates(BaseModel):
    altitude: float
    latitude: float
    longitude: float


#
class ZoneBase(BaseModel):
    code: Optional[int]
    name: str
    coordinates: Optional[ZoneCoordinates]

    class Config:
        orm_mode = True


#
class CreateZone(ZoneBase):
    pass


class ZoneSchema(ZoneBase):
    id: int
    is_activated: bool
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]


class ZoneItemSchema(ZoneSchema):
    regions: list[RegionSchema] = []
