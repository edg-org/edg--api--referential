from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class ElectricMeterInfos(BaseModel):
    brand: str
    meter_type: str
    supply_mode: str
    index_reading: float
    manufacturing_country: str

class ElectricMeterUpdate(BaseModel):
    infos: ElectricMeterInfos

class ElectricMeterInput(ElectricMeterUpdate):
    meter_number: str

class ElectricMeterBase(ElectricMeterInput):
    meter_type_id: int
    supply_mode_id: int

    class Config:
        orm_mode = True

class CreateElectricMeter(ElectricMeterBase):
    pass

class ElectricMeterSchema(ElectricMeterBase):
    id: int
    is_activated: bool
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]