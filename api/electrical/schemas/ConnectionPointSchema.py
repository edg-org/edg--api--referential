from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from api.electrical.schemas.DeliveryPointSchema import DeliveryPointSchema

class ConnectionCoordinates(BaseModel):
    altitude: float
    latitude: float
    longitude: float


class ConnectionInfos(BaseModel):
    name: str
    area_code: int
    transformer_number: str
    address: str
    coordinates: ConnectionCoordinates


class ConnectionPointBase(BaseModel):
    connection_point_number: str
    name: Optional[str]
    transformer_id: Optional[int]
    area_id: Optional[int]
    infos: ConnectionInfos

    class Config:
        orm_mode = True


class CreateConnectionPoint(ConnectionPointBase):
    pass


class ConnectionPointSchema(ConnectionPointBase):
    id: int
    is_activated: bool
    created_at: datetime
    updated_at: Optional[datetime]


class ConnectionPointItemSchema(ConnectionPointSchema):
    tranformers: list[DeliveryPointSchema] = []
