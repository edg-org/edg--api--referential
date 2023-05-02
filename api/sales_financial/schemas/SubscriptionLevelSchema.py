from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class PaymentMode(BaseModel):
    code: int
    name: str

class SubscriptionLevelBase(BaseModel):
    code: int
    name: str
    payment_mode: PaymentMode

    class Config:
        orm_mode = True

class CreateSubscriptionLevel(SubscriptionLevelBase):
    pass

class SubscriptionLevelSchema(SubscriptionLevelBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]