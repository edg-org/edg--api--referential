from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List, Dict

class DeliveryCoordinates(BaseModel):
    altitude: float
    latitude: float
    longitude: float

class DeliveryInfos(BaseModel):
    number: int
    area_code: int
    electrical_code: int
    pole_number: int
    address: str
    coordinates: Optional[DeliveryCoordinates]

class ConnectionPole(BaseModel):
    electrical_code: int
    activation_date: date
    desactivation_date: Optional[date]=None
    is_actived: bool
    
class DeliveryPointUpdate(BaseModel):
    infos: DeliveryInfos
    connection_poles: List[ConnectionPole]

class DeliveryPointInput(DeliveryPointUpdate):
    pass

class DeliveryPointBase(DeliveryPointInput):
    delivery_point_number: int
    area_id: int
    pole_id: int

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