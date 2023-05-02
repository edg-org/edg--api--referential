from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from api.geographical.schemas.CitySchema import CitySchema

class PrefectureCoordinates(BaseModel):
    altitude: float
    latitude: float
    longitude: float

class PrefectureInfos(BaseModel):
    region_code: int
    name: str
    coordinates: Optional[PrefectureCoordinates]

class PrefectureBase(BaseModel):
    code: Optional[int]
    prefecture_number: Optional[str]
    region_id: Optional[int]
    is_capital: bool
    infos: PrefectureInfos

    class Config:
        orm_mode = True

class CreatePrefecture(PrefectureBase):
    pass

class PrefectureSchema(PrefectureBase):
    id: int
    is_activated: bool
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

class PrefectureItemSchema(PrefectureSchema):
    cities : list[CitySchema] = []