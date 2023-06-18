from typing import Optional
from datetime import datetime
from api.configs.BaseModel import BaseSchema

#
class SubscriptionStatusSchema(BaseSchema):
    id: int
    code: int
    name: str
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        orm_mode = True

#
class CreateSubscriptionStatus(SubscriptionStatusSchema):
    class Config:
        fields_to_hide = {
            "id", 
            "created_at",
            "updated_at"
        }

#
class SubscriptionStatusInput(CreateSubscriptionStatus):
    pass

#
class SubscriptionStatusUpdate(SubscriptionStatusInput):
    class Config:
        fields_to_hide = {"code"}