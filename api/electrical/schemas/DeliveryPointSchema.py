from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class DeliveryPointCoordinates(BaseModel):
    altitude: str
    latitude: str
    longitude: str

class DeliveryPointInfos(BaseModel):
    name: str
    address: str
    coordinates: DeliveryPointCoordinates

class DeliveryPointBase(BaseModel):
    delivery_point_number: int
    name: Optional[str]
    infos: DeliveryPointInfos
    
    class Config:
        orm_mode = True

class CreateDeliveryPoint(DeliveryPointBase):
    pass

class DeliveryPointSchema(DeliveryPointBase):
    id: int
    is_activated: bool
    created_at: datetime
    updated_at: Optional[datetime]