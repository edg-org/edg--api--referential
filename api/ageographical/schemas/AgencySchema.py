from typing import Optional
from datetime import datetime
from pydantic import EmailStr, Field, constr
from api.configs.BaseModel import SchemaModel

class AgencySearchParams(SchemaModel):
    code: int | None = Field(description="Field of the agency name")
    name: str | None = Field(description="Field of the agency name")

class AgencyCoordinates(SchemaModel):
    altitude: str
    latitude: str
    longitude: str

class AgencyInfos(SchemaModel):
    name: str
    email: EmailStr
    telephone: constr(regex=r'^\+224-\d{3}-\d{2}-\d{2}-\d{2}$')
    address: str
    city_code: int
    coordinates: Optional[AgencyCoordinates]

#
class AgencySchema(SchemaModel):
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
class CreateAgency(AgencySchema):
    class Config:
        fields_to_hide = {
            "id", 
            "is_activated",
            "created_at",
            "updated_at",
            "deleted_at"
        }    

#
class AgencyInput(CreateAgency):
    class Config:
        fields_to_hide = {
            "code", 
            "city_id"
        }

#
class AgencyUpdate(AgencyInput):
    pass