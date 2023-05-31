from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from api.configs.Environment import HideFields

#
class CityTypeSchema(BaseModel):
    id: int
    code: int
    name: str
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    
    class Config:
        orm_mode = True

#
class CreateCityType(CityTypeSchema, metaclass=HideFields):
    class Config:
        fields_hided = {
            "id", 
            "created_at",
            "updated_at",
            "deleted_at"
        }

#
class CityTypeInput(CreateCityType, metaclass=HideFields):
    class Config:
        fields_hided = {"code"}

#
class CityTypeUpdate(CityTypeInput):
    pass