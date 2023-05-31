from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List
from api.configs.BaseModel import SchemaModel

#
class PaymentMode(SchemaModel):
    code: int
    name: str  

#
class SubscriptionLevelSchema(SchemaModel):
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
class SubscriptionLevelUpdate(SubscriptionLevelInput):
    pass