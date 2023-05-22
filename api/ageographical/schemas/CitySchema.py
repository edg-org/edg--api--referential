from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from api.ageographical.schemas.AreaSchema import AreaSchema

class CitySearchParams(BaseModel):
    code: int | None = Field(description="Field of the city code")
    zipcode: str | None = Field(description="Field of the city zipcode")

class CityCoordinates(BaseModel):
    altitude: float
    latitude: float
    longitude: float

class CityInfos(BaseModel):
    name: str
    city_type: str
    city_level: str
    prefecture: str
    coordinates: Optional[CityCoordinates]

class CityUpdate(BaseModel):
    infos: CityInfos

class CityInput(CityUpdate):
    pass

class CityBase(CityInput):
    code: int
    zipcode: str
    city_type_id: int
    city_level_id: int
    prefecture_id: int

    class Config:
        orm_mode = True

class CreateCity(CityBase):
    pass

class CitySchema(CityBase):
    id: int
    is_activated: bool
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]

class CityItemSchema(CitySchema):
    areas: list[AreaSchema] = []