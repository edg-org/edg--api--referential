from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class MeterInfos(BaseModel):
    factory_name: str
    index_reading: float
    manufacturing_country: str

class ElectricMeterBase(BaseModel):
    code: int
    name: str
    infos: MeterInfos
    
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