from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from api.configs.Environment import HideFields
from api.ageographical.schemas.PrefectureSchema import PrefectureSchema

#
class RegionSearchParams(BaseModel):
    code: int = Field(description="Field of the region code")
    name: str | None = Field(description="Field of the region name")

#
class RegionCoordinates(BaseModel):
    altitude: float
    latitude: float
    longitude: float

#
class RegionInfos(BaseModel):
    natural_zone: str
    coordinates: Optional[RegionCoordinates]

#  
class RegionSchema(BaseModel):
    id: int
    name: str
    code: int
    zone_id: int
    infos: RegionInfos
    is_activated: bool
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    
    class Config:
        orm_mode = True

#
class CreateRegion(RegionSchema, metaclass=HideFields):
    class Config:
        fields_hided = {
            'id', 
            'is_activated', 
            'created_at', 
            'updated_at', 
            'deleted_at'
        }

#
class RegionInput(CreateRegion, metaclass=HideFields):
    class Config:
        fields_hided = {
            'code', 
            'zone_id'
        }

#
class RegionUpdate(RegionInput):
    pass
#
class RegionItemSchema(RegionSchema):
    prefectures: list[PrefectureSchema] = []