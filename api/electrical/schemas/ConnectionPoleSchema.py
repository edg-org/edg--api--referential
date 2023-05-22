from datetime import datetime, date
from pydantic import BaseModel
from typing import Optional, List
from api.ageographical.schemas.DeliveryPointSchema import DeliveryPointSchema

class PoleCoordinates(BaseModel):
    altitude: float
    latitude: float
    longitude: float

class Transformers(BaseModel):
    electrical_code: int
    activation_dated: date
    desactivation_date: Optional[date]=None
    is_actived: bool
    
class PoleInfos(BaseModel):
    number: int
    name: Optional[str]=None
    area_code: int
    electrical_code: int
    transformer_code: int
    address: str
    transformers: List[Transformers]
    coordinates: Optional[PoleCoordinates]=None
    
class ConnectionPoleUpdate(BaseModel):
    infos: PoleInfos

class ConnectionPoleInput(ConnectionPoleUpdate):
    pass
class ConnectionPoleBase(ConnectionPoleInput):
    area_id: int
    transformer_id: int
    pole_number: str

    class Config:
        orm_mode = True

class CreateConnectionPole(ConnectionPoleBase):
    pass

class ConnectionPoleSchema(ConnectionPoleBase):
    id: int
    is_activated: bool
    created_at: datetime
    updated_at: Optional[datetime]

class ConnectionPoleItemSchema(ConnectionPoleSchema):
    deliverypoints: list[DeliveryPointSchema] = []