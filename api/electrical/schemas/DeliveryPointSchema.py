from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class DeliveryCoordinates(BaseModel):
    altitude: float
    latitude: float
    longitude: float

class DeliveryInfos(BaseModel):
    name: Optional[str]
    area_code: int
    address: str
    coordinates: Optional[DeliveryCoordinates]

class DeliveryPointUpdate(BaseModel):
    infos: DeliveryInfos

class DeliveryPointInput(DeliveryPointUpdate):
    pass

class DeliveryPointBase(DeliveryPointInput):
    delivery_point_number: str
    area_id: int

    class Config:
        orm_mode = True

class CreateDeliveryPoint(DeliveryPointBase):
    pass

class DeliveryPointSchema(DeliveryPointBase):
    id: int
    is_activated: bool
    created_at: datetime
    updated_at: Optional[datetime]