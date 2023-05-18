from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List
from api.ageographical.schemas.DeliveryPointSchema import DeliveryPointSchema

class ConnectionCoordinates(BaseModel):
    altitude: float
    latitude: float
    longitude: float

class Transformers(BaseModel):
    code: int
    is_active: bool
    
class ConnectionInfos(BaseModel):
    number: int
    name: Optional[str]=None
    area_code: int
    transformer_code: int
    address: str
    transformers: List[Transformers]
    coordinates: Optional[ConnectionCoordinates]=None
    
class ConnectionPointUpdate(BaseModel):
    infos: ConnectionInfos

class ConnectionPointInput(ConnectionPointUpdate):
    pass
class ConnectionPointBase(ConnectionPointInput):
    area_id: int
    transformer_id: int
    connection_point_number: str

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