from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, constr

class AgencySearchParams(BaseModel):
    code: int | None = Field(description="Field of the agency name")
    name: str | None = Field(description="Field of the agency name")

class AgencyCoordinates(BaseModel):
    altitude: str
    latitude: str
    longitude: str

class AgencyInfos(BaseModel):
    name: str
    email: EmailStr
    telephone: constr(regex=r'^\+224-\d{3}-\d{2}-\d{2}-\d{2}$')
    address: str
    city_code: int
    coordinates: Optional[AgencyCoordinates]

class AgencyInput(BaseModel):
    infos: AgencyInfos

class AgencyUpdate(AgencyInput):
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