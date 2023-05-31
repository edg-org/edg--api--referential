from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from api.configs.Environment import HideFields

#
class HousingTypeSchema(BaseModel):
    id: int
    code: int
    name: str
    shortname: str
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        orm_mode = True

#
class CreateHousingType(HousingTypeSchema, metaclass=HideFields):
    class Config:
        fields_hided = {
            "id", 
            "created_at",
            "updated_at"
        }

#
class HousingTypeInput(CreateHousingType, metaclass=HideFields):
    class Config:
        fields_hided = {"code"}

#
class HousingTypeUpdate(HousingTypeInput):
    pass