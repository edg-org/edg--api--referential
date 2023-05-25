from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from api.configs.Environment import OmitFields

class VoltageTypeInfos(BaseModel):
    minimum_voltage: float
    maximum_voltage: float
    measurement_unit: str

class VoltageTypeInput(BaseModel):
    code: int
    name: str
    shortname: str
    infos: VoltageTypeInfos

class VoltageTypeUpdate(VoltageTypeInput, metaclass=OmitFields):
    class Config:
        omit_fields = {'code'}

class VoltageTypeBase(VoltageTypeInput):
    pass

    class Config:
        orm_mode = True

class CreateVoltageType(VoltageTypeBase):
    pass

class VoltageTypeSchema(VoltageTypeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]