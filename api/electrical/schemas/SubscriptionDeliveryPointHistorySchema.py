from pydantic import BaseModel
from datetime import datetime, date

class SubscriptionHistoryInput(BaseModel):
    contract_number: str
    delivery_point_number: str
    opening_date: date
    closing_date: date

class SubscriptionHistoryBase(SubscriptionHistoryInput):
    pass

    class Config:
        orm_mode = True

class CreateSubscriptionHistory(SubscriptionHistoryBase):
    pass

class SubscriptionHistorySchema(SubscriptionHistoryBase):
    id: int
    created_at: datetime
