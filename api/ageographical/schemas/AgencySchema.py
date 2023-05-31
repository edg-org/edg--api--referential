from typing import Optional
from datetime import datetime
from api.configs.Environment import HideFields
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

#
class AgencySchema(BaseModel):
    id: int
    code: int
    city_id: int
    infos: AgencyInfos
    is_activated: bool
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    
    class Config:
        orm_mode = True

#
class CreateAgency(AgencySchema, metaclass=HideFields):
    class Config:
        fields_hided = {
            "id", 
            "is_activated",
            "created_at",
            "updated_at",
            "deleted_at"
        }    

#
class AgencyInput(CreateAgency, metaclass=HideFields):
    class Config:
        fields_hided = {
            "code", 
            "city_id"
        }

#
class AgencyUpdate(AgencyInput):
    pass