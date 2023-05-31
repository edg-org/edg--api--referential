from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from api.configs.BaseModel import SchemaModel
from api.salesfinancial.schemas.SubscriptionTypeSchema import SubscriptionTypeSchema

#
class TrackingTypeSchema(SchemaModel):
    id: int
    code: int
    name: str
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        orm_mode = True

#
class CreateTrackingType(TrackingTypeSchema):
    class Config:
        fields_to_hide = {
            "id", 
            "created_at",
            "updated_at"
        }

#
class TrackingTypeInput(CreateTrackingType):
    class Config:
        fields_to_hide = {"code"}

#
class TrackingTypeUpdate(TrackingTypeInput):
    pass

#
class TrackingTypeItemSchema(TrackingTypeSchema):
    sub: list[SubscriptionTypeSchema] = []
