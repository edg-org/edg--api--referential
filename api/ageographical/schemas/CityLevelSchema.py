from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from api.configs.BaseModel import SchemaModel

#
class CityLevelSchema(SchemaModel):
    id: int
    code: int
    name: str
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    
    class Config:
        orm_mode = True

#
class CreateCityLevel(CityLevelSchema):
    class Config:
        fields_to_hide = {
            "id", 
            "created_at",
            "updated_at",
            "deleted_at"
        }

#
class CityLevelInput(CreateCityLevel):
    class Config:
        fields_to_hide = {"code"}

#
class CityLevelUpdate(CityLevelInput):
    pass