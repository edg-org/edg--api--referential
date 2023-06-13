from typing import Optional
from datetime import datetime
from pydantic import EmailStr, Field, constr
from api.configs.BaseModel import BaseSchema

class AgencySearchParams(BaseSchema):
    code: int | None = Field(description="Field of the agency name")
    name: str | None = Field(description="Field of the agency name")

class AgencyCoordinates(BaseSchema):
    altitude: float
    latitude: float
    longitude: float

class AgencyInfos(BaseSchema):
    name: str
    email: EmailStr
    telephone: constr(regex=r'^\+224-\d{3}-\d{2}-\d{2}-\d{2}$')
    address: str
    city_code: int
    coordinates: Optional[AgencyCoordinates]

class AgencyUpdateInfos(AgencyInfos):
    pass
    # class Config:
    #     fields_to_hide = {
    #         "city_code",
    #         # "coordinates"
    #     }

#
# {
#   "id": 14,
#   "code": 102020110,
#   "city_id": 1,
#   "infos": {
#     "name": "Agence Kankan 1",
#     "email": "kankan1@edg.gn.com",
#     "telephone": "+224-630-34-56-78",
#     "address": "quartier korialen",
#     "city_code": 1020201,
#     "coordinates": null
#   },
#   "is_activated": true,
#   "created_at": "2023-06-07T14:18:10",
#   "updated_at": null,
#   "deleted_at": null
# }


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
