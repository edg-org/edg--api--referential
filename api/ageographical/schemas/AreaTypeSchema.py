from typing import Optional
from datetime import datetime
from api.configs.BaseModel import BaseSchema

class AreaTypeSchema(BaseSchema):
    id: int
    code: int
    name: str
    is_hierarchical : Optional[bool] = False
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    
    class Config:
        orm_mode = True

#
class CreateAreaType(AreaTypeSchema):
    class Config:
        fields_to_hide = {
            "id", 
            "created_at",
            "updated_at"
        }

#
class AreaTypeInput(CreateAreaType):
    class Config:
        fields_to_hide = {"code"}

#
class AreaTypeUpdate(AreaTypeInput):
    pass