from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from api.salesfinancial.schemas.SubscriptionTypeSchema import SubscriptionTypeSchema

class TrackingTypeUpdate(BaseModel):
    name: str

class TrackingTypeInput(TrackingTypeUpdate):
    code: int

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
