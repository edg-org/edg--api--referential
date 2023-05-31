from datetime import datetime, date
from api.configs.BaseModel import SchemaModel

class MeterDeliveryPointInput(SchemaModel):
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