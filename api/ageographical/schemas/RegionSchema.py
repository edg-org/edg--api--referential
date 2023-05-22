from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from api.ageographical.schemas.PrefectureSchema import PrefectureSchema


class RegionCoordinates(BaseModel):
    altitude: float
    latitude: float
    longitude: float

class RegionSearchParams(BaseModel):
    code: int = Field(description="Field of the region code")
    name: str | None = Field(description="Field of the region name")

class RegionInfos(BaseModel):
    natural_zone: str
    coordinates: Optional[RegionCoordinates]

class RegionUpdate(BaseModel):
    name: str
    infos: RegionInfos

class RegionInput(RegionUpdate):
    pass

class RegionBase(RegionInput):
    code: int
    zone_id: int

    class Config:
        orm_mode = True

class CreateRegion(RegionBase):
    pass

class RegionSchema(RegionBase):
    id: int
    is_activated: bool
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

class RegionItemSchema(RegionSchema):
    prefectures: list[PrefectureSchema] = []