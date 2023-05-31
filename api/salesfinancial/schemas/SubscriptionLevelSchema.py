from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List
from api.configs.Environment import HideFields

#
class PaymentMode(BaseModel):
    code: int
    name: str  

#
class SubscriptionLevelSchema(BaseModel):
    id: int
    code: int
    name: str
    payment_mode: List[PaymentMode]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        orm_mode = True

#
class CreateSubscriptionLevel(SubscriptionLevelSchema, metaclass=HideFields):
    class Config:
        fields_hided = {
            "id", 
            "created_at",
            "updated_at"
        }

#
class SubscriptionLevelInput(CreateSubscriptionLevel, metaclass=HideFields):
    class Config:
        fields_hided = {"code"}

#
class SubscriptionLevelUpdate(SubscriptionLevelInput):
    pass