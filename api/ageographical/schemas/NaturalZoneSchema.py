from pydantic import Field
from datetime import datetime
from typing import List, Optional
from api.configs.BaseModel import BaseSchema
from api.ageographical.schemas.RegionSchema import RegionSchema

#
class ZoneSearchParams(BaseSchema):
    code: int = Field(description="Field of the natural region code")
    name: Optional[str] = Field(description="Field of the natural region name")

#
class ZoneCoordinates(BaseSchema):
    altitude: float
    latitude: float
    longitude: float

#
class ZoneSchema(BaseSchema):
    id: int
    code: int
    name: str
    coordinates: Optional[ZoneCoordinates]
    is_activated: bool
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    class Config:
        orm_mode = True

#
class CreateZone(ZoneSchema):
    class Config:
        fields_to_hide = {
            "id",
            "is_activated",
            "created_at",
            "updated_at",
            "deleted_at",
        }

#
class ZoneInput(CreateZone):
    class Config:
        fields_to_hide = {"code"}

#
class ZoneUpdate(ZoneInput):
    pass

#
class ZoneItemSchema(ZoneSchema):
    regions: list[RegionSchema] = []
    
#
class ZonePagination(BaseSchema):
    count: int
    total: int
    page_size: int
    start_index: int
    results: List[ZoneSchema] = []