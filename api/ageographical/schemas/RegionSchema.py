from pydantic import Field
from typing import Optional
from datetime import datetime
from api.configs.BaseModel import BaseSchema
from api.ageographical.schemas.PrefectureSchema import PrefectureSchema

#
class RegionSearchParams(BaseSchema):
    code: int = Field(description="Field of the region code")
    name: str | None = Field(description="Field of the region name")

#
class RegionCoordinates(BaseSchema):
    altitude: float
    latitude: float
    longitude: float

#
class RegionInfos(BaseSchema):
    natural_zone: str
    coordinates: Optional[RegionCoordinates]

#  
class RegionSchema(BaseSchema):
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
class CreateRegion(RegionSchema):
    class Config:
        fields_to_hide = {
            'id', 
            'is_activated', 
            'created_at', 
            'updated_at', 
            'deleted_at'
        }

#
class RegionInput(CreateRegion):
    class Config:
        fields_to_hide = {
            'code', 
            'zone_id'
        }

#
class RegionUpdate(RegionInput):
    pass
#
class RegionItemSchema(RegionSchema):
    prefectures: list[PrefectureSchema] = []