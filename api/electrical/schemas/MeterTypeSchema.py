from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from api.configs.Environment import HideFields

#
class MeterTypeSchema(BaseModel):
    id: int
    code: int
    name: str
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        orm_mode = True

#
class CreateMeterType(MeterTypeSchema, metaclass=HideFields):
    class Config:
        fields_hided = {
            "id", 
            "created_at",
            "updated_at"
        }

#
class MeterTypeInput(CreateMeterType, metaclass=HideFields):
    class Config:
        fields_hided = {"code"}

#
class MeterTypeUpdate(MeterTypeInput):
    pass