from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List
from api.configs.Environment import HideFields

class PaymentMode(BaseModel):
    code: int
    name: str

class SubscriptionLevelInput(BaseModel):
    code: int
    name: str
    payment_mode: List[PaymentMode]

class SubscriptionLevelUpdate(SubscriptionLevelInput, metaclass=HideFields):
    class Config:
        fields_hided = {'code'}
        
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