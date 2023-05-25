from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List
from api.configs.Environment import OmitFields

class PaymentMode(BaseModel):
    code: int
    name: str

class SubscriptionLevelInput(BaseModel):
    code: int
    name: str
    payment_mode: List[PaymentMode]

class SubscriptionLevelUpdate(SubscriptionLevelInput, metaclass=OmitFields):
    class Config:
        omit_fields = {'code'}
        
class SubscriptionLevelBase(SubscriptionLevelInput):
    pass

    class Config:
        orm_mode = True

class CreateSubscriptionLevel(SubscriptionLevelBase):
    pass

class SubscriptionLevelSchema(SubscriptionLevelBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]