from typing import Optional
from datetime import datetime
from api.configs.BaseModel import SchemaModel

#
class MeterTypeSchema(SchemaModel):
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
    class Config:
        fields_to_hide = {"code"}

#
class MeterTypeUpdate(MeterTypeInput):
    pass