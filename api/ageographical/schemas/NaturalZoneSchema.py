from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from api.configs.Environment import HideFields
from api.ageographical.schemas.RegionSchema import RegionSchema

#
class ZoneSearchParams(BaseModel):
    code: int = Field(description="Field of the natural region code")
    name: str | None = Field(description="Field of the natural region name")

#
class ZoneCoordinates(BaseModel):
    altitude: float
    latitude: float
    longitude: float

#
class ZoneSchema(BaseModel):
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
class CreateZone(ZoneSchema, metaclass=HideFields):
    class Config:
        fields_hided = {
            "id",
            "is_activated",
            "created_at",
            "updated_at",
            "deleted_at",
        }

#
class ZoneInput(CreateZone, metaclass=HideFields):
    class Config:
        fields_hided = {"code"}

#
class ZoneUpdate(ZoneInput):
    pass

#
class ZoneItemSchema(ZoneSchema):
    regions: list[RegionSchema] = []