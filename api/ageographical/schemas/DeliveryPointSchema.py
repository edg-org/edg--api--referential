from datetime import date, datetime
from typing import Optional, List, Dict
from api.configs.BaseModel import BaseSchema

class DeliveryCoordinates(BaseSchema):
    altitude: float
    latitude: float
    longitude: float

class DeliveryInfos(BaseSchema):
    number: Optional[int]
    area_code: Optional[int]
    electrical_code: Optional[int]
    pole_number: Optional[int]
    address: Optional[str]
    coordinates: Optional[DeliveryCoordinates]

class ConnectionPole(BaseSchema):
    electrical_code: Optional[int]
    activation_date: Optional[date]
    desactivation_date: Optional[date]=None
    is_actived: bool = False
    
class DeliveryPointSchema(BaseSchema):
    id: int
    delivery_point_number: Optional[int]
    infos: DeliveryInfos
    connection_poles: Optional[List[ConnectionPole]]
    area_id: int
    pole_id: int
    is_activated: bool
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    
    class Config:
        orm_mode = True
    
class CreateDeliveryPoint(DeliveryPointSchema):
    class Config:
        fields_to_hide = {
            "id",
            "is_activated",
            "created_at",
            "updated_at",
            "deleted_at",
        }

#
class DeliveryPointInput(CreateDeliveryPoint):
    class Config:
        fields_to_hide = {
            "id",
            "area_id",
            "pole_id",
            "delivery_point_number"
        }

class DeliveryPointUpdate(DeliveryPointInput):
 pass

class DeliveryPointDetails(CreateDeliveryPoint):
    details: Dict
    class Config:
        fields_to_hide = {
            "id",
            "area_id",
            "pole_id",
            "infos"
        }