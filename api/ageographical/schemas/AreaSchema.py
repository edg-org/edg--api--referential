from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from api.ageographical.schemas.AgencySchema import AgencySchema

class AreaSearchParams(BaseModel):
    code: int = Field(description="Field of the area code")
    zipcode: str | None = Field(description="Field of the area zipcode")
    name: str | None = Field(description="Field of the area name")

class AreaCoordinates(BaseModel):
    altitude: float
    latitude: float
    longitude: float


class AreaInfos(BaseModel):
    name: str
    area_type: str  # neighborhood, district, village,  industrial area, administrative area
    city_code: int
    on_city_zipcode: bool = False
    agency_code: Optional[int] = None
    coordinates: Optional[AreaCoordinates] = None

class AreaUpdate(BaseModel):
    infos: AreaInfos

class AreaInput(AreaUpdate):
    pass

class AreaBase(AreaInput):
    code: int
    zipcode: int
    city_id: int
    area_type_id: int
    agency_id: Optional[int] = None

    class Config:
        orm_mode = True

class CreateArea(AreaBase):
    pass


class AreaSchema(AreaBase):
    id: int
    is_activated: bool
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]


class AreaItemSchema(AreaSchema):
    agencies: list[AgencySchema] = []
