from datetime import datetime
from typing import List, Optional
from pydantic import EmailStr, Field, constr
from api.configs.BaseModel import BaseSchema

class AgencySearchParams(BaseSchema):
    code: Optional[int] = Field(description="Field of the agency name")
    name: Optional[str] = Field(description="Field of the agency name")

class AgencyCoordinates(BaseSchema):
    altitude: str
    latitude: str
    longitude: str

class AgencyInfos(BaseSchema):
    name: str
    email: EmailStr
    telephone: constr(regex=r'^\+224-\d{3}-\d{2}-\d{2}-\d{2}$')
    address: str
    city_code: int
    coordinates: Optional[AgencyCoordinates]

class AgencyUpdateInfos(AgencyInfos):
    class Config:
        fields_to_hide = {
            "city_code",
            "coordinates"
        }
    
#
class AgencySchema(BaseSchema):
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
class AgencyUpdate(BaseSchema):
    infos: AgencyUpdateInfos
    
#
class AgencyPagination(BaseSchema):
    count: int
    total: int
    page_size: int
    start_index: int
    results: List[AgencySchema] = []