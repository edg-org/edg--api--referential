from pydantic import Field
from datetime import datetime
from typing import List, Optional
from api.configs.BaseModel import BaseSchema
from api.ageographical.schemas.AreaSchema import AreaSchema

#
class CitySearchParams(BaseSchema):
    code: Optional[int] = Field(description="Field of the city code")
    zipcode: Optional[str] = Field(description="Field of the city zipcode")

#
class CityCoordinates(BaseSchema):
    altitude: float
    latitude: float
    longitude: float

#
class CityInfos(BaseSchema):
    name: str
    city_type: str
    city_level: str
    prefecture: str
    coordinates: Optional[CityCoordinates]

#
class CityUpdateInfos(BaseSchema):
    name: str
    city_type: str
    city_level: str
#
class CitySchema(BaseSchema):
    id: int
    code: int
    zipcode: str
    city_type_id: int
    city_level_id: int
    prefecture_id: int
    infos: CityInfos
    is_activated: bool
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    
    class Config:
        orm_mode = True

#
class CreateCity(CitySchema):
    class Config:
        fields_to_hide = {
            "id", 
            "is_activated",
            "created_at",
            "updated_at",
            "deleted_at"
        }

#
class CityInput(CreateCity):
    class Config:
        fields_to_hide = {
            "code",
            "zipcode",
            "city_type_id",
            "city_level_id",
            "prefecture_id"
        }

#
class CityUpdate(BaseSchema):
    infos: CityUpdateInfos

#
class CityItemSchema(CitySchema):
    areas: list[AreaSchema] = []
    
#
class CityPagination(BaseSchema):
    count: int
    total: int
    page_size: int
    start_index: int
    results: List[CitySchema] = []