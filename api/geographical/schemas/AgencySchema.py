from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class AgencyCoordinates(BaseModel):
    altitude: str
    latitude: str
    longitude: str

class AgencyInfos(BaseModel):
    name: str
    email: str
    telephone: str
    address: str
    coordinates: Optional[AgencyCoordinates]

class AgencyBase(BaseModel):
    code: Optional[int]
    area_id: Optional[int]
    type_id: Optional[int]
    infos: AgencyInfos

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