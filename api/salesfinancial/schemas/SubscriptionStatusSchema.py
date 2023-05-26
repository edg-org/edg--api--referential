from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from api.configs.Environment import HideFields

class SubscriptionStatusInput(BaseModel):
    code: int
    name: str

class SubscriptionStatusUpdate(SubscriptionStatusInput, metaclass=HideFields):
    class Config:
        fields_hided = {'code'}

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