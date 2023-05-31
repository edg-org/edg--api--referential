from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from api.configs.Environment import HideFields
from api.salesfinancial.schemas.SubscriptionTypeSchema import SubscriptionTypeSchema

#
class TrackingTypeSchema(BaseModel):
    id: int
    code: int
    name: str
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        orm_mode = True

#
class CreateTrackingType(TrackingTypeSchema, metaclass=HideFields):
    class Config:
        fields_hided = {
            "id", 
            "created_at",
            "updated_at"
        }

#
class TrackingTypeInput(CreateTrackingType, metaclass=HideFields):
    class Config:
        fields_hided = {"code"}

#
class TrackingTypeUpdate(TrackingTypeInput):
    pass

#
class TrackingTypeItemSchema(TrackingTypeSchema):
    sub: list[SubscriptionTypeSchema] = []
