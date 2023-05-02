from typing import Optional
from pydantic import BaseModel
from datetime import datetime, date

class Infos(BaseModel):
    meter_number: str
    delivery_point_number: int

class MeterDeliveryPointBase(BaseModel):
    meter_id: int
    delivery_point_id: int
    installation_date: date
    infos: Infos
    
    class Config:
        orm_mode = True

class CreateMeterDeliveryPoint(MeterDeliveryPointBase):
    pass

class MeterDeliveryPointSchema(MeterDeliveryPointBase):
    created_at: datetime