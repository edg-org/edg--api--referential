from datetime import datetime
from typing import Optional, List
from api.configs.BaseModel import BaseSchema

#
class PaymentMode(BaseSchema):
    code: int
    name: str  

#
class SubscriptionLevelSchema(BaseSchema):
    id: int
    code: int
    name: str
    payment_mode: List[PaymentMode]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        orm_mode = True

#
class CreateSubscriptionLevel(SubscriptionLevelSchema):
    class Config:
        fields_to_hide = {
            "id", 
            "created_at",
            "updated_at"
        }

#
class SubscriptionLevelInput(CreateSubscriptionLevel):
    class Config:
        fields_to_hide = {"code"}

#
class SubscriptionLevelUpdate(CreateSubscriptionLevel):
    pass