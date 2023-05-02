from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class SubscriptionStatusBase(BaseModel):
    code: int
    name: str
    
    class Config:
        orm_mode = True

class CreateSubscriptionStatus(SubscriptionStatusBase):
    pass

class SubscriptionStatusSchema(SubscriptionStatusBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]