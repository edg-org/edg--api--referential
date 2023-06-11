from typing import Optional
from datetime import datetime
from api.configs.BaseModel import BaseSchema

#
class HousingTypeSchema(BaseSchema):
    id: int
    code: int
    name: str
    shortname: str
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        orm_mode = True

#
class CreateHousingType(HousingTypeSchema):
    class Config:
        fields_to_hide = {
            "id", 
            "created_at",
            "updated_at"
        }

#
class HousingTypeInput(CreateHousingType):
    pass

#
class HousingTypeUpdate(HousingTypeInput):
    class Config:
        fields_to_hide = {"code"}