from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List

class PaymentMode(BaseModel):
    code: str
    name: str

class SubscriptionLevelBase(BaseModel):
    code: int
    name: str
    payment_mode: List[PaymentMode]

    class Config:
        orm_mode = True

class CreateSubscriptionLevel(SubscriptionLevelBase):
    pass

class SubscriptionLevelSchema(SubscriptionLevelBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]