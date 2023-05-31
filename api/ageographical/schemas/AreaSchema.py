from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from api.configs.Environment import HideFields
from api.ageographical.schemas.AgencySchema import AgencySchema

#
class AreaSearchParams(BaseModel):
    code: int | None = Field(description="Field of the area code")
    zipcode: str | None = Field(description="Field of the area zipcode")

#
class AreaCoordinates(BaseModel):
    altitude: float
    latitude: float
    longitude: float

#
class AreaInfos(BaseModel):
    name: str
    area_type: str  # district, neighborhood, village,  industrial area, administrative area
    city_code: Optional[int]
    is_same_zipcode: bool = False
    agency_code: Optional[int] = None
    hierarchical_area_code: Optional[int] = None
    coordinates: Optional[AreaCoordinates] = None

#
class AreaSchema(BaseModel):
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
class CreateArea(AreaSchema, metaclass=HideFields):
    class Config:
        fields_hided = {
            "id", 
            "is_activated",
            "created_at",
            "updated_at",
            "deleted_at"
        }    

#
class AreaInput(AreaSchema, metaclass=HideFields):    
    class Config:
        fields_hided = {
            "code", 
            "zipcode",
            "city_type_id",
            "city_level_id",
            "prefecture_id"
        }

#
class AreaUpdate(AreaInput):
    pass

#
class AreaItemSchema(AreaSchema):
    agencies: list[AgencySchema] = []