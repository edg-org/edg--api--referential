from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class ConnectionPointCoordinates(BaseModel):
    altitude: str
    latitude: str
    longitude: str

class ConnectionPointInfos(BaseModel):
    name: str
    address: str
    coordinates: ConnectionPointCoordinates

class ConnectionPointBase(BaseModel):
    connection_point_number: int
    name: Optional[str]
    infos: ConnectionPointInfos
    
    class Config:
        orm_mode = True

class CreateConnectionPoint(ConnectionPointBase):
    pass

class ConnectionPointSchema(ConnectionPointBase):
    id: int
    is_activated: bool
    created_at: datetime
    updated_at: Optional[datetime]