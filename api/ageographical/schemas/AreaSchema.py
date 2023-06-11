from typing import Optional
from pydantic import Field
from datetime import datetime
from api.configs.BaseModel import BaseSchema
from api.ageographical.schemas.AgencySchema import AgencySchema

#
class AreaSearchParams(BaseSchema):
    code: Optional[int] = Field(description="Field of the area code")
    zipcode: Optional[str] = Field(description="Field of the area zipcode")

#
class AreaCoordinates(BaseSchema):
    altitude: float
    latitude: float
    longitude: float

#
class AreaInfos(BaseSchema):
    name: str
    area_type: str  # district, neighborhood, village,  industrial area, administrative area
    city_code: Optional[int]
    is_same_zipcode: bool = False
    agency_code: Optional[int] = None
    hierarchical_area_code: Optional[int] = None
    coordinates: Optional[AreaCoordinates] = None

class AreaUpdateInfos(BaseSchema):
    name: Optional[str]
    area_type: Optional[str]
    city_code: Optional[int]
    is_same_zipcode: bool = False
    agency_code: Optional[int] = None
    hierarchical_area_code: Optional[int] = None
    
#
class AreaSchema(BaseSchema):
    id: int
    code: int
    zipcode: int
    city_id: int
    area_type_id: int
    agency_id: Optional[int] = None
    hierarchical_area_id: Optional[int] = None
    infos: AreaInfos
    is_activated: bool
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    
    class Config:
        orm_mode = True
 
 #       
class CreateArea(AreaSchema):
    class Config:
        fields_to_hide = {
            "id", 
            "is_activated",
            "created_at",
            "updated_at",
            "deleted_at"
        }    

#
class AreaInput(CreateArea):    
    class Config:
        fields_to_hide = {
            "code", 
            "zipcode",
            "city_id",
            "agency_id",
            "area_type_id",
            "hierarchical_area_id"
        }

#
class AreaUpdate(BaseSchema):
    infos: AreaUpdateInfos

#
class AreaItemSchema(AreaSchema):
    agencies: list[AgencySchema] = []