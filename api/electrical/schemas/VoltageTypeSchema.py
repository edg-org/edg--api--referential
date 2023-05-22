from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class VoltageTypeInfos(BaseModel):
    minimum_voltage: float
    maximum_voltage: float
    measurement_unit: str

class VoltageTypeUpdate(BaseModel):
    name: str
    shortname: str
    infos: VoltageTypeInfos

class VoltageTypeInput(VoltageTypeUpdate):
    code: int

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