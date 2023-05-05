from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from api.ageographical.schemas.PrefectureSchema import (
    PrefectureSchema,
)


class RegionCoordinates(BaseModel):
    altitude: float
    latitude: float
    longitude: float


class RegionInfos(BaseModel):
    zone_code: int
    name: str
    coordinates: Optional[RegionCoordinates]


class RegionBase(BaseModel):
    code: Optional[int]
    zone_id: Optional[int]
    infos: RegionInfos

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
