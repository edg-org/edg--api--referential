from typing import Optional
from pydantic import BaseModel
from datetime import datetime, date

class MeterDeliveryPointInput(BaseModel):
    meter_number: str
    delivery_point_number: str
    installation_date: date

class MeterDeliveryPointBase(MeterDeliveryPointInput):
    pass

    class Config:
        orm_mode = True

class CreateMeterDeliveryPoint(MeterDeliveryPointBase):
    pass

class MeterDeliveryPointSchema(MeterDeliveryPointBase):
    created_at: datetime