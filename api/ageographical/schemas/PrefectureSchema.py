from pydantic import Field
from typing import Optional
from datetime import datetime
from api.configs.BaseModel import BaseSchema
from api.ageographical.schemas.CitySchema import CitySchema

class PrefectureSearchParams(BaseSchema):
    code: int = Field(description="Field of the prefecture code")
    name: str | None = Field(description="Field of the prefecture name")

class PrefectureCoordinates(BaseSchema):
    altitude: float
    latitude: float
    longitude: float

class PrefectureInfos(BaseSchema):
    region: str
    coordinates: Optional[PrefectureCoordinates]
    
class PrefectureUpdateInfos(BaseSchema):
    region: str

class PrefectureSchema(BaseSchema):
    id: Optional[int]
    name: Optional[str]
    is_capital: Optional[bool]
    code: Optional[int]
    region_id: Optional[int]
    prefecture_number: Optional[str]
    infos: Optional[PrefectureInfos]
    is_activated: Optional[bool]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    class Config:
        orm_mode = True

#
class CreatePrefecture(PrefectureSchema):
    class Config:
        fields_to_hide = {
            'id', 
            'is_activated', 
            'created_at', 
            'updated_at', 
            'deleted_at'
        }

#
class PrefectureInput(CreatePrefecture):
    class Config:
        fields_to_hide = {
            'code', 
            'prefecture_number', 
            'region_id'
        }

#
class PrefectureUpdate(BaseSchema):
    name: Optional[str]
    is_capital: Optional[bool]
    infos: Optional[PrefectureUpdateInfos]

#
class PrefectureItemSchema(PrefectureSchema):
    cities: list[CitySchema] = []