from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from api.configs.Environment import OmitFields
from api.salesfinancial.schemas.SubscriptionTypeSchema import SubscriptionTypeSchema

class TrackingTypeInput(BaseModel):
    code: int
    name: str

class TrackingTypeUpdate(TrackingTypeInput, metaclass=OmitFields):
    class Config:
        omit_fields = {'code'}
        
class TrackingTypeBase(TrackingTypeInput):
    pass

    class Config:
        orm_mode = True

class CreateTrackingType(TrackingTypeBase):
    pass

class TrackingTypeSchema(TrackingTypeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

class TrackingTypeItemSchema(TrackingTypeSchema):
    sub: list[SubscriptionTypeSchema] = []
