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


class DeliveryPointBase(BaseModel):
    delivery_point_number: str
    name: Optional[str]
    area_id: Optional[int]
    connection_point_id: Optional[int]
    infos: DeliveryInfos

    class Config:
        orm_mode = True


class CreateDeliveryPoint(DeliveryPointBase):
    pass


class DeliveryPointSchema(DeliveryPointBase):
    id: int
    is_activated: bool
    created_at: datetime
    updated_at: Optional[datetime]
