from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

class AgencySearchParams(BaseModel):
    code: int = Field(description="Field of the agency name")
    name: str | None = Field(description="Field of the agency name")

class AgencyCoordinates(BaseModel):
    altitude: str
    latitude: str
    longitude: str

class AgencyInfos(BaseModel):
    name: str
    email: str
    telephone: str
    address: str
    city_code: int
    coordinates: Optional[AgencyCoordinates]

class AgencyUpdate(BaseModel):
    infos: AgencyInfos

class AgencyInput(AgencyUpdate):
    pass

class AgencyBase(AgencyInput):
    code: int
    city_id: int

    class Config:
        orm_mode = True

class CreateAgency(AgencyBase):
    pass

class AgencySchema(AgencyBase):
    id: int
    is_activated: bool
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]