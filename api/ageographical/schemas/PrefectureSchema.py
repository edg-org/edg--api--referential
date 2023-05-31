from pydantic import Field
from typing import Optional
from datetime import datetime
from api.configs.BaseModel import SchemaModel
from api.ageographical.schemas.CitySchema import CitySchema

#
class PrefectureSearchParams(SchemaModel):
    code: int = Field(description="Field of the prefecture code")
    name: str | None = Field(description="Field of the prefecture name")

#
class PrefectureCoordinates(SchemaModel):
    altitude: float
    latitude: float
    longitude: float

#
class PrefectureInfos(SchemaModel):
    region: str
    coordinates: Optional[PrefectureCoordinates]
    
#
class PrefectureSchema(SchemaModel):
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
class CreatePrefecture(PrefectureSchema):
    class Config:
        fields_to_hide = {
            'id', 
            'created_at', 
            'updated_at', 
            'deleted_at'
        }

#
class PrefectureInput(PrefectureSchema):
    name: str
    is_capital: bool
    infos: PrefectureInfos
    
    class Config:
        fields_to_hide = {
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