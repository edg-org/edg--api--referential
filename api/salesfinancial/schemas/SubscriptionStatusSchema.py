from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class SubscriptionStatusUpdate(BaseModel):
    name: str

class SubscriptionStatusInput(SubscriptionStatusUpdate):
    code: int

class SubscriptionStatusBase(SubscriptionStatusInput):
    pass
    
    class Config:
        orm_mode = True

class CreateSubscriptionStatus(SubscriptionStatusBase):
    pass

class SubscriptionStatusSchema(SubscriptionStatusBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]