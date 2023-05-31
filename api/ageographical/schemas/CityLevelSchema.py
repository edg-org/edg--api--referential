from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from api.configs.Environment import HideFields

#
class CityLevelSchema(BaseModel):
    id: int
    code: int
    name: str
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    
    class Config:
        orm_mode = True

#
class CreateCityLevel(CityLevelSchema, metaclass=HideFields):
    class Config:
        fields_hided = {
            "id", 
            "created_at",
            "updated_at",
            "deleted_at"
        }

#
class CityLevelInput(CreateCityLevel, metaclass=HideFields):
    class Config:
        fields_hided = {"code"}

#
class CityLevelUpdate(CityLevelInput):
    pass