from pydantic import Field
from typing import Optional
from datetime import datetime
from api.configs.BaseModel import BaseSchema
from api.ageographical.schemas.AreaSchema import AreaSchema

#
class CitySearchParams(BaseSchema):
    code: int | None = Field(description="Field of the city code")
    zipcode: str | None = Field(description="Field of the city zipcode")

#
class CityCoordinates(BaseSchema):
    altitude: float
    latitude: float
    longitude: float

#
class CityInfos(BaseSchema):
    name: Optional[str]
    city_type: Optional[str]
    city_level: Optional[str]
    prefecture: Optional[str]
    coordinates: Optional[CityCoordinates]

#
class CityUpdateInfos(CityInfos):
    pass
#     name: str
#     city_type: str
#     city_level: str
# #
class CitySchema(BaseSchema):
    id: int
    code: int
    zipcode: str
    city_type_id: int
    city_level_id: int
    prefecture_id: int
    infos: CityInfos
    is_activated: bool
    created_at: Optional[datetime]
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
# {
#    "infos":{
#       "code":1020201,
#       "name":"boké",
#       "city_type":"Commune Urbaine",
#       "city_level":"Préfecture",
#       "prefecture":"boké",
#       "coordinates":{
#          "altitude":0,
#          "latitude":0,
#          "longitude":0
#       }
#    }
# }
#
class CityItemSchema(CitySchema):
    areas: list[AreaSchema] = []