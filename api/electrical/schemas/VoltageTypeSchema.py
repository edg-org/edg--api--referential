from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from api.configs.BaseModel import SchemaModel

#
class VoltageTypeInfos(SchemaModel):
    minimum_voltage: float
    maximum_voltage: float
    measurement_unit: str
    
#
class VoltageTypeSchema(SchemaModel):
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
class CreateVoltageType(VoltageTypeSchema):
    class Config:
        fields_to_hide = {
            "id", 
            "created_at",
            "updated_at",
            "deleted_at"
        }

#
class VoltageTypeInput(CreateVoltageType):
    class Config:
        fields_to_hide = {"code"}

#
class VoltageTypeUpdate(VoltageTypeInput):
    pass