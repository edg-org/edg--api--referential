from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from api.electrical.schemas.DeliveryPointSchema import (
    DeliveryPointSchema,
)


class ConnectionCoordinates(BaseModel):
    altitude: float
    latitude: float
    longitude: float


class ConnectionInfos(BaseModel):
    name: str
    address: str
    coordinates: ConnectionCoordinates


class ConnectionPointBase(BaseModel):
    code: str
    connection_point_number: str
    # name: Optional[str]
    transformer_id: int
    area_id: int
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
