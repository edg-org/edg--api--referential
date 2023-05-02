from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from api.sales.schemas.SubscriptionTypeSchema import SubscriptionTypeSchema

class TrackingTypeBase(BaseModel):
    code: int
    name: str
    
    class Config:
        orm_mode = True

class CreateTrackingType(TrackingTypeBase):
    pass

class TrackingTypeSchema(TrackingTypeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]


class TrackingTypeItemSchema(TrackingTypeSchema):
    sub : list[SubscriptionTypeSchema] = []