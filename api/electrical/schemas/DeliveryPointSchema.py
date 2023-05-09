from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class DeliveryCoordinates(BaseModel):
    altitude: float
    latitude: float
    longitude: float


class DeliveryInfos(BaseModel):
    name: str
    area_code: int
    connection_point_number: str
    address: str
    coordinates: DeliveryCoordinates

class DeliveryPointUpdate(BaseModel):
    name: Optional[str]
    infos: Optional[DeliveryInfos]

class DeliveryPointInput(DeliveryPointUpdate):
    delivery_point_number: str

class DeliveryPointBase(DeliveryPointInput):
    area_id: int
    connection_point_id: int

    class Config:
        orm_mode = True

class CreateDeliveryPoint(DeliveryPointBase):
    pass

class DeliveryPointSchema(DeliveryPointBase):
    id: int
    is_activated: bool
    created_at: datetime
    updated_at: Optional[datetime]