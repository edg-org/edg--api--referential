from typing import Optional
from datetime import datetime
from api.configs.BaseModel import BaseSchema

#
class MeterTypeSchema(BaseSchema):
    id: int
    code: int
    name: str
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        orm_mode = True

#
class CreateMeterType(MeterTypeSchema):
    class Config:
        fields_to_hide = {
            "id", 
            "created_at",
            "updated_at"
        }

#
class MeterTypeInput(CreateMeterType):
    pass

#
class MeterTypeUpdate(MeterTypeInput):
    class Config:
        fields_to_hide = {"code"}