from pydantic import BaseModel
from datetime import datetime, date

class MeterHistoryInput(BaseModel):
    meter_number: str
    delivery_point_number: str
    installation_date: date
    uninstallation_date: date

class MeterHistoryBase(MeterHistoryInput):
    pass

    class Config:
        orm_mode = True

class CreateMeterHistory(MeterHistoryBase):
    pass

class MeterHistorySchema(MeterHistoryBase):
    id: int
    created_at: datetime