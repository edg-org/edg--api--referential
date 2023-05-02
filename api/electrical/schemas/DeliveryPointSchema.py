from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class DeliveryCoordinates(BaseModel):
    altitude: float
    latitude: float
    longitude: float


class DeliveryInfos(BaseModel):
    name: str
    address: str
    coordinates: DeliveryCoordinates


class DeliveryPointBase(BaseModel):
    delivery_point_number: str
    name: Optional[str]
    area_id: int
    connection_point_id: int
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
