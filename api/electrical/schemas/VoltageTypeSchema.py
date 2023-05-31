from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from api.configs.Environment import HideFields

#
class VoltageTypeInfos(BaseModel):
    minimum_voltage: float
    maximum_voltage: float
    measurement_unit: str
    
#
class VoltageTypeSchema(BaseModel):
    id: int
    code: int
    name: str
    shortname: str
    infos: VoltageTypeInfos
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    
    class Config:
        orm_mode = True

#
class CreateVoltageType(VoltageTypeSchema, metaclass=HideFields):
    class Config:
        fields_hided = {
            "id", 
            "created_at",
            "updated_at",
            "deleted_at"
        }

#
class VoltageTypeInput(CreateVoltageType, metaclass=HideFields):
    class Config:
        fields_hided = {"code"}

#
class VoltageTypeUpdate(VoltageTypeInput):
    pass