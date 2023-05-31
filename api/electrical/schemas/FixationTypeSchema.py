from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from api.configs.BaseModel import SchemaModel

#
class FixationTypeSchema(SchemaModel):
    id: int
    code: int
    name: str
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        orm_mode = True

#
class CreateFixationType(FixationTypeSchema):
    class Config:
        fields_to_hide = {
            "id", 
            "created_at",
            "updated_at"
        }

#
class FixationTypeInput(CreateFixationType):
    class Config:
        fields_to_hide = {"code"}

#
class FixationTypeUpdate(FixationTypeInput):
    pass