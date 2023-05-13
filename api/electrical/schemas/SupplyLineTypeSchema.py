from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class SupplyLineTypeInfos(BaseModel):
    minimum_power: int
    maximum_power: int
    measurement_unit: str
    color: str

class SupplyLineTypeUpdate(BaseModel):
    name: str
    infos: SupplyLineTypeInfos

class SupplyLineTypeInput(SupplyLineTypeUpdate):
    code: int

class SupplyLineTypeBase(SupplyLineTypeInput):
    pass

    class Config:
        orm_mode = True

class CreateSupplyLineType(SupplyLineTypeBase):
    pass

class SupplyLineTypeSchema(SupplyLineTypeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]