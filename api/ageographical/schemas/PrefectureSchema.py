from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from api.configs.Environment import HideFields
from api.ageographical.schemas.CitySchema import CitySchema

#
class PrefectureSearchParams(BaseModel):
    code: int = Field(description="Field of the prefecture code")
    name: str | None = Field(description="Field of the prefecture name")

#
class PrefectureCoordinates(BaseModel):
    altitude: float
    latitude: float
    longitude: float

#
class PrefectureInfos(BaseModel):
    region: str
    coordinates: Optional[PrefectureCoordinates]
    
#
class PrefectureSchema(BaseModel):
    id: int
    name: str
    is_capital: bool
    code: int
    region_id: int
    prefecture_number: str
    infos: PrefectureInfos
    is_activated: bool
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

    class Config:
        orm_mode = True

#
class CreatePrefecture(PrefectureSchema, metaclass=HideFields):
    class Config:
        fields_hided = {
            'id', 
            'created_at', 
            'updated_at', 
            'deleted_at'
        }

#
class PrefectureInput(PrefectureSchema, metaclass=HideFields):
    name: str
    is_capital: bool
    infos: PrefectureInfos
    
    class Config:
        fields_hided = {
            'code', 
            'prefecture_number', 
            'region_id'
        }

#
class PrefectureUpdate(PrefectureInput):
    pass

#
class PrefectureItemSchema(PrefectureSchema):
    cities: list[CitySchema] = []