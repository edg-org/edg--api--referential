from pydantic import Field
from typing import Optional
from datetime import datetime
from api.configs.BaseModel import SchemaModel
from api.ageographical.schemas.AreaSchema import AreaSchema

#
class CitySearchParams(SchemaModel):
    code: int | None = Field(description="Field of the city code")
    zipcode: str | None = Field(description="Field of the city zipcode")

#
class CityCoordinates(SchemaModel):
    altitude: float
    latitude: float
    longitude: float

#
class CityInfos(SchemaModel):
    name: str
    city_type: str
    city_level: str
    prefecture: str
    coordinates: Optional[CityCoordinates]

#
class CitySchema(SchemaModel):
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
class CityUpdate(CityInput):
    pass

#
class CityItemSchema(CitySchema):
    areas: list[AreaSchema] = []