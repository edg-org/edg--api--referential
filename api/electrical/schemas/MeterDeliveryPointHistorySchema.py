from pydantic import BaseModel
from datetime import datetime, date

class MeterDeliveryPointBase(BaseModel):
    meter_number: str
    delivery_point_number: str
    installation_date: date
    uninstallation_date: date

    class Config:
        orm_mode = True


class CreateMeterDeliveryPoint(MeterDeliveryPointBase):
    pass


class MeterDeliveryPointSchema(MeterDeliveryPointBase):
    id: int
    created_at: datetime
