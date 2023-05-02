from pydantic import BaseModel
from datetime import datetime, date

class Infos(BaseModel):
    meter_number: str
    delivery_point_number: int

class SubscriptionDeliveryPointBase(BaseModel):
    contract_number: int
    delivery_point_number: int
    opening_date: date
    closing_date: date
    
    class Config:
        orm_mode = True

class CreateSubscriptionDeliveryPoint(SubscriptionDeliveryPointBase):
    pass

class SubscriptionDeliveryPointSchema(SubscriptionDeliveryPointBase):
    id: int
    created_at: datetime