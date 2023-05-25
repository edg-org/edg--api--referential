from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from api.ageographical.schemas.RegionSchema import RegionSchema

class ZoneSearchParams(BaseModel):
    code: int = Field(description="Field of the natural region code")
    name: str | None = Field(description="Field of the natural region name")

class ZoneCoordinates(BaseModel):
    altitude: float
    latitude: float
    longitude: float

class ZoneInput(BaseModel):
    name: str
    coordinates: Optional[ZoneCoordinates]

class ZoneUpdate(ZoneInput):
    pass
#
class ZoneBase(ZoneInput):
    code: int

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