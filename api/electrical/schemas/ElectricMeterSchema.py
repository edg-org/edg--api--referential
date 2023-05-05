from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class ElectricMeterInfos(BaseModel):
    name: Optional[str]
    meter_type: str
    power_mode: str
    factory_name: str
    index_reading: float
    manufacturing_country: str


class ElectricMeterBase(BaseModel):
    meter_number: str
    type_id: Optional[int]
    power_mode_id: Optional[int]
    infos: ElectricMeterInfos

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
