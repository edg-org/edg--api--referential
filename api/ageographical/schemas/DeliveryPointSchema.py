from datetime import datetime
from pydantic import BaseModel
from typing import Optional, Dict

class DeliveryCoordinates(BaseModel):
    altitude: float
    latitude: float
    longitude: float

class DeliveryInfos(BaseModel):
    number: int
    area_code: int
    connection_point_number: int
    address: str
    coordinates: Optional[DeliveryCoordinates]

class DeliveryPointUpdate(BaseModel):
    infos: DeliveryInfos

class DeliveryPointInput(DeliveryPointUpdate):
    pass

class DeliveryPointBase(DeliveryPointInput):
    delivery_point_number: int
    area_id: int
    connection_point_id: int

    class Config:
        orm_mode = True

class CreateDeliveryPoint(DeliveryPointBase):
    pass

class DeliveryPointSchema(DeliveryPointBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

class DeliveryPointDetails(DeliveryPointInput):
    delivery_point_number: int
    details: Dict